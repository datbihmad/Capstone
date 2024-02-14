import prompts 
import functions
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import table
import pydantic 
from pydantic import BaseModel
from typing import List
import config
import instructor
from openai import OpenAI

client = instructor.patch(OpenAI(
    api_key=config.madeline_openai_key
))

file = "winequality-red.csv"

# AI system

def main():
    df = read_csv_file(file)
    exploritory_data_analysis_response = exploritory_data_analysis(df)
    analysis_technique_response = analysis_technique(exploritory_data_analysis_response)
    print(analysis_technique_response)
    print(type(analysis_technique_response))
    # create_analysis(analysis_technique_response, df)


# Load in data or read data
def read_csv_file(file):
    df = pd.read_csv(file)
    return df



def exploritory_data_analysis(df):
    # what is the data
    data_info_result = functions.data_info(df)
    data_describe_result = functions.data_describe(df)
    data_head_result = functions.data_head(df)
    data_nunique_result = functions.data_nunique(df)
    data_null_result = functions.data_null(df)
    # data_types_result = functions.check_data_types(df)

    
    api_schema_description = "The data we are looking at is on production debugging. The rows in the data frame denote a different api phase. Id is an identifier of each api phase. Execution time is of data type int and is how much time the api phase took to complete."
    data_schema_description = "The data we are looking at simple height and weight of different people. They are both int values. Height is the height of the person in inches and weight is the weight of the person in pounds."
    wine_schema_description = "The data we are looking at is on red wine. The rows in the data frame denote a different wine. The columns are the different attributes of the wine. The data is a mix of int and float values."
    exploritory_data_analysis_response = prompts.evaluate_exploratory_data_analysis(data_info_result, data_describe_result, data_head_result, data_nunique_result, data_null_result, wine_schema_description, verbose=True)
    return exploritory_data_analysis_response
    # print(data_info_result)
    # print(data_head_result)
    # print(data_describe_result)

class ExploratoryResponse(BaseModel):
    analysis_technique: List[str]
    rationale: List[str]
    function_to_call: List[int] 

  
    # data_nunique_result = functions.data_nunique(df)
    # data_null_result = functions.data_null(df)
    # data_types_result = functions.check_data_types(df)

def analysis_technique(exploritory_data_analysis_response):
    data_technique_response = prompts.evaluate_analysis_technique(exploritory_data_analysis_response, verbose=True)
    exploratory_response = ExploratoryResponse(**data_technique_response)
 
    return exploratory_response

def create_analysis(analysis_technique_response, df):
    
    index = analysis_technique_response['function_to_call']
    print(type(index))
    x = None
    y = None
    columns = None
    phases = None

    if '1' in index:
        analysis_technique = "create_scatterplot"
        functions.create_scatterplot(x, y)
    elif '2' in index:
        analysis_technique = "create_scatterplots"
        functions.create_scatterplots(df, columns)
    elif '3' in index:
        analysis_technique = "create_scatterplots_unique"
        functions.create_scatterplots_unique(df, phases)
    elif '4' in index:
        analysis_technique = "create_histogram"
        functions.create_histogram(x)
    elif '5' in index:
        analysis_technique = "create_histograms"
        functions.create_histograms(df, columns)
    elif '6' in index:
        analysis_technique = "create_boxplot"
        functions.create_boxplot(x)
    elif '7' in index:
        analysis_technique = "create_heatmap"
        functions.create_heatmap(df)


# begin the process of data analysis with explloritory data analysis
            # data_info(df)
            # data_describe(df)
            # data_head(df)
            # data_nunique(df)
    
# data quality check and cleaning

# based on exploritory data analysis, make a decision on what to do next
# perform data science and display with visualizations
# analyze the data and vizualizations











if __name__ == '__main__':
    main()
