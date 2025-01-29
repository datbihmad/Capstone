# Automated Data Science Analysis with AI

## Overview
This project automates the data science analysis process by leveraging Artificial Intelligence (AI) to generalize fundamental components of data science across a diverse range of datasets. The AI system aims to minimize manual, repetitive tasks associated with data preprocessing, analysis, and interpretation, making the process more efficient and accessible.

At its core, the project involves developing AI algorithms capable of performing a comprehensive suite of data science operations, including:
- **Exploratory Data Analysis (EDA)**: Understanding dataset characteristics, identifying patterns, outliers, and anomalies, and determining the most appropriate analytical techniques.
- **Data Analysis Decision-Making**: AI determines the most relevant analytical approach based on EDA results.
- **Automated Graph Labeling**: AI dynamically generates titles and axis labels for visualizations.


## Project Structure
The repository includes multiple Python files, each playing a distinct role in automating the data science workflow. Below is an explanation of key source files:

### `function.py` / `functions.ipynb`
This file contains all functions used for Exploratory Data Analysis (EDA) and generating visualizations. The functions are generalized to support different datasets and can be tested using the `main()` function. However, the primary execution should be handled via `runner.py`.

### `prompts.py` / `prompts.ipynb`
This file contains AI prompts specifically designed for the project. There are three AI models used in the pipeline:
1. **EDA Model**: Processes dataset characteristics using various EDA functions.
2. **Analysis Selection Model**: Determines the appropriate data analysis technique based on the EDA model's output. Some inconsistencies exist where the model sometimes specifies analysis types (e.g., Correlation Analysis, Linear Regression) and other times refers to specific visualization methods (e.g., Heatmap, Scatterplot). Further refinement is needed.
3. **Graph Labeling Model**: Generates graph titles and axis labels. Output varies, sometimes including units (e.g., inches, centimeters) or producing creative vs. generic titles. Further testing is required to enhance consistency.

### `runner.py` / `runner.ipynb`
This is the main execution file that controls all AI models and outputs. Users should run this file to produce results. Key functionalities include:
- Connecting to the appropriate datasets.
- Running EDA functions.
- Generating AI-driven analyses and visualizations.
- Saving outputs, including graphs and a PDF report.

The report generation is a work in progress. The current approach involves creating a PDF with all results, but transitioning to a Jupyter Markdown-to-PDF workflow may be more effective for improved formatting.

### `utilityFunction.py` / `utilityFunction.ipynb`
This file contains utility functions for connecting to external services, including:
- **OpenAI API**: For AI model execution.
- **Supabase Database**: For data storage and retrieval.
- **Postico Local Database**: For local dataset management.

## Configuration and Security
Certain sensitive files, including `config.py`, have been excluded from this repository for security reasons. These files contain:
- OpenAI API Key
- Database credentials (Supabase, Postico, etc.)

To run the project successfully, users must provide their own API keys and database credentials on their local machines.

## Getting Started
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add your OpenAI API key and database credentials to a local `config.py` file.
4. Run the project by executing `runner.py`:
   ```bash
   python runner.py
   ```

