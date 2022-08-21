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
        print(f"Positional arguments: {args}")
        print(f"Keyword arguments message: {kwargs['message']}")
        print(f"Jinja-templated argument ds: {kwargs['templates_dict']['ds']}")
        print(f"Jinja-templated file contents query: {kwargs['templates_dict']['query']}")
        print(f"Default tempalte variables passed in automatically:")
        ls = ["data_interval_start", "data_interval_end" , "ds", "ts"]
        for k in ls:
            print(f"    {k} = {kwargs[k]}")

    t1 = PythonOperator(
        task_id = "func"
        , python_callable = func
        , op_kwargs = {
            "message": "hello world"
        }
        , op_args = [1, "foo", "bar"]

        # templates_dict is marked as templated in documentation.
        # This means Jinja templating can be used with this parameter.
        , templates_dict = {
            # pass in jinja-templated values
            "ds": "{{ ds }}"

            # pass in jinja-templated files
            , "query": "./sql/query.sql"
        }

        # specify that .sql files are jinja-templated
        , templates_exts = [".sql"]
        , show_return_value_in_logs = False
    )

    t1