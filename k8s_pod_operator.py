from kubernetes.client import models as k8s

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)
from airflow.utils.dates import days_ago


default_args = {
    "owner": "airflow",
}


port = k8s.V1ContainerPort(name="http", container_port=80)

with DAG(
    dag_id="example_kubernetes_operator",
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(2),
    tags=["example", "kubernetes_pod_operator"],
) as dag:
    k = KubernetesPodOperator(
        in_cluster=True,
        # config_file="/opt/airflow/dags/kube-config",
        namespace="airflow",
        image="busybox",
        arguments=["echo", "hello"],
        name="airflow_k8s_pod_operator",
        is_delete_operator_pod=False,
        # ports=[port],
        # hostnetwork=False,
        task_id="pod_op",
        get_logs=True,
    )

    t = BashOperator(bash_command='echo "ended"', task_id="final")

    k >> t