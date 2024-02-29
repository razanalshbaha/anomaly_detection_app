from langchain.prompts import ChatPromptTemplate
import pandas as pd
import os
from langchain.chat_models import AzureChatOpenAI
import seaborn as sns
import matplotlib.pyplot as plt
from app.prompts.select_features import template_string
from config import AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT



def feature_selection(file_path):
    chat = AzureChatOpenAI(api_version="2023-07-01-preview", azure_deployment="razz2", temperature= 0.2)
    df = pd.read_csv(file_path)
    col= df.columns


    prompt_template = ChatPromptTemplate.from_template(template_string)
    customer_messages = prompt_template.format_messages(columns=col) 
    customer_response = chat(customer_messages)
    response= customer_response.content
    features_list = eval(response)
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
        if not os.path.exists('outlier_plots'):
            os.makedirs('outlier_plots')

        for feature in features:
            plt.figure(figsize=(8, 6))
            func(data, feature)
            plt.tight_layout()
            plt.savefig(f'outlier_plots/{feature}_{"outliers" if pd.api.types.is_numeric_dtype(data[feature]) else "countplot"}.png')
            plt.xticks(rotation=45)
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


