from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta, datetime

with DAG(
    "jinja_templating"
    , default_args={
      "depends_on_past": True
      ,"retries": 1
      ,"retry_delay": timedelta(seconds = 10)
    }
    ,schedule_interval = None #"* * * * *"
    ,start_date = datetime(2022, 8, 20)
    ,catchup = False
) as dag:

    def func(*args, **kwargs):
        print(args)
        print(kwargs["key"])
        print(kwargs["templates_dict"]["ds"])
        print(kwargs["templates_dict"]["query"])

    t1 = PythonOperator(
        task_id = "func"
        , python_callable = func
        , op_kwargs = {
            "key": "hello world"
        }
        , op_args = [1, "foo", "bar"]
        , templates_dict = {
            "ds": "{{ ds }}"
            , "query": "./sql/query.sql"
        }
        , templates_exts = [".sql"]
        , show_return_value_in_logs = False
    )

    t1