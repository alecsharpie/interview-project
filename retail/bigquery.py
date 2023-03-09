from google.cloud import bigquery
from google.cloud.bigquery import SchemaField

class BigQuery:

    def __init__(self, project_id, dataset_id):
        """Initialize a BigQuery client and create a dataset if it doesn't exist"""
        self.client = bigquery.Client()
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.dataset_list = [
            f"{self.project_id}.{dataset.dataset_id}"
            for dataset in self.client.list_datasets()
        ]
        print('Dataset list:')
        print(self.dataset_list)
        if f"{self.project_id}.{self.dataset_id}" not in self.dataset_list:
            self.create_dataset()

        self.tables = [
            f"{table.project}.{table.dataset_id}.{table.table_id}"
            for table in self.client.list_tables(self.dataset_id)
            ]
        print('Table list:')
        print(self.tables)


    def create_dataset(self):
        """Create a new dataset in the specified project."""
        dataset_ref = bigquery.DatasetReference.from_string(
            f"{self.project_id}.{self.dataset_id}",
            default_project=self.client.project)
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "asia-east1"
        dataset = self.client.create_dataset(dataset)
        self.dataset_list.append(f"{self.project_id}.{dataset.dataset_id}")
        print(f"Created dataset {self.client.project}.{dataset.dataset_id}")

    def create_table(self, table_name, schema, clustered_columns = None):
        """Create a new table in the specified dataset.
        schema is a list of dictionaries with the following keys:
        name, type, mode"""
        table_id = f"{self.project_id}.{self.dataset_id}.{table_name}"
        print('table: ', table_id)
        print('tables: ', self.tables)
        if table_id not in self.tables:
            column_schema = [SchemaField(field['name'], field['type'], field['mode']) for field in schema['columns']]
            table = bigquery.Table(table_id, schema=column_schema)
            if clustered_columns:
                table.clustering_fields = clustered_columns
            table = self.client.create_table(table)
            self.tables.append(table_id)
            print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")

            self._add_primary_key(table_name, schema['primary_key'])
            for fk in schema['foreign_keys']:
                self._add_foreign_key(table_name,
                                    foreign_key = fk['column'],
                                    pk_table_id = f"{self.project_id}.{self.dataset_id}.{fk['references']}",
                                    ref_primary_key =  fk['ref_column'])

        else:
            print(f"Table {table_name} already exists")

    def _add_primary_key(self, table_name, primary_key):
        """Add a primary key to a table."""
        table_id = f"{self.project_id}.{self.dataset_id}.{table_name}"
        query = f"""
            ALTER TABLE {table_id}
            ADD PRIMARY KEY ({primary_key}) NOT ENFORCED;
        """
        job = self.client.query(query)
        job.result()

    def _add_foreign_key(self, table_name, foreign_key, pk_table_id, ref_primary_key):
        """Add a foreign key to a table."""
        table_id = f"{self.project_id}.{self.dataset_id}.{table_name}"
        query = f"""
            ALTER TABLE {table_id}
            ADD CONSTRAINT fk_{foreign_key} FOREIGN KEY ({foreign_key})
            REFERENCES {pk_table_id}({ref_primary_key}) NOT ENFORCED;
        """
        job = self.client.query(query)
        job.result()

    def create_view(self, view_name, query):
        """Create a view from a query."""
        view_id = f"{self.project_id}.{self.dataset_id}.{view_name}"
        view = bigquery.Table(view_id)
        view.view_query = query
        view = self.client.create_table(view)
        print(f"Created view {view.project}.{view.dataset_id}.{view.table_id}")

    def insert_data(self, table_name, data):
        """Insert data into a table."""
        table_id = f"{self.project_id}.{self.dataset_id}.{table_name}"
        errors = self.client.insert_rows_json(table_id, data)
        if len(errors) > 0:
            print(f"Errors while loading data into {table_id}: {errors}")
