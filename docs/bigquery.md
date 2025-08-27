# bigquery.py

## Set up
1. Create a BigQuery client using your service account key
2. You can now include the client in your function calls

```py
from google.cloud import bigquery as bq
from google.oauth2 import service_account

JSON_KEYS_PATH = '/home/directory-for-keys'
SERVICE_ACCOUNT = f'{JSON_KEYS_PATH}/key.json'

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT)
bq_client = bq.Client(credentials=credentials, project=credentials.project_id)
service = build_drive_service(SERVICE_ACCOUNT)
```

---

## df_to_bq

#### **Definition:**
```py
def df_to_bq(bq_client, df:pd.DataFrame, table_id:str, mode:str, schema=None,autodetect:bool=True)
```

#### **Parameters:**
- ``

#### **Function call:**

<details>
<summary>Expand to see how to define schema for BQ upload</summary>

```py
from google.cloud import bigquery as bq

schema = [
    bq.SchemaField("primary_column_name", "INTEGER", mode="REQUIRED"),
    bq.SchemaField("column2", "STRING", mode="NULLABLE"),
    bq.SchemaField("column3", "BOOLEAN", mode="NULLABLE")
]
```

</details>

```py
df_to_bq(
    bq_client,
    df=my_df,
    table_id:str,
    mode:str,
    schema=schema,
    autodetect:bool=True
)
```

**Use case:**
Loads data from Python Pandas Dataframe to BigQuery.

**Return value:**
None

---

