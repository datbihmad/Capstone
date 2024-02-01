import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import prompts 
import math

data_table = "data.csv"

def main():
    df = pd.read_csv(data_table)
    create_scatterplot(df["Height"], df["Weight"])
    # data_info(df)
    # data_head(df)
    # data_nunique(df)
    # unique(df, 'api_phase')
    # description = call_describe(df)
    # response = prompts.evaluate_call_describe(description, verbose=True)
    # x = df['id']
    # y = df['execution_time']
    # create_scatterplot(x,y)
    # print(response)


# Helper Functions

# python.info() displays data types and information about the data frame
def data_info(df):
    result_info = df.info()

# python.head() displays the first 5 rows of the data frame
def data_head(df):
    result_head = df.head()

# python.tail() displays the last 5 rows of the data frame
def data_tail(df):
    result_tail = df.tail()

# python.nunique() displays the number of unique values in each column
def data_nunique(df):
    result_unique = df.nunique()

# python.isnull().sum() displays the number of null values in each column
def data_null(df):
    result_null = df.isnull().sum()

# python.describe() displays the summary statistics of the data frame
def call_describe(df):
    result = df.describe(include="number")
    result_describe_formatted = result.to_string()
    return result_describe_formatted

# python.unique() displays the unique values in a column
def unique(df, column_name):

    phases = df[column_name].unique()
    create_sub_scatterplots(df, phases)

# python.drop() drops a column
def data_drop(df):
    result_drop = df.drop(columns=['id'])
    print(result_drop)
    return result_drop

# python.dropna() drops all rows with null values
def data_dropna(df):
    result_dropna = df.dropna()
    print(result_dropna)
    return result_dropna


def check_data_types(df):
    obj_cols = df.select_dtypes(include=['object']).columns
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    print("Categorical Variables:")
    print(obj_cols)
    print("Numerical Variables:")
    print(num_cols)




# Actual Components
    
# Creates scatter plots for each phase
def create_sub_scatterplots(df, phases):
   
    # Create the dimensions of displaying multiple scatterplots
    count_subplots = len(phases)
    columns = 4
    rows = math.ceil(count_subplots / columns)
    fig, axs = plt.subplots(rows, columns, figsize=(20, 10))

    for i, phase in enumerate(phases):
        ax = axs[i // 4, i % 4]
        data = df[df['api_phase'] == phase]
        ax.scatter(data['id'], data['execution_time'])
        ax.set_title(phase)
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