from .outlier_class import OutlierDetection


async def outlier_detection(file_path):
    object = OutlierDetection()
    data = object.read_csv(file_path)
    selected_features = await object.select_features(file_path)
    plots = object.plot(file_path, data)
    detected_outliers = object.detect_outliers(file_path, selected_features)
    anomalies = object.get_anomalies(file_path, detected_outliers)
    return anomalies, plots


