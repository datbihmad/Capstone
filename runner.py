import prompts 
import functions
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import table
import pydantic 
from pydantic import BaseModel, ValidationError
from typing import List
import config
import instructor
from openai import OpenAI
from typing import Callable, Dict
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

client = instructor.patch(OpenAI(
    api_key=config.madeline_openai_key
))

file = "data.csv"

# AI system

def main():
    df = read_csv_file(file)
    exploratory_data_response = exploratory_data_analysis(df)
    analysis_technique_response = analysis_technique(exploratory_data_response)
    if isinstance(exploratory_data_response, str):
        exploratory_data_response = json.loads(exploratory_data_response)
        print(exploratory_data_response)
    if isinstance(analysis_technique_response, str):
        analysis_technique_response = json.loads(analysis_technique_response)
    formatted_exploratory_data = format_json_data_for_report(exploratory_data_response)
    formatted_analysis_technique = format_analysis_plan_for_report(analysis_technique_response)
    graph_image = f"./report images/scatterplot.png"
    build_pdf_report(formatted_exploratory_data, formatted_analysis_technique, graph_image)
    # create_analysis(analysis_technique_response, df)


# Load in data or read data
def read_csv_file(file):
    df = pd.read_csv(file)
    return df



def exploratory_data_analysis(df):

    data_info_result = functions.data_info(df)
    data_describe_result = functions.data_describe(df)
    data_head_result = functions.data_head(df)
    data_nunique_result = functions.data_nunique(df)
    data_null_result = functions.data_null(df)

    api_schema_description = "The data we are looking at is on production debugging. The rows in the data frame denote a different api phase. Id is an identifier of each api phase. Execution time is of data type int and is how much time the api phase took to complete."
    data_schema_description = "The data we are looking at simple height and weight of different people. They are both int values. Height is the height of the person in inches and weight is the weight of the person in pounds."
    wine_schema_description = "The data we are looking at is on red wine. The rows in the data frame denote a different wine. The columns are the different attributes of the wine. The data is a mix of int and float values."
    exploratory_data_response = prompts.evaluate_exploratory_data_analysis(data_info_result, data_describe_result, data_head_result, data_nunique_result, data_null_result, wine_schema_description, verbose=True)
    return exploratory_data_response
  

class AnalysisTechniqueResponse(BaseModel):
    plan: Dict[str, str]
    function_to_call: int
    input_parameters: dict


def analysis_technique(exploratory_data_response):
    analysis_technique_response = prompts.evaluate_analysis_technique(exploratory_data_response, verbose=True)
 
    return analysis_technique_response

def create_analysis(analysis_technique_response, df):
    try:
        validated_data = AnalysisTechniqueResponse(**analysis_technique_response)
    except ValidationError as e:
        print(f"Validation Error: {e}")
        return

    index = validated_data.function_to_call
    input_params = validated_data.input_parameters  
    print(input_params)
   
    function_mappings = {
        1: functions.create_scatterplot,
        2: functions.create_sub_scatterplots,
        3: functions.create_sub_scatterplots_unique,
        4: functions.create_histogram,
        5: functions.create_histograms,
        6: functions.create_boxplot,
        7: functions.create_heatmap
    }

    if index in function_mappings:
        handler = function_mappings[index]
        if index == 1:
            x_column = input_params['x']
            y_column = input_params['y']
            handler(x=df[x_column], y=df[y_column])
        elif index == 7:  #
            handler(df)
        else:
            handler(df, **input_params)
    else:
        print(f"No handler defined for function_to_call: {index}")



def format_json_data_for_report(data):
    formatted_text = ""
    
    data_summary = data.get("data_summary", {})
    if data_summary:
        formatted_text += "Data Summary:\n"
        for key, value in data_summary.items():
            formatted_text += f"- {key.replace('_', ' ').capitalize()}: {value}\n"
            formatted_text += "\n"
        formatted_text += "\n"
 
    quality_score = data.get("quality_score", {})
    if quality_score:
        formatted_text += "Quality Score:\n"
        formatted_text += "\n"
        formatted_text += f"- Score: {quality_score.get('score', '')}\n"
        formatted_text += f"- Reasoning: {quality_score.get('reasoning', '')}\n"
        formatted_text += "\n"
  
    columns_to_drop = data.get("columns_to_drop", [])
    if columns_to_drop:
        formatted_text += "Columns to Drop:\n"
        for column in columns_to_drop:
            formatted_text += f"- {column}\n"
            formatted_text += "\n"
        formatted_text += "\n"
    else:
        formatted_text += "Columns to Drop: None\n\n"
        formatted_text += "\n"
   
    noteworthy_aspects = data.get("noteworthy_aspects", {})
    if noteworthy_aspects:
        formatted_text += "Noteworthy Aspects:\n"
        interesting_columns = noteworthy_aspects.get("interesting_columns", [])
        if interesting_columns:
            formatted_text += f"- Interesting Columns: {', '.join(interesting_columns)}\n"
            formatted_text += "\n"
        analysis_potential = noteworthy_aspects.get("analysis_potential", "")
        if analysis_potential:
            formatted_text += f"- Analysis Potential: {analysis_potential}\n"
            formatted_text += "\n"
        formatted_text += "\n"
    
    return formatted_text.strip()

def format_analysis_plan_for_report(json_data):
    formatted_text = ""
    
    plan = json_data.get("plan", {})
    if plan:
        formatted_text += "Analysis Plan:\n"
        for key, value in plan.items():
            formatted_text += f"- {key.replace('_', ' ').capitalize()}: {value}\n"
        formatted_text += "\n"
    
    function_to_call = json_data.get("function_to_call", "N/A")
    if function_to_call != "N/A":
        formatted_text += "Function to Call:\n"
        formatted_text += f"- {function_to_call}\n\n"
    
    input_parameters = json_data.get("input_parameters", {})
    if input_parameters:
        formatted_text += "Input Parameters:\n"
        for param, value in input_parameters.items():
            formatted_text += f"- {param.capitalize()}: {value}\n"
        formatted_text += "\n"
    
    return formatted_text.strip()


def build_pdf_report(exploratory_data_analysis_response, analysis_technique_response, graph_image):

    pdf_file = "output_document.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    content = []

    sections = exploratory_data_analysis_response.split("\n\n")

    for section in sections:
        para = Paragraph(section, normal_style)
        content.append(para)
        content.append(Spacer(1, 12))

    content.append(Paragraph(analysis_technique_response, normal_style))
    content.append(Spacer(1, 12))
    content.append(Image(graph_image, width=200, height=150))

    doc.build(content)



if __name__ == '__main__':
    main()
