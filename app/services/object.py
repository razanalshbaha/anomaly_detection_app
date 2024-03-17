from .outlier_class import OutlierDetection


async def outlier_detection(file_path):
    object = OutlierDetection()
    df = object.read_csv(file_path)
    selected_features = await object.select_features(df)
    plots = object.plot(df,selected_features)
    detected_outliers = object.detect_outliers(df, selected_features)
    anomalies = object.get_anomalies(df, detected_outliers)
    return anomalies, plots


