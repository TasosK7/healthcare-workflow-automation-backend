import requests
import os

AIRFLOW_EMAIL_DAG_TRIGGER_URL = os.getenv("AIRFLOW_DAG_TRIGGER_URL", "http://localhost:8080/api/v1/dags/appointment_email_flow/dagRuns")
AIRFLOW_USERNAME = os.getenv("AIRFLOW_USERNAME", "airflow")
AIRFLOW_PASSWORD = os.getenv("AIRFLOW_PASSWORD", "airflow")

def trigger_appointment_dag(appointment_id: int):
    response = requests.post(
        AIRFLOW_EMAIL_DAG_TRIGGER_URL,
        auth=(AIRFLOW_USERNAME, AIRFLOW_PASSWORD),
        json={"conf": {"appointment_id": appointment_id}},
        headers={"Content-Type": "application/json"},
        timeout=10
    )

    if response.status_code not in [200, 201]:
        raise RuntimeError(f"Failed to trigger DAG: {response.status_code} - {response.text}")

def trigger_test_upload_dag(lab_test_id: int):
    url = "http://localhost:8080/api/v1/dags/test_upload_notification/dagRuns"
    response = requests.post(
        url,
        auth=(AIRFLOW_USERNAME, AIRFLOW_PASSWORD),
        json={"conf": {"lab_test_id": lab_test_id}},
        headers={"Content-Type": "application/json"},
        timeout=10
    )
    if response.status_code not in [200, 201]:
        raise RuntimeError(f"Failed to trigger DAG: {response.status_code} - {response.text}")

def trigger_test_diagnosis_notification_dag(lab_test_id: int):
    url = "http://localhost:8080/api/v1/dags/test_diagnosis_notification/dagRuns"
    response = requests.post(
        url,
        auth=(AIRFLOW_USERNAME, AIRFLOW_PASSWORD),
        json={"conf": {"lab_test_id": lab_test_id}},
        headers={"Content-Type": "application/json"},
        timeout=10
    )
    if response.status_code not in [200, 201]:
        raise RuntimeError(f"Failed to trigger DAG: {response.status_code} - {response.text}")

