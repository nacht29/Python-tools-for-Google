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
def file_to_bucket(storage_client, bucket_id:str, bucket_filepath:str, file_type:str, file_path:str, mode:str, log=False):
```

#### **Parameters:**
- `storage_client`: BigQuery API client created during [set up](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/gcs_bucket.md#set-up).
- `bucket_id`: Unique name (Id) of your Bucket.
- `bucket_filepath`: Path to the target directory in the Bucket. The file path is available for copy at the top.
- `file_type`: Type of file to upload.
- `mode`: 't' to truncate same-name files, 'i' to ignore and create a duplicate.
- `log`: Enable printing messages for logging.

#### **Function call:**
```py
file_to_bucket(
    bucket_client,
    bucket_id="my-first-bucket",
    bucket_filepath="folder1/folder2/folder3", # exclude gs://, file path avaliable for copy in Bucket
    file_type=".csv",
    mode="t",
    log=True
)
```

#### **Use case:**
Load local files to GCS Bucket

#### **Return value:**
No return value.
