from langchain.prompts import ChatPromptTemplate
import pandas as pd
import os
#from langchain.chat_models import AzureChatOpenAI
from langchain_openai import AzureChatOpenAI
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
from app.prompts.select_features import template_string
from app.database.database import sessions_collection
import ast
from config import AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT
#from .outlier_detection import OutlierDetection
os.environ["AZURE_OPENAI_ENDPOINT"]=AZURE_OPENAI_ENDPOINT
os.environ["AZURE_OPENAI_API_KEY"]=AZURE_OPENAI_API_KEY




async def feature_selection(file_path):
    chat = AzureChatOpenAI(api_version="2023-07-01-preview", azure_deployment="razz2", temperature= 0.2)
    df = pd.read_csv(file_path)
    col= df.columns

    prompt_template = ChatPromptTemplate.from_template(template_string)
    customer_messages = prompt_template.format_messages(columns=col) 
    customer_response = await chat.ainvoke(customer_messages)
    response= customer_response.content
    features_list = []
    if isinstance(response, str):
        features_list = ast.literal_eval(response)
    return features_list


def get_anomalies_data(file_path, anomalies):
    df = pd.read_csv(file_path)
    outlier_df = pd.DataFrame(columns=df.columns)
    
    for feature, outlier_values in anomalies.items():
        outlier_rows = df[df[feature].isin(outlier_values)]
        outlier_df = pd.concat([outlier_df, outlier_rows])
    
    anomalies_data = outlier_df.to_dict(orient='records')
    return anomalies_data
    


def plot_decorator(func):
    def wrapper(*args):
        file_path, features = args
        data = pd.read_csv(file_path)
        plots = {}

        for feature in features:
            plt.figure(figsize=(8, 6))
            func(data, feature)
            plt.tight_layout()
            plot_key = f'plot_{feature}'
            plot_stream = BytesIO()
            plt.savefig(plot_stream, format='png')
            plots[plot_key] = plot_stream.getvalue()
            plt.close()

        return plots

    return wrapper

@plot_decorator
def plot_outliers(data, feature):
    if pd.api.types.is_numeric_dtype(data[feature]):
        Q1 = data[feature].quantile(0.25)
        Q3 = data[feature].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = data[(data[feature] < lower_bound) | (data[feature] > upper_bound)]

        sns.boxplot(x=data[feature])
        plt.title(f'Boxplot of {feature} with Outliers Highlighted')
        plt.scatter(outliers.index, outliers[feature], color='red', label='Outliers')
        plt.legend()
    else:
        sns.countplot(x=feature, data=data, palette='viridis')
        plt.title(f'Countplot of {feature}')



