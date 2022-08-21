from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta, datetime

with DAG(
    "python_operators"
    , default_args={
      "depends_on_past": True
      ,"retries": 1
      ,"retry_delay": timedelta(seconds = 10)
    }
    ,schedule_interval = None #"* * * * *"
    ,start_date = datetime(2022, 8, 20)
    ,catchup = False
) as dag:

    # Function that the PythonOperator runs
    def func(*args, **kwargs):
        print(f"Positional arguments: {args}")
        print(f"Keyword arguments message: {kwargs['message']}")
        print(f"Jinja-templated argument ds: {kwargs['templates_dict']['ds']}")
        print(f"Jinja-templated file contents query: {kwargs['templates_dict']['query']}")
        print(f"Default tempalte variables passed in automatically:")
        ls = ["data_interval_start", "data_interval_end" , "ds", "ts"]
        for k in ls:
            print(f"    {k} = {kwargs[k]}")

    # Create a PythonOperator task
    t1 = PythonOperator(
        # unique identifier of the task
        task_id = "func"
        
        # function to run
        , python_callable = func

        # dictionary is passed in as kwargs in function
        , op_kwargs = {
            "message": "hello world"
        }

        # positional arguments is passed in as args
        , op_args = [1, "foo", "bar"]

        , templates_dict = {
            # pass in jinja-templated values
            "ds": "{{ ds }}"

            # pass in jinja-templated files
            , "query": "./sql/query.sql"
        }

        # specify that .sql files are jinja-templated
        , templates_exts = [".sql"]

        # don't show return
        , show_return_value_in_logs = False
    )

    t1