import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import prompts 
import math
import io

data_table = "winequality-red.csv"




def main():
    df = pd.read_csv(data_table)
    
    x = df.columns
    y = df['quality']
    create_sub_scatterplots(df, x, y)
    # data_info(df)
    # data_head(df)
    # data_nunique(df)
    # unique(df, 'api_phase')
    # description = call_describe(df)
   
    # response = prompts.evaluate_data_info(info, verbose=False)
    # x = df['id']
    # y = df['execution_time']
    # create_scatterplot(x,y)
    # print(response)




# Helper Functions

# pandas.DataFrame.info() displays data types and information about the data frame including the index dtype and columns, non-null values and memory usage.
# Returns None so have to create a io.StringIO object to capture the output
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.info.html
def data_info(df):
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    return info_str
    


# pandas.DataFrame.head() displays the first 5 rows of the data frame
# Returns type of caller - the first n rows
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.head.html
def data_head(df, rows=2):
    result_head = df.head(rows)
    formatted_result_head = result_head.to_string()
    return formatted_result_head



# pandas.DataFrame.tail() displays the last 5 rows of the data frame
# Returns type of caller - the last n rows
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.tail.html
def data_tail(df):
    result_tail = df.tail()
    formatted_result_tail = result_tail.to_string()
    return formatted_result_tail



# pandas.DataFrame.nunique() displays the number of unique values in each column
# Returns a series
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.nunique.html
def data_nunique(df):
    result_unique = df.nunique()
    formatted_result_unique = result_unique.to_string()
    return formatted_result_unique

# pandas.DataFrame.isnull().sum() displays the number of null values in each column
# Returns bool or array-like of bool
# https://pandas.pydata.org/docs/reference/api/pandas.isnull.html
def data_null(df):
    result_null = df.isnull().sum()
    formatted_result_null = result_null.to_string()
    return formatted_result_null



# pandas.DataFrame.describe() displays the summary statistics of the data frame
# Returns a Series or DataFrame
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html
def data_describe(df):
    result = df.describe(include="number")
    result_describe_formatted = result.to_string()
    return result_describe_formatted



# pandas.DataFrame.unique() displays the unique values in a column
# Returns a series
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.unique.html
def unique(df, column_name):

    phases = df[column_name].unique()
    # create_sub_scatterplots(df, phases)



# pandas.DataFrame.drop() drops a column
# Returns a DataFrame or None
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop.html
def data_drop(df):
    result_drop = df.drop(columns=['id'])
    print(result_drop)
    return result_drop



# pandas.DataFrame.dropna() drops all rows with null values
# Returns a DataFrame or None
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dropna.html
def data_dropna(df):
    result_dropna = df.dropna()
    print(result_dropna)
    return result_dropna



# pandas.DataFrame.select_dtypes() selects columns based on data types
# Returns a DataFrame
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.select_dtypes.html
def check_data_types(df):
    obj_cols = df.select_dtypes(include=['object']).columns
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    print("Categorical Variables:")
    print(obj_cols)
    print("Numerical Variables:")
    print(num_cols)
    formatted_obj_cols = obj_cols.to_string()
    formatted_num_cols = num_cols.to_string()
    return formatted_obj_cols, formatted_num_cols



# Actual Components
    
# Creates scatter plots for each phase
def create_sub_scatterplots(df, x, y):
    columns = df.columns
    # Create the dimensions of displaying multiple scatterplots
    count_subplots = len(columns)
    rows = math.ceil(4)
    fig, axs = plt.subplots(rows, 4, figsize=(20, 10))

    # Iterate through the phases and create a scatterplot for each
    for i, column in enumerate(columns):
        ax = axs[i // 4, i % 4]
        data = df[df[column] == column]
        ax.scatter(data[x], data[y])
        ax.set_title(column)

    plt.tight_layout()
    plt.show()



# Creates a scatterplot
def create_scatterplot(x,y):
    plt.scatter(x,y)
    plt.show()


def create_histogram(x):
    plt.hist(x)
    plt.show()


def create_boxplot(x):
    sns.boxplot(x)
    plt.show()

def create_heatmap(df):
    sns.heatmap(df.corr(), annot=True)
    plt.show()





if __name__ == '__main__':
    main()