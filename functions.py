import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import prompts 
import math
import io
from pandas.plotting import table
from PIL import Image, ImageDraw, ImageFont
import os

# data_table = "data.csv"
# data_table = "production_api_debug_rows.csv"
data_table = "data.csv"




def main():
    df = pd.read_csv(data_table)
    # phases = df['api_phase'].unique()
    create_scatterplot(df['Height'], df['Weight'])
    # create_boxplot(df['quality'])
  

# Functions to save outputs of exploritory data analysis as images

def save_table_as_image(data, filename):
    filename = f"./report images/{filename}"
    fig, ax = plt.subplots(figsize=(data.shape[1], data.shape[0]))
    ax.axis('off')
    tbl = table(ax, data, loc='center', cellLoc='center', rowLoc='center')
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.close()


def text_to_image_pil(text, filename):
    filename = f"./report images/{filename}"
    width, height = 800, 600 
    image = Image.new('RGB', (width, height), color = (255, 255, 255))
    d = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    d.text((10,10), text, fill=(0,0,0), font=font)
    image.save(filename)


def graph_to_image(graph, filename):
    filename = f"./report images/{filename}"
    graph.savefig(filename)
    plt.close()



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
    describe_result = df.describe(include="number")
    result_describe_formatted = describe_result.to_string()
    return result_describe_formatted

# pandas.DataFrame.unique() displays the unique values in a column
# Returns a series
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.unique.html
def unique(df, column_name):
    phases = df[column_name].unique()
    print(phases)
    create_sub_scatterplots_unique(df, phases)

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


# Creates a scatterplot
def create_scatterplot(graph_labels, x, y):
    plt.scatter(x,y)
    plt.title(graph_labels.get("graph_title", "Scatterplot"))
    plt.xlabel(graph_labels.get("axis_labels", {}).get("x_axis", "X-axis"))
    plt.ylabel(graph_labels.get("axis_labels", {}).get("y_axis", "Y-axis"))
    
    # Handle legend if specified
    if graph_labels.get("legend", {}).get("display", False):
        legend_labels = [label_info.get("label") for label_info in graph_labels["legend"]["labels"]]
        plt.legend(legend_labels, loc=graph_labels["legend"].get("position", "best"))
    
    
    folder_path = 'report images'  
    filename = 'scatterplot.png'
    
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    file_path = os.path.join(folder_path, filename)
    plt.savefig(file_path)
    plt.close()
    return file_path

# Creates multiple scatter plots for columns 
def create_sub_scatterplots(df, columns):
 

    x = df['quality']
    count_subplots = len(columns)
    columns = 4
    rows = math.ceil(count_subplots / columns)
    fig, axs = plt.subplots(rows, columns, figsize=(20, 10))

    for i, column in enumerate(columns):
        y = df[column]
        ax = axs[i//4, i%4]  
        ax.scatter(y, x)
        ax.set_title(f'Column: {column}')
        ax.set_xlabel('Quality')
        ax.set_ylabel(f"{column}")

    plt.tight_layout()
    plt.show()



# Creates scatter plots for unique values in a column
def create_sub_scatterplots_unique(df, phases):
    print(phases)

    x = df['quality']
    count_subplots = len(phases)
    columns = 4
    rows = math.ceil(count_subplots / columns)
    fig, axs = plt.subplots(rows, columns, figsize=(20, 10))


    for i, phase in enumerate(phases):
        y = df[phase]
        ax = axs[i//4, i%4]  
        ax.scatter(y, x)
        ax.set_title(f'Phase: {phase}')
        ax.set_xlabel('Quality')
        ax.set_ylabel(f"{phase}")

    plt.tight_layout()
    plt.show()


# Creates a histogram
def create_histogram(x):
    plt.hist(x)
    plt.show()

# Creates multiple histograms
def create_histograms(df, columns):
    num_columns = len(columns)
    rows = 2  
    cols = math.ceil(num_columns / rows)
    
    fig, axs = plt.subplots(rows, cols, figsize=(20, 10))
    axs = axs.flatten()  

    for i, column in enumerate(columns):
        if i < len(axs): 
            axs[i].hist(df[column], bins=20) 
            axs[i].set_title(f'Histogram of {column}')
            axs[i].set_xlabel(column)
            axs[i].set_ylabel('Frequency')
    
    for j in range(i + 1, len(axs)):
        axs[j].set_visible(False)
    
    plt.tight_layout()
    plt.show()

# Creates a boxplot
def create_boxplot(x):
    sns.boxplot(x)
    plt.show()

# Creates a heatmap
def create_heatmap(df):
    sns.heatmap(df.corr(), annot=True)
    plt.show()




if __name__ == '__main__':
    main()