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


def evaluate_call_describe(description, verbose=False):
     
    system = "\nI want you to do data analysis. \n\nThis is the output from a function pandas.describe(). This is from the python package pandas and is originally a data frame. This function is used for giving a descriptive statistical summary of numerical variables in the data frame. \n\nThe data we are looking at is on production debugging. The rows in the data frame denote a different api phase. Id is an identifier of each api phase. Execution time is of data type int and is how much time the api phase took to complete.\n\nI would like you to give me a summary of what each of the outputs mean. Please note anything interesting or noteworthy about the data. "
    user = f"{description}"
    # Convert the system and user strings to a Messages object
    messages = util.convert_to_messages(system, user)
    # Get the parameters to call the OpenAI API
    params = util.get_chat_completion_params("gpt-4", messages, temperature=0.4)
    # Actually call the OpenAI ChatCompletion API, get the completion message
    completion = util.create_chat_completion(params)

    if verbose:
        print(completion)

    return completion


  
