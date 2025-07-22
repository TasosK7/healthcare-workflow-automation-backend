import requests
import os

# AIRFLOW_APPOINTMENT_EMAIL_DAG_TRIGGER_URL = os.getenv("AIRFLOW_APPOINTMENT_EMAIL_DAG_TRIGGER_URL", "http://localhost:8080/api/v1/dags/appointment_email_flow/dagRuns")
# AIRFLOW_TEST_UPLOAD_EMAIL_DAG_TRIGGER_URL = os.getenv("AIRFLOW_TEST_UPLOAD_EMAIL_DAG_TRIGGER_URL", "http://localhost:8080/api/v1/dags/test_upload_notification/dagRuns")
# AIRFLOW_DIAGNOSIS_EMAIL_DAG_TRIGGER_URL = os.getenv("AIRFLOW_DIAGNOSIS_EMAIL_DAG_TRIGGER_URL", "http://localhost:8080/api/v1/dags/diagnosis_notification/dagRuns")
AIRFLOW_API_BASE = os.getenv("AIRFLOW_API_BASE", "http://localhost:8080/api/v1/dags")

DAG_TRIGGER_ENDPOINTS = {
    "appointment": "appointment_email_flow",
    "lab_upload": "test_upload_notification",
    "diagnosis": "diagnosis_notification",
    "appointment_approval": "appointment_approval_notification"
}

AIRFLOW_USERNAME = os.getenv("AIRFLOW_USERNAME", "airflow")
AIRFLOW_PASSWORD = os.getenv("AIRFLOW_PASSWORD", "airflow")

def trigger_dag(dag_key: str, conf: dict):
    dag_id = DAG_TRIGGER_ENDPOINTS.get(dag_key)
    if not dag_id:
        raise ValueError(f"No DAG found for key '{dag_key}'")

    url = f"{AIRFLOW_API_BASE}/{dag_id}/dagRuns"

    response = requests.post(
        url,
        auth=(AIRFLOW_USERNAME, AIRFLOW_PASSWORD),
        json={"conf": conf},
        headers={"Content-Type": "application/json"},
        timeout=10
    )

    if response.status_code not in [200, 201]:
        raise RuntimeError(f"Failed to trigger DAG '{dag_id}': {response.status_code} - {response.text}")

def trigger_appointment_dag(appointment_id: int):
    trigger_dag("appointment", {"appointment_id": appointment_id})

def trigger_appointment_approval_dag(appointment_id: int):
    trigger_dag("appointment_approval", {"appointment_id": appointment_id})

def trigger_test_upload_dag(lab_test_id: int):
    trigger_dag("lab_upload", {"lab_test_id": lab_test_id})

def trigger_test_diagnosis_notification_dag(lab_test_id: int):
    trigger_dag("diagnosis", {"lab_test_id": lab_test_id})

