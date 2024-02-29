from .outlier_detection_class import OutlierDetection
from config import AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT


def outlier_detection(file_path):
    data = OutlierDetection.read_csv(file_path)
    selected_features = OutlierDetection.select_features(file_path)
    plots = OutlierDetection.plot(file_path, data)
    detected_outliers = OutlierDetection.detect_outliers(file_path, selected_features)
    anomalies = OutlierDetection.get_anomalies(file_path, detected_outliers)
    return anomalies
