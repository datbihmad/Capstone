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


def evaluate_exploratory_data_analysis(data_info_result, data_describe_result, data_head_result, data_nunique_result, data_null_result, schema_description, verbose=False):
    system = f"You are a data science analyst. Your speciality is in doing initial exploratory data analysis and recommending next steps for analysis to your boss.\n\nYour boss has given you the following description of the data you will be dealing with: {schema_description}"+"\n\ndata_info is the returned string of the result from the pandas function pandas.info(). This is from the python package pandas and is originally a data frame. This function is used for displaying data types and information about the data frame. \n \ndata_describe is a returned string from a pandas function pandas.describe(). It is originally a data frame formatted into a string. This function is used for giving a descriptive statistical summary of numerical variables in the data frame. \n\ndata_head is a returned string of the result from the pandas function pandas.head(). This is originally structured as a data frame. This function is used to display the first 5 rows of the data frame from the original read data. \n\ndata_nunique is a returned string of the result from the pandas function pandas.nunique(). This is originally structured as a series. This function shows the count of unique values for each column. \n\ndata_isnull_sum is a returned string of the result from the pandas function pandas.isnull.sum().  THis is originally structured as a dataframe. This function shows the count of null (or NaN) values for each column. This helps to quickly identify missing data in your DataFrame.\n\ndata_types is a returned string of the result from the pandas functions pandas.dtypes(). This is originally formatted as a series. This function is used to show which columns are categorical variables and which columns are numerical variables.\n\nYou are to perform an initial data analysis by following these instructions:\n1. Write a summary of the data that you see\n- data_info, data_describe, data_nunique, data_isnull_sum, and data_types will give an overview of the whole table\n- data_head will show a few examples \n2. Give a quality score between 1 to 7, this score should denote the cleanliness and quality of data. This will determine whether the data is ready for use or needs further cleaning and transformation before analysis. Give the result as an int value and then reason why. \n- a score of 1 means very terrible \n- a score of 7 means very excellent\n3. Note any columns that don't give any meaningful information and that should be dropped. \n4. Please note anything interesting or noteworthy about the data including particular columns in the data that would be worthy analyzing or looking more detail. \n\nReturn your response in json format: {\n  \"data_summary\": {\n    \"data_info\": \"Overview of the dataset including data types, missing values, etc.\",\n    \"data_describe\": \"Statistical summary of numerical columns, including mean, median, mode, etc.\",\n    \"data_nunique\": \"Number of unique values in each column, to understand the diversity of data.\",\n    \"data_isnull_sum\": \"Total number of missing values in each column, to assess data completeness.\",\n    \"data_types\": \"Data types of each column, to ensure correct data handling and analysis.\",\n    \"data_head\": \"First few rows of the dataset to give a quick glimpse of the data entries.\"\n  },\n  \"quality_score\": {\n    \"score\": 4,\n    \"reasoning\": \"This score is based on the level of cleanliness, completeness, and readiness of the data for analysis. A score of 1 indicates very terrible quality, while a score of 7 indicates very excellent quality. The provided value is a placeholder and should be replaced with an actual assessment.\"\n  },\n  \"columns_to_drop\": [\n    \"column_name_1\",\n    \"column_name_2\"\n  ],\n  \"noteworthy_aspects\": {\n    \"interesting_columns\": [\n      \"column_name_3\",\n      \"column_name_4\"\n    ],\n    \"analysis_potential\": \"Details about why these columns are interesting and what kind of analysis could be done with them.\"\n  }\n}\n\n"

    user = f"data_info={data_info_result} \n\ndata_describe={data_describe_result} \n\ndata_head={data_head_result}, data_nunique={data_nunique_result}, data_isnull_sum={data_null_result}"
    # Convert the system and user strings to a Messages object
    messages = util.convert_to_messages(system, user)
    # Get the parameters to call the OpenAI API
    params = util.get_chat_completion_params("gpt-4", messages, temperature=0.4)
    # Actually call the OpenAI ChatCompletion API, get the completion message
    completion = util.create_chat_completion(params)

    if verbose:
        print(completion)

    return completion
    


