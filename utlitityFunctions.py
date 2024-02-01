import tiktoken
from openai import OpenAI
import json
import config
import os
from tenacity import retry, wait_random_exponential, stop_after_attempt
import psycopg2
from config import config_psql
import time
from supabase import create_client, Client



SUPABASE_URL = config.SUPABASE_URL
SUPABASE_KEY = config.SUPABASE_KEY
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=config.madeline_openai_key,
)

def main():
    pass


def convert_to_messages(system, user):
    return [
        {'role': 'system', 'content': system},
        {'role': 'user', 'content': user}
    ]


def get_chat_completion_params(model, messages, temperature=1, max_tokens=None, top_p=1,
                               stream=False, frequency_penalty=0, presence_penalty=0):
    # Create the parameters dictionary
    params = {
        'model': model,
        'messages': messages,
        'temperature': temperature,
        'top_p': top_p,
        'frequency_penalty': frequency_penalty,
        'presence_penalty': presence_penalty,
        'stream': stream
    }

    # Add 'max_tokens' to the dictionary if it's provided
    if max_tokens is not None:
        params['max_tokens'] = max_tokens

    return params


import asyncio

def create_chat_completion(params):
    # Extract specific parameters
    completion = None
    try:
        if params['model'] == "gpt-4-1106-preview" or params['model'] == "gpt-3.5-turbo-1106":
            
            completion =  client.chat.completions.create(
                model=params['model'],
                messages=params['messages'],
                temperature=params['temperature'],
                top_p=params['top_p'],
                frequency_penalty=params['frequency_penalty'],
                presence_penalty=params['presence_penalty'],
                stream=params['stream'],
                response_format={"type": "json_object"}
            )
        else:
            completion =  client.chat.completions.create(
                model=params['model'],
                messages=params['messages'],
                temperature=params['temperature'],
                top_p=params['top_p'],
                frequency_penalty=params['frequency_penalty'],
                presence_penalty=params['presence_penalty'],
                stream=params['stream'],
            )

        if not completion:
            raise Exception(f"OpenAI API call failed with status: {completion}")

        # prompt_tokens = completion['usage']['prompt_tokens']
        # completion_tokens = completion['usage']['completion_tokens']
        # cost = 0

        # if prompt_tokens == 0 or completion_tokens == 0:
        #     print("WARNING: prompt_tokens or completion_tokens is 0!")
        # else:
        #     cost = calculate_chat_completion_cost(model, prompt_tokens, completion_tokens)

        # await insert_completion_cost(phase, prompt_tokens, completion_tokens, cost, model, your_supabase_url, your_supabase_key)
    
    except Exception as error:
        print(f"Error: {error}")

    return completion.choices[0].message.content

## DECORATORS
# Debug decorator specifically for gpt completions
def gpt_wrapper(func):
    def inner(*args, **kwargs):
        if "debug_print" in kwargs:
            print_debug = kwargs["debug_print"]
        else:
            print_debug = False
        if print_debug:
            print("## Before openAI create_chat_completion:\n## Used Model: {}, API Key: {}\n## Function Input: {}".format(kwargs["used_model"], kwargs["api_key_choice"], kwargs["prompt_messages"]))
        begin = time.time()
        returned_value = func(*args, **kwargs)
        end = time.time()
        if print_debug:
            prompt_tokens = returned_value.usage["prompt_tokens"]
            completion_tokens = returned_value.usage["completion_tokens"]
            total_tokens = returned_value.usage["total_tokens"]
            total_cost = calculate_prompt_cost(kwargs["used_model"], prompt_tokens, completion_tokens)
            print("## After openAI create_chat_completion:\n## Total time in {}: {}, Prompt Tokens: {}, Completion Tokens: {}, Total Tokens: {}, Total Cost: ${},\n## GPT Output: {}".format(func.__name__, end-begin,prompt_tokens, completion_tokens, total_tokens, total_cost, returned_value.choices[0].message.content))
        return returned_value
    return inner

# General debug decorator
def debug(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args: {args}, \
        kwargs: {kwargs}")
        begin = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("{} ran in {}.".format(func.__name__, end-begin))
        print(f"{func.__name__} returned: {result}")
        return result

    return wrapper


# Deprecated

def num_tokens_from_string(string):
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(string))
    return num_tokens


    
# PSQL Access Functions, previously getPSQLConn.py
def psql_connect(user):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        
        conn = psycopg2.connect(database="floridalocal",host="localhost",user="madelinekaufman",password=config.localdb_password,port="5432",client_encoding="utf8")
       
		
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise error

def select_and_fetch_rows(conn, sql_select):
    cursor = conn.cursor()
    cursor.execute(sql_select)
    rows = cursor.fetchall()
    cursor.close()
    return rows


def create_embedding(input_text):
    """Create an embedding from a string of text."""
    response = client.embeddings.create(
        input=input_text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

# Prompt cost calculations
def calculate_prompt_cost(model, prompt_tokens, completion_tokens):
    model_rates = {"gpt-3.5-turbo-16k":[0.003, 0.004], "gpt-3.5-turbo-4k":[0.0015, 0.002], "gpt-4":[0.03, 0.06], "gpt-4-32k":[0.06, 0.12]}
    prompt_rate = model_rates[model][0]
    completion_rate = model_rates[model][1]
    cost = ((prompt_rate/1000)*prompt_tokens) + ((completion_rate/1000)*completion_tokens)
    #print("Prompt Tokens: {}, Completion Tokens: {}".format(prompt_tokens, completion_tokens))
    #print("Total cost of using {}: ${}".format(model, cost))
    return "${}".format(round(cost, 3))

 

def read_row_by_node_id(user, table_name, node_id):
    conn = psql_connect(user)
    cursor = conn.cursor()

    # Prepare the query string with placeholders
    query = f"SELECT node_type, node_level_classifier, node_text, node_citation, node_link, node_addendum, node_name, node_parent FROM {table_name} WHERE node_id='{node_id}';"
    cursor.execute(query)
    row = cursor.fetchall()
    cursor.close()
    return row

    
if __name__ == "__main__":
    main()
