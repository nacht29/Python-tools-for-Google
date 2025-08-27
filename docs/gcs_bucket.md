# gcs_bucket.py

## file_to_bucket

1. Create a GCS Bucket Client using your service account key
2. You can now include the client in your function calls

#### **Definition:**
```py
def file_to_bucket(bucket_client, bucket_id:str, bucket_filepath:str, file_type:str, file_path:str, mode:str, log=False) -> None:
```

#### **Parameters:**
- `bucket_client`: Bucket client that you just created.
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
None
