import prompts 
import functions
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import table


file = "winequality-red.csv"

# AI system

def main():
    df = read_csv_file(file)
    exploritory_data_analysis(df)


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
    prompts.evaluate_exploratory_data_analysis(data_info_result, data_describe_result, data_head_result, data_nunique_result, data_null_result, wine_schema_description, verbose=True)

    # print(data_info_result)
    # print(data_head_result)
    # print(data_describe_result)


  
    # data_nunique_result = functions.data_nunique(df)
    # data_null_result = functions.data_null(df)
    # data_types_result = functions.check_data_types(df)





    

# begin the process of data analysis with explloritory data analysis
            # data_info(df)
            # data_describe(df)
            # data_head(df)
            # data_nunique(df)
    
# data quality check and cleaning

# based on exploritory data analysis, make a decision on what to do next
# perform data science and display with visualizations
# analyze the data and vizualizations


def save_table_as_image(data, data_info_result, data_describe_result, data_head_result):
    filename = "./report images"
    fig, ax = plt.subplots(figsize=(6.5, 4.875)) # Adjust figure size as needed
    ax.axis('off')
    tbl = table(ax, data, loc='center', cellLoc='center', rowLoc='center')
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.close()

    # Convert your results to DataFrames if they aren't already







if __name__ == '__main__':
    main()
