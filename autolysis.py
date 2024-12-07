# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "pandas",
#   "numpy",
#   "seaborn",
#   "scikit-learn",
#   "requests",
#   "matplotlib",
#   "tabulate"
# ]
# ///

"""
Imports 
"""

import os
import sys
import json
from typing import Tuple, Optional


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests



AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")


def load_data(file_path: str) -> pd.DataFrame:
    """
    Tries to load a CSV file with various encodings to handle different character encodings.
    
    :param file_path: Path to the CSV file.
    :return: Pandas DataFrame containing the dataset.
    """
    encodings_to_try = [
        'utf8','latin1','ascii', 'us-ascii', 'big5', 'big5-tw', 'csbig5', 'big5hkscs', 'big5-hkscs', 
        'cp037', 'IBM037', 'IBM039', 'cp273', 'IBM273', 'cp424', 'EBCDIC-CP-HE', 'IBM424', 
        'cp437', 'IBM437', 'cp500', 'EBCDIC-CP-BE', 'EBCDIC-CP-CH', 'IBM500', 'cp720', 
        'cp737', 'cp775', 'IBM775', 'cp850', 'IBM850', 'cp852', 'IBM852', 'cp855', 'IBM855', 
        'cp856', 'cp857', 'IBM857', 'cp858', 'IBM858', 'cp860', 'IBM860', 'cp861', 'IBM861', 
        'cp862', 'IBM862', 'cp863', 'IBM863', 'cp864', 'IBM864', 'cp865', 'IBM865', 'cp866', 
        'IBM866', 'cp869', 'IBM869', 'cp874', 'cp875', 'cp932', 'ms932', 'ms-kanji', 'windows-31j',
        'cp949', 'ms949', 'uhc', 'cp950', 'ms950', 'cp1006', 'cp1026', 'ibm1026', 'cp1125', 
        'ibm1125', 'cp1140', 'ibm1140', 'cp1250', 'windows-1250', 'cp1251', 'windows-1251', 
        'cp1252', 'windows-1252', 'cp1253', 'windows-1253', 'cp1254', 'windows-1254', 'cp1255', 
        'windows-1255', 'cp1256', 'windows-1256', 'cp1257', 'windows-1257', 'cp1258', 'windows-1258',
        'euc_jp', 'eucjp', 'ujis', 'u-jis', 'euc_jis_2004', 'jisx0213', 'eucjis2004', 'euc_jisx0213', 
        'eucjisx0213', 'euc_kr', 'euckr', 'korean', 'ks_c-5601', 'ks_c-5601-1987', 'ksx1001', 
        'ks_x-1001', 'gb2312', 'gbk', 'gb18030', 'hz', 'iso2022_jp', 'iso2022jp', 'iso-2022-jp', 
        'iso2022_jp_1', 'iso2022jp-1', 'iso2022_jp_2', 'iso2022jp-2', 'iso-2022-jp-2', 'iso2022_jp_2004', 
        'iso2022jp-2004', 'iso-2022-jp-2004', 'iso2022_jp_3', 'iso2022jp-3', 'iso-2022-jp-3', 'iso2022_jp_ext', 
        'iso2022jp-ext', 'iso-2022-jp-ext', 'iso2022_kr', 'iso2022kr', 'iso-2022-kr', 
        'iso-8859-1', 'iso8859-1', '8859', 'cp819', 'latin', 'latin1', 'L1', 'iso8859_2', 'iso-8859-2', 
        'latin2', 'L2', 'iso8859_3', 'iso-8859-3', 'latin3', 'L3', 'iso8859_4', 'iso-8859-4', 'latin4', 
        'L4', 'iso8859_5', 'iso-8859-5', 'cyrillic', 'iso8859_6', 'iso-8859-6', 'arabic', 'iso8859_7', 
        'iso-8859-7', 'greek', 'greek8', 'iso8859_8', 'iso-8859-8', 'hebrew', 'iso8859_9', 'iso-8859-9', 
        'latin5', 'L5', 'iso8859_10', 'iso-8859-10', 'latin6', 'L6', 'iso8859_11', 'iso-8859-11', 'thai', 
        'iso8859_13', 'iso-8859-13', 'latin7', 'L7', 'iso8859_14', 'iso-8859-14', 'latin8', 'L8', 'iso8859_15', 
        'iso-8859-15', 'latin9', 'L9', 'iso8859_16', 'iso-8859-16', 'latin10', 'L10', 'johab', 'cp1361', 
        'ms1361', 'koi8_r', 'koi8_t', 'koi8_u', 'kz1048', 'kz_1048', 'strk1048_2002', 'rk1048', 'mac_cyrillic', 
        'maccyrillic', 'mac_greek', 'macgreek', 'mac_iceland', 'maciceland', 'mac_latin2', 'maclatin2', 
        'maccentraleurope', 'mac_centeuro', 'mac_roman', 'macroman', 'macintosh', 'mac_turkish', 'macturkish', 
        'ptcp154', 'csptcp154', 'pt154', 'cp154', 'cyrillic-asian', 'shift_jis', 'csshiftjis', 'shiftjis', 
        'sjis', 's_jis', 'shift_jis_2004', 'shiftjis2004', 'sjis_2004', 'sjis2004', 'shift_jisx0213', 
        'shiftjisx0213', 'sjisx0213', 's_jisx0213', 'utf_32', 'U32', 'utf32', 'utf_32_be', 'UTF-32BE', 
        'utf_32_le', 'UTF-32LE', 'utf_16', 'U16', 'utf16', 'utf_16_be', 'UTF-16BE', 'utf_16_le', 'UTF-16LE', 
        'utf_7', 'U7', 'unicode-1-1-utf-7', 'utf_8', 'U8', 'UTF', 'cp65001', 'utf_8_sig'
    ]
    
    for encoding in encodings_to_try:
        try:
            data = pd.read_csv(file_path, encoding=encoding)
            print(f"Successfully loaded data with {encoding} encoding.")
            return data
        except UnicodeDecodeError:
            print(f"Failed to load data with {encoding} encoding. Trying next...")
        except Exception as e:
            print(f"An error occurred with {encoding} encoding: {e}")
            continue
    
    # We can't continue if we reach here
    raise NotImplementedError("Failed to load the CSV file with all attempted encodings.")



