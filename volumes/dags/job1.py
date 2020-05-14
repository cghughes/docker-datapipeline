# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to operate!
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from _datetime import timedelta
from airflow.operators.papermill_operator import PapermillOperator
from airflow.operators.python_operator import PythonOperator
import time, datetime, os

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['jobs@cgh.dev'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=1),
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
    'notebooks',
    default_args=default_args,
    description='Notebook Pipeline',
    schedule_interval=None,
    params={
        "base_directory": "/opt/airflow/dags/notebooks/",
        "output_directory": "/opt/airflow/dags/notebooks/output/"
    }
)

def initDag(**context):
    print("DAG Started")
    
    today = datetime.datetime.today()
    output_directory = dag.params['base_directory'] + "output/" + str(context["execution_date"]) + "/"
    dag.params['output_directory'] = output_directory
    os.mkdir(output_directory)
    print("Creating output directory to " + output_directory)

t1 = PythonOperator(
    task_id = 'init',
    python_callable=initDag,
    provide_context=True,
    dag=dag,
)

t2 = PapermillOperator(
    task_id='notebook01',
    depends_on_past=True,
    input_nb=dag.params['base_directory'] + "Notebook01.ipynb",
    output_nb= dag.params['base_directory'] + "output/{{ execution_date }}/" + "Notebook01.ipynb",
    parameters="",
    dag=dag,
)

t3 = PapermillOperator(
    task_id='notebook02',
    depends_on_past=True,
    input_nb=dag.params['base_directory'] + "Notebook02.ipynb",
    output_nb= dag.params['base_directory'] + "output/{{ execution_date }}/" + "Notebook02.ipynb",
    parameters="",
    dag=dag,
)

dag.doc_md = __doc__

t1.set_downstream(t2)
t2.set_downstream(t3)
#t3.set_upstream([t1,t2])
#t1.set_downstream([t2, t3])