def evaluate_analysis_technique(data_input, verbose=False):
    system = """You are a data science analyst. Your speciality is in figuring out what data science function to use based on the analysis you want to perform on the data.\n\nYour boss will provide you with summaries in JSON format from an exploratory data analysis. This will also include a description of the schema of the data you will be performing an analysis on. \n\nYour boss has also provided you with a list of functions that another expert will be using to call on. You have to choose from this list of functions in order for the expert to perform this analysis. \n\nIndex 1: create_scatterplot(x,y)\n- This function create a single function based on input variables x and y.\n\nIndex 2: create_scatterplots(df, columns)\n- This function creates multiple scatter plots based on the data examining unique columns . Takes the dataframe and columns as input variables.\n\nIndex 3: create_scatterplots_unique(df, phases):\n- This function creates multiple scatter plots based on the data examining unique variables within a column . Takes the data frame and unique column variables as input.\n\n\nIndex 4: create_histogram(x)\n- This function creates a single histogram based on the frequency of one input variable (a column) x.\n\nIndex 5: create_histograms(df, columns)\n- This functions creates multiple histograms based on the frequency of many columns given the input variables data frame and columns.\n\nIndex 6: create_boxplot(x)\n- This function created a box plot given one input variable x which is likely a specific column of values\n\nIndex 7: create_heatmap(df)\n -This function creates a heat map of the data frame. It is given the entire data frame as an input variable. \n\n\nFollowing these instructions, you will choose which functions to use\n1. Read all of the provided summaries and exploratory data analysis fully.\n2. Write a short plan on which analysis technique you plan on using and why you chose that specific one and also how you are planning on using it.\n- analysis_technique should be the data science technique that should be used for data analysis\n- rationale should be why you chose to use this technique \n3. Return the index of the function that you would like to call to perform analysis technique\n- This should be the function to call based on analysis technique given the options above. Pick only one function.\n4. Return the input parameters for the function to call. \n- Include the type and role. \n- If the input variables are x, y values make sure you include the column name for x, and the column name to be used for y. The variables should be labeled as x and y.\n\nPlease put your answer in the following json format:\n{\n  \"plan\": {\n    \"analysis_technique\": \"Insert analysis technique here\",\n    \"rationale\": \"Explain why this analysis technique was chosen based on the data and objectives\"\n  },\n  \"function_to_call\": 0,  // Adjust based on the function to call\n  \"input_parameters\": {\n    // Adjust based on required parameters for the specific function\n    // Example for create_scatterplot:\n    // \"x\": \"column_name_for_x\",\n    // \"y\": \"column_name_for_y\"\n    // Example for create_histogram:\n    // \"x\": \"column_name_for_x\"\n  }\n}\n\n\n\n"""
    
    
    user = f"{data_input}"
    # Convert the system and user strings to a Messages object
    messages = util.convert_to_messages(system, user)
    # Get the parameters to call the OpenAI API
    params = util.get_chat_completion_params("gpt-4", messages, temperature=0.4)
    # Actually call the OpenAI ChatCompletion API, get the completion message
    completion = util.create_chat_completion(params)

    if verbose:
        print(completion)

    return completion




def evaluate_graph_labels(data_input, verbose=False):
    system = "You are a data science analyst. Your speciality is in formatting graphs with proper labels. \n\nYour boss will provide you with summaries in JSON format from an analysis technique analysis. This will include the analysis technique chosen. Function to call and input parameters.\n\nYour job is to create appropriate labels for the graph including axis labels, graph title, and a legend if necessary. \n\nThe graph title should be a clear representation of what the graph depicts without actually including the type of graph. \n\nThe functions are as follows:\n1: functions.create_scatterplot,\n2: functions.create_sub_scatterplots,\n3: functions.create_sub_scatterplots_unique,\n4: functions.create_histogram,\n5: functions.create_histograms,\n6: functions.create_boxplot,\n7: functions.create_heatmap\n\n\n\n{\n  \"graph_labels\": {\n    \"axis_labels\": {\n      \"x_axis\": \"X-axis Label\",\n      \"y_axis\": \"Y-axis Label\"\n    },\n    \"graph_title\": \"Title of the Graph\",\n    \"legend\": {\n      \"display\": true,\n      \"labels\": [\n        {\n          \"label\": \"Dataset 1\",\n          \"color\": \"blue\",\n          \"shape\": \"circle\"\n        },\n        {\n          \"label\": \"Dataset 2\",\n          \"color\": \"red\",\n          \"shape\": \"square\"\n        }\n      ],\n      \"position\": \"top-right\"\n    }\n  }\n}\n"
    
    user = f"{data_input}"
    # Convert the system and user strings to a Messages object
    messages = util.convert_to_messages(system, user)
    # Get the parameters to call the OpenAI API
    params = util.get_chat_completion_params("gpt-4", messages, temperature=0.4)
    # Actually call the OpenAI ChatCompletion API, get the completion message
    completion = util.create_chat_completion(params)

    if verbose:
        print(completion)

    return completion
    