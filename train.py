import os
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_diabetes, fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error, accuracy_score
from mlflow.tracking import MlflowClient

# إعداد Tracking URI لـ MLflow
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"))
mlflow.set_experiment("MLOps_Disease_Boston_Experiment")

def run_pipeline():
    # 1. Data Ingest & Model Train (بيانات المرض - Classification)
    data_disease = load_diabetes()
    X_train, X_test, y_train, y_test = train_test_split(data_disease.data, (data_disease.target > 140).astype(int), test_size=0.2, random_state=42)

    with mlflow.start_run(run_name="Dev_Pipeline_Run"):
        # تدريب Logistic Regression / Random Forest
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)

        # تسجيل المعاملات والمقاييس في MLflow
        mlflow.log_param("model_type", "RandomForestRegressor")
        mlflow.log_metric("mse", mse)

        # تسجيل النموذج في MLflow Model Registry
        model_info = mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            registered_model_name="MLOps_Model"
        )

        # تعيين Alias للنموذج كـ 'Challenger' (الخطوة الخاصة بـ Dev Pipeline)
        client = MlflowClient()
        client.set_registered_model_alias(
            name="MLOps_Model",
            alias="Challenger",
            version=model_info.registered_model_version
        )
        print(f"Model saved in registry with alias 'Challenger', Version: {model_info.registered_model_version}")

if __name__ == "__main__":
    run_pipeline()
