import utlitityFunctions as util


def getPromptTemplate(data_input, verbose=False):
    system = "This is my system message I have created."
    user = f"This is my user message with the data_input, {data_input}."
    # Convert the system and user strings to a Messages object
    messages = util.convert_to_messages(system, user)
    # Get the parameters to call the OpenAI API
    params = util.get_chat_completion_params("gpt-4", messages, temperature=0.4)
    # Actually call the OpenAI ChatCompletion API, get the completion message
    completion = util.create_chat_completion(params)

    if verbose:
        print(completion)

    return completion


def evaluate_exploratory_data_analysis(data_info_result, data_describe_result, data_head_result, schema_description, verbose=False):
    system = f"You are a data science analyst. Your speciality is in doing initial exploratory data analysis and recommending next steps for analysis to your boss.\n\nYour boss has given you the following description of the data you will be dealing with: {schema_description}"+"\n\ndata_info is the returned string of the result from the pandas function pandas.info(). This is from the python package pandas and is originally a data frame. This function is used for displaying data types and information about the data frame. \n \ndata_describe is a returned string from a pandas function pandas.describe(). It is originally a data frame formatted into a string. This function is used for giving a descriptive statistical summary of numerical variables in the data frame. \n\ndata_head is a returned string of the result from the pandas function pandas.head(). This is originally structured as a data frame. This function is used to display the first 5 rows of the data frame from the original read data. \n\nYou are to perform an initial data analysis by following these instructions:\n1. Write a summary of the data that you see\n- data_info and data_describe will give an overview of the whole table\n- data_head will show a few examples \n2. Give a quality score between 1 to 7, this score should denote the cleanliness and quality of data. This will determine whether the data is ready for use or needs further cleaning and transformation before analysis. Give the result as an int value and then reason why. \n- a score of 1 means very terrible \n- a score of 7 means very excellent\n3. Note any columns that don't give any meaningful information and that should be dropped. \n4. Please note anything interesting or noteworthy about the data including particular columns in the data that would be worthy analyzing or looking more detail. \n\nReturn your response in json format: {\n  \"data_summary\": {\n    \"data_info\": \"Overview of the dataset including data types, missing values, etc.\",\n    \"data_describe\": \"Statistical summary of numerical columns, including mean, median, mode, etc.\",\n    \"data_head\": \"First few rows of the dataset to give a quick glimpse of the data entries.\"\n  },\n  \"quality_score\": {\n    \"score\": 4,\n    \"reasoning\": \"This score is based on the level of cleanliness, completeness, and readiness of the data for analysis. A score of 1 indicates very terrible quality, while a score of 7 indicates very excellent quality. The provided value is a placeholder and should be replaced with an actual assessment.\"\n  },\n  \"columns_to_drop\": [\n    \"column_name_1\",\n    \"column_name_2\"\n  ],\n  \"noteworthy_aspects\": {\n    \"interesting_columns\": [\n      \"column_name_3\",\n      \"column_name_4\"\n    ],\n    \"analysis_potential\": \"Details about why these columns are interesting and what kind of analysis could be done with them.\"\n  }\n}\n"

    user = f"data_info={data_info_result} \n\ndata_describe={data_describe_result} \n\ndata_head={data_head_result}"
    # Convert the system and user strings to a Messages object
    messages = util.convert_to_messages(system, user)
    # Get the parameters to call the OpenAI API
    params = util.get_chat_completion_params("gpt-4", messages, temperature=0.4)
    # Actually call the OpenAI ChatCompletion API, get the completion message
    completion = util.create_chat_completion(params)

    if verbose:
        print(completion)

    return completion
    

def evaluate_data_describe(data_info_result, data_describe_result, data_head_result, schema_description, verbose=False):
     
    system = f"\nI want you to do data analysis. \n\nThis is the output from a function pandas.describe(). This is from the python package pandas and is originally a data frame. This function is used for giving a descriptive statistical summary of numerical variables in the data frame. {schema_description} \n\nI would like you to give me a summary of what each of the outputs mean. Please note anything interesting or noteworthy about the data. "
    user = f"{data_info_result} \n\n{data_describe_result} \n\n{data_head_result}"
    # Convert the system and user strings to a Messages object
    messages = util.convert_to_messages(system, user)
    # Get the parameters to call the OpenAI API
    params = util.get_chat_completion_params("gpt-4", messages, temperature=0.4)
    # Actually call the OpenAI ChatCompletion API, get the completion message
    completion = util.create_chat_completion(params)

    if verbose:
        print(completion)

    return completion


  

def evaluate_data_info(info, verbose=False):
    
    system = "I want you to do data analysis. \n\nThis is the output from a function pandas.info(). This is from the python package pandas and is originally a data frame. This function is used for displaying data types and information about the data frame. \n\nI would like you to give me a summary of what each of the outputs mean. \n\nDescribe what the data set is and please note anything interesting or noteworthy about the data."
    user = f"{info}"
    # Convert the system and user strings to a Messages object
    messages = util.convert_to_messages(system, user)
    # Get the parameters to call the OpenAI API
    params = util.get_chat_completion_params("gpt-4", messages, temperature=0.4)
    # Actually call the OpenAI ChatCompletion API, get the completion message
    completion = util.create_chat_completion(params)

    if verbose:
        print(completion)

    return completion

