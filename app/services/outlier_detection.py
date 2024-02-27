import pandas as pd
from services.utils import feature_selection, get_anomalies_data, plot_outliers

def outlier_detection(file_path):
    df= pd.read_csv(file_path)
    feature_outliers = {}

    features_list= feature_selection(file_path)
    plot_outliers(file_path, features_list)
    for feature in features_list:
        if df[feature].dtype == 'object':
            cat_counts = df[feature].value_counts()
            threshold = 0.01 * len(df) 
            outliers = cat_counts[cat_counts < threshold]
            feature_outliers[feature] = outliers.index.tolist()
        else:
            q1 = df[feature].quantile(0.25)
            q3 = df[feature].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outliers = df[(df[feature] < lower_bound) | (df[feature] > upper_bound)]
            feature_outliers[feature] = outliers.index.tolist()
    get_anomalies_data(file_path, feature_outliers)
































##########################################################################################################################
##########################################################################################################################
# features= feature_selection('OpenStack_2k.log_structured.csv')
# print(features)
# print(type(features))
# df= pd.read_csv('OpenStack_2k.log_structured.csv')
# feature_outliers = {}

# for feature in features:
#     if df[feature].dtype == 'object':
#         cat_counts = df[feature].value_counts()
#         threshold = 0.01 * len(df) 
#         outliers = cat_counts[cat_counts < threshold]
#         feature_outliers[feature] = outliers.index.tolist()
#     else:
#         q1 = df[feature].quantile(0.25)
#         q3 = df[feature].quantile(0.75)
#         iqr = q3 - q1
#         lower_bound = q1 - 1.5 * iqr
#         upper_bound = q3 + 1.5 * iqr
#         outliers = df[(df[feature] < lower_bound) | (df[feature] > upper_bound)]
#         feature_outliers[feature] = outliers.index.tolist()

    


# for feature, outliers in feature_outliers.items():
#     print(f"Outliers in '{feature}': {outliers}")



