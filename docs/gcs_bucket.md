# gcs_bucket.py

## Set up
1. Create a BigQuery API client object using your service account key. The API client allows your Python script/programme to communicate with BigQuery.

2. Create a Google Cloud Storage API client object using your service account key. The API client allows your Python script/programme to communicate with Cloud Storage and interact with Storage Buckets and Bucket objects.

3. You can now include the API client object in your function calls.

```py
from google.cloud import storage
from google.cloud import bigquery as bq
from google.oauth2 import service_account

JSON_KEYS_PATH = '/home/directory-for-keys'
SERVICE_ACCOUNT = f'{JSON_KEYS_PATH}/key.json'

# retrieve account credentials and project id from the service account key
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT)

# build BigQuery API client
bq_client = bq.Client(credentials=credentials, project=credentials.project_id)

# build BigQuery API client
storage_client = storage.Client(credentials=credentials, project=credentials.project_id)
```

---

## file_to_bucket

#### **Definition:**
```py
def file_to_bucket(storage_client, bucket_id:str, bucket_dir_path:str, file_type:str, file_path:str, mode:str, log=False):
```

#### **Parameters:**
- `storage_client`: BigQuery API client created during [set up](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/gcs_bucket.md#set-up).
- `bucket_id`: Unique name (Id) of your Bucket.
- `bucket_dir_path`: Path to the target directory in the Bucket. The file path is available for copy at the top.
- `file_type`: Type of file to upload.
- `mode`: 't' to truncate same-name files, 'i' to ignore and create a duplicate.
- `log`: Enable printing messages for logging.

#### **Function call:**
```py
file_to_bucket(
	bucket_client,
	bucket_id="my-first-bucket",
	bucket_dir_path="folder1/folder2/folder3", # exclude gs://, file path avaliable for copy in Bucket
	file_type=".csv",
	mode="t",
	log=True
)
```

#### **Use case:**
Load local files to GCS Bucket

#### **Return value:**
No return value.

---

## bin_file_to_bucket

#### **Definition:**
```py
def bin_file_to_bucket(storage_client, bucket_id:str, bucket_dir_path:str, file_data:List[Tuple], mode:str, log=False):
```

#### **Parameters:**
- `storage_client`: BigQuery API client created during [set up](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/gcs_bucket.md#set-up).
- `bucket_id`: Unique name (Id) of your Bucket.
- `bucket_dir_path`: Path to the target directory in the Bucket. The file path is available for copy at the top.
- `file_data`: List of file name and file buffer pair: `[(file_name, file_buffer)]`, can be obtained from [`df_to_csv_bin`](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/bigquery.md#df_to_csv_bin) and [`df_to_excel_bin`](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/bigquery.md#df_to_excel_bin).
- `mode`: 't' to truncate same-name files, 'i' to ignore and create a duplicate.
- `log`: Enable printing messages for logging.

#### **Function call:**
```py
# example value: [(1.csv, csv_buffer1), (2.csv, csv_buffer2)]
csv_bin_files = df_to_csv_bin(
	df=df,
	slice_row=100,
	outfile_name="sales.csv",
	sep='|', 
	log=True,
	ignore_error=False
)

bin_file_to_bucket(
	storage_client,
	bucket_id:"my_bucket",
	bucket_dir_path:"folder1/folder2",
	file_data:csv_bin_files,
	mode:'t',
	log=True
)
```

#### **Use case:**
Upload files from memory (binary buffers) to GCS Bucket.

#### **Return value:**
No return value.

---

## bucket_csv_to_bq

#### **Definition:**
```py
def bucket_csv_to_bq(bq_client, bucket_dir_path:str, project_id:str, dataset_id:str, table_id:str, write_mode:str, skip_leading_rows:int=1, schema:Optional[List[bq.SchemaField]]=None, log:bool=False) -> None:
```

#### **Parameters:**
- `bq_client` BigQuery API client object. Please refer to the [set up](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/gcs_bucket.md#set-up) section and BigQuery related functions in [bigquery.md](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/bigquery.md) for more information.
- `bucket_filepath`: Path to the target CSV file in the Bucket.
- `project_id`: Project ID for the target table.
- `dataset_id`: Name of the dataset that stores the target table.
- `table_id`: Name of the target table. This combined with `project_id` and `dataset_id` will form the complete BigQuery table ID, in the form of `project_id.dataset.table`.
- `write_mode`: `'a'` to append to table and `'t'` to truncate the table during data loading.
- `skip_leading_row`: `1` to skip the first row of the CSV file which is usually the header. `0` to include the header as well (not recommended).
- `schema`: Schema definition for the data to be uploaded. This hard-sets the data type of the uploaded data. See the expandable part in [function call](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/gcs_bucket.md#function-call-2) on how to define a BigQuery schema in Python code.
- `log`: `True` to enable printing messages for logging. `False` otherwise.

#### **Function call:**

<details>
<summary>Expand to see how to define schema for BigQuery upload</summary>

Note: you can store the schema definitions in [formats.py](https://github.com/nacht29/Python-tools-for-Google/blob/main/python_utils/formats.py). See documentation [here](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/formats.md).

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
bucket_csv_to_bq(
	bq_client,
	bucket_filepath:"folder1/folder2/sample.csv",
	project_id:"my_project",
	dataset_id:"dataset1",
	table_id:"master_tab1e",
	write_mode:'t',
	skip_leading_rows=1,
	schema=schema,
	log=False
)
```

#### **Use case:**
Uploads data from CSV files in Google Cloud Storage Bucket to BigQuery.

#### **Return value:**
No return value.

---

## bucket_excel_to_bq

#### **Definition:**
```py
def bucket_excel_to_bq(bq_client, bucket_filepath:str, project_id:str, dataset_id:str, table_id:str, write_mode:str, schema:Optional[List[bq.SchemaField]]=None, log:bool=False) -> None:
```

#### **Parameters:**
- `bq_client` BigQuery API client object. Please refer to the [set up](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/gcs_bucket.md#set-up) section and BigQuery related functions in [bigquery.md](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/bigquery.md) for more information.
- `bucket_filepath`: Path to the target Excel file in the Bucket.
- `project_id`: Project ID for the target table.
- `dataset_id`: Name of the dataset that stores the target table.
- `table_id`: Name of the target table. This combined with `project_id` and `dataset_id` will form the complete BigQuery table ID, in the form of `project_id.dataset.table`.
- `write_mode`: `'a'` to append to table and `'t'` to truncate the table during data loading.
- `schema`: Schema definition for the data to be uploaded. This hard-sets the data type of the uploaded data. See the expandable part in [function call](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/gcs_bucket.md#function-call-2) on how to define a BigQuery schema in Python code.
- `log`: `True` to enable printing messages for logging. `False` otherwise.

#### **Function call:**
```py
bucket_excel_to_bq(
	bq_client,
	bucket_filepath:"folder1/folder2/sample.xlsx",
	project_id:"my_project",
	dataset_id:"dataset1",
	table_id:"master_tab1e",
	write_mode:'t',
	schema=schema,
	log=False
)
```

#### **Use case:**
Uploads data from Excel files in Google Cloud Storage Bucket to BigQuery.

#### **Return value:**
No return value.
