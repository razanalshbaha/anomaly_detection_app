import pandas as pd
from .utils import feature_selection, get_anomalies_data, plot_outliers




class OutlierDetection:
    @staticmethod
    def read_csv(file_path):
        df= pd.read_csv(file_path)
        return df
    
    @staticmethod
    async def select_features(file_path):
        features= await feature_selection(file_path)
        return features
    
    @staticmethod
    def plot(file_path, features):
        return plot_outliers(file_path, features)
    
    @staticmethod
    def detect_outliers(file_path, features):
        df= OutlierDetection.read_csv(file_path)
        feature_outliers = {}
        for feature in features:
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
        return feature_outliers
    
    @staticmethod
    def get_anomalies(file_path, feature_outliers):
        anomalies= get_anomalies_data(file_path, feature_outliers)
        return anomalies