def summarize_data(data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    """
    Summarizes the dataset by providing numerical and categorical summary statistics,
    and counting missing values.

    :param data: Pandas DataFrame containing the dataset.
    :return: A tuple containing:
             - Numerical summary (DataFrame)
             - Categorical summary (DataFrame)
             - Missing values (Series)
    """
    numerical_summary = data.describe().T[['mean', '50%', 'std', 'min', 'max']]
    categorical_summary = data.select_dtypes(include=['object']).describe().T[['top', 'freq']]
    missing_values = data.isnull().sum()
    
    return numerical_summary, categorical_summary, missing_values


def generate_visualizations(data: pd.DataFrame, file_path: str) -> None:
    """
    Generates visualizations (e.g., correlation heatmap) based on the dataset.

    :param data: Pandas DataFrame containing the dataset.
    :param file_path: Path to the CSV file.
    :return: None
    """
    dataset_name = os.path.splitext(os.path.basename(file_path))[0]
    folder_path = os.path.join(os.getcwd(), dataset_name)
    os.makedirs(folder_path, exist_ok=True)
    
    corr_path = os.path.join(folder_path, "correlation_matrix.png")
    plt.figure(figsize=(10, 8))
    numerical_cols = data.select_dtypes(include=['number']).columns
    if numerical_cols.shape[0] > 1:
        correlation_matrix = data[numerical_cols].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Correlation Matrix")
        plt.savefig(corr_path)
        plt.close()


def analyze_with_llm(filename: str, api_key: str) -> Optional[str]:
    """
    Analyzes the dataset using an LLM via a proxy API and returns string in markdown format.

    :param filename: Path to the CSV dataset.
    :param api_key: OpenAI API key for authenticating the request.
    :return: string with the LLM's analysis results, or None if the request fails.
    """
    data = load_data(filename)
    summary_stats = data.describe().to_dict()
    column_info = {col: str(data[col].dtype) for col in data.columns}
    
    dataset_summary = {
        "columns": list(data.columns),
        "column_info": column_info,
        "summary_stats": summary_stats
    }
    url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data_prompt = f"""
    Analyze the dataset from the provided CSV file. Below is the summary information:
    
    Dataset Summary:
    Columns: {', '.join(data.columns)}
    Column Information (Data Types): {json.dumps(column_info, indent=2)}
    Summary Statistics (Key Insights):
    {json.dumps(dataset_summary, indent=2)}

    Based on this, please:
    1. Identify key trends and patterns.
    2. Point out any potential outliers or anomalies.
    3. Suggest any potential insights or analyses that might be valuable.
    4. Provide any other interesting observations from the dataset.

    Please return your findings in a MARKDOWN format you can use html in it to further beautify it, 
    highlighting the trends, insights, and any notable outliers or anomalies.
    """
    
    data_to_send = {
        "model": "gpt-4o-mini",
        "response_format": {"type": "text"},
        "messages": [
            {
                "role": "system",
                "content": """You are an intelligent data analyst capable of providing insights from datasets. 
                    You provide your insights in the form of a story which is very captivating.
                    You always support your claims with data. You only claim when you have data to back it up.
                    You are very professional and well versed in providing insights in comprehensive fashion.
                    You always return your findings in a MARKDOWN format you can use html in it to further beautify it."""
            },
            {
                "role": "user",
                "content": data_prompt
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=data_to_send)
    
    if response.status_code == 200:
        result = response.json()
        analysis = result["choices"][0]["message"]["content"]
        return analysis
    else:
        print(response.text)
        print(f"Error: {response.status_code}")
        return None


def save_readme(file_path: str, llm_response: str) -> None:
    """
    Saves the LLM response and analysis summary in a README.md file inside a folder 
    named after the dataset (folder name will be the same as the dataset filename).
    
    :param file_path: Path to the dataset CSV file.
    :param llm_response: The response from the LLM to be written into the README.
    """
    readme_path = get_readme(file_path)
    
    with open(readme_path, "a", encoding="utf-8") as f:
        f.write("\n## LLM Insights\n")
        f.write(f"{llm_response}\n")
    
    print(f"Analysis complete. Results saved to {readme_path} and charts.")


def get_readme(file_path: str) -> str:
    """
    Generates the file path for the README.md based on the dataset name.

    :param file_path: Path to the dataset file.
    :return: Path to the README.md file inside a folder named after the dataset.
    """
    dataset_name = os.path.splitext(os.path.basename(file_path))[0]
    folder_path = os.path.join(os.getcwd(), dataset_name)
    os.makedirs(folder_path, exist_ok=True)
    
    readme_path = os.path.join(folder_path, "README.md")
    return readme_path


def main(file_path: str) -> None:
    """
    Orchestrates the loading, summarizing, and analyzing of the dataset.
    It generates summary statistics, visualizations, and interacts with an LLM for further analysis.

    :param file_path: Path to the CSV file to be analyzed.
    """
    data = load_data(file_path)
    
    numerical_summary, categorical_summary, missing_values = summarize_data(data)
    
    readme_path = get_readme(file_path)

    with open(readme_path, "w") as f:
        f.write("# Data Summary\n")
        f.write("## Numerical Summary\n")
        f.write(numerical_summary.to_markdown())
        f.write("\n## Categorical Summary\n")
        f.write(categorical_summary.to_markdown())
        f.write("\n## Missing Values\n")
        f.write(missing_values.to_markdown())
    
    generate_visualizations(data, file_path)
    
    llm_response = analyze_with_llm(file_path, AIPROXY_TOKEN)

    if llm_response:
        save_readme(file_path, llm_response)
    
    print("Analysis complete. Results saved to README.md and charts.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a dataset filename.")
    else:
        file_path = sys.argv[1]
        main(file_path)
