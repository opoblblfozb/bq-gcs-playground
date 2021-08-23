## bigquery
## リソースの作成は， dataset(node)→table→rowの順
# %%
from google.cloud import bigquery

# %%
########## datasetの作成
# Construct a BigQuery client object. 
client = bigquery.Client()

# TODO(developer): Set dataset_id to the ID of the dataset to create.
dataset_id = "{}.nonaka_sample".format(client.project)

# Construct a full Dataset object to send to the API.
dataset = bigquery.Dataset(dataset_id)

# TODO(developer): Specify the geographic location where the dataset should reside.
dataset.location = "US"

# Send the dataset to the API for creation, with an explicit timeout.
# Raises google.api_core.exceptions.Conflict if the Dataset already
# exists within the project.
dataset = client.create_dataset(dataset, timeout=30)  # Make an API request.
print("Created dataset {}.{}".format(client.project, dataset.dataset_id))

# %%
########## tableの作成
# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to create.
table_id = "{}.nonaka_sample.sample_table".format(client.project)

schema = [
    bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
]

table = bigquery.Table(table_id, schema=schema)
table = client.create_table(table)  # Make an API request.
print(
    "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
)


########## 以下rowの作成
# %%
client = bigquery.Client()

query_job = client.query(
    """
    INSERT INTO
        `data-intelligence-216907.nonaka_sample.sample_table`
        (full_name, age)
    VALUES
        ('nonakakenya', 25),
        ('hogehoge', 99),
        ('bigquery-man', 100)
    """
)

results = query_job.result()

# %%
### formatを使って

client = bigquery.Client()
tablename = "{}.nonaka_sample.sample_table".format(client.project)

query_job = client.query(
    """
    INSERT INTO
        `{}`
        (full_name, age)
    VALUES
        ('{}', {})
    """.format(tablename, "nonakakenya2", 25)
)

results = query_job.result()
# %%
