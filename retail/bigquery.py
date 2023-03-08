from google.cloud import bigquery


from dotenv import load_dotenv
import os

load_dotenv()


DATASET = f"{os.getenv('PROJECT_ID')}.online-retail-uci"

client = bigquery.Client()


def create_dataset(dataset_id):
    dataset_ref = bigquery.DatasetReference.from_string(
        dataset_id, default_project=client.project)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "US"
    dataset = client.create_dataset(dataset)
    print("Created dataset {}.{}".format(client.project, dataset.dataset_id))


create_dataset(dataset_id=DATASET)


def create_table():
    table_id = f"{DATASET}.customers"
    schema = [
        bigquery.SchemaField("first_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("last_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("dob", "STRING"),
        bigquery.SchemaField("title", "STRING"),
        bigquery.SchemaField("age", "INTEGER"),
    ]
    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)
    print("Created table {}.{}.{}".format(table.project, table.dataset_id,
                                          table.table_id))
