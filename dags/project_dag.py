from airflow.decorators import dag, task
from datetime import datetime
from airflow.providers.sqlite.hooks.sqlite import SqliteHook
from airflow.providers.sqlite.operators.sqlite import SqliteOperator

import weather_service


@dag(
    dag_id='project_dag',
    schedule_interval="0 1 * * *",
    start_date=datetime(2023, 1, 11),
    catchup=False,
    tags=['example']
)
def project_dag():
    @task(multiple_outputs=True)
    def get_weather(lat: float, lng: float, ds=None) -> dict:
        res = weather_service.read_form_api(lat, lng, ds)
        return {"weather_data": res}

    @task(multiple_outputs=True)
    def process_weather_data(data: dict) -> dict:
        proc_data = weather_service.process_weather_data(data["weather_data"])
        return {"proc_weather_data": proc_data}

    @task
    def insert_with_hook(data: dict, ds=None) -> None:
        timestamp = datetime.strptime(ds, '%Y-%m-%d').isoformat()
        sqlite_hook = SqliteHook()
        rows, target_fields = weather_service.prepare_rows_and_fields(data["proc_weather_data"], timestamp)
        sqlite_hook.insert_rows(table='weather_data', rows=rows, target_fields=target_fields)

    @task
    def read_with_hook() -> None:
        sqlite_hook = SqliteHook()
        query = "SELECT * FROM weather_data;"
        rows = sqlite_hook.get_records(query)
        print(rows)

    @task
    def write_to_file(data: dict) -> None:
        weather_service.write_to_json_file(data)

    create_table = SqliteOperator(task_id="create_weather_table", sql="sql/create_table.sql")

    latitude = 52.52
    longitude = 13.41

    data = get_weather(latitude, longitude)
    processed_data = process_weather_data(data)
    processed_data >> create_table >> insert_with_hook(processed_data) >> read_with_hook()
    write_to_file(data)


_ = project_dag()
