# from kubernetes.client import models as k8s

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.utils.dates import days_ago


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    # "retry_delay": timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

dag = DAG(
    "example_kubernetes_operator",
    default_args=default_args,
    description="A kubernetes operator DAG",
    start_date=days_ago(2),
    tags=["example", "kubernetes"],
)


# with DAG(
#     dag_id="example_kubernetes_operator",
#     default_args=default_args,
#     schedule_interval=None,
#     start_date=days_ago(2),
#     tags=["example", "kubernetes_pod_operator"],
# ) as dag:
k = KubernetesPodOperator(
    in_cluster=True,
    # config_file="/opt/airflow/dags/kube-config",
    namespace="default",
    image="busybox",
    arguments=["echo", "hello"],
    name="airflow_k8s_pod_operator",
    is_delete_operator_pod=False,
    # ports=[port],
    hostnetwork=False,
    task_id="pod_op",
    dag=dag,
)

t = BashOperator(bash_command='echo "ended"', task_id="final", dag=dag)

k >> t