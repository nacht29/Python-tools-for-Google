# Python-tools-for-Google
Building a Python package for working with Google Services, including GCP and Google Drive

## Set up
1. Install the Python package as a local directory
2. Copy the package to your current working directory
3. Append the package to your path
	```
	sys.path.append("/mnt/c/Users/Asus/Desktop/cloud-space-workspace/Taylors/taylors-data-poc")
	```
4. Import the functions into your code
	```py
	from python_utils.bigquery import *
	from python_utils.utils import *
	```
---

## bigquery.py

### df_to_bq

#### **Header:**
```py
df_to_bq(bq_client, df:pd.DataFrame, table_id:str, mode:str, schema=None,autodetect:bool=True)
```

#### **Use case:**
Loads data from Python Pandas Dataframe to BigQuery.

#### **Return value:**
None

---

## gcs_bucket.py

### file_to_bucket

#### **Header:**
```py
def file_to_bucket(bucket_client, bucket_id:str, bucket_filepath:str, file_type:str, file_path:str, mode:str, log=False) -> None:
```

#### **Use case:**
Load local files to GCS Bucket

#### **Return value:**
None

---


## google_drive.py

### How to use

1. Create a Google Drive Service.
2. Create a class for the Google Drive that you are working on.

```py
from python_utils.google_drive import build_drive_service

# create Drive service
service = build_drive_service("Path to your service account JSON key file")

# create Class for target Drive
target_drive = Google_Drive(service, is_shared_drive=True, main_drive_id="Id of the root Drive folder")
```

---

### drive_autodetect_folders

#### **Header:**
```py
def drive_autodetect_folders(self, parent_folder_id:str, folder_name:str, create_folder:bool, log:bool=False) -> list:
```

#### **Syntax:**
```py
target_drive.drive_autodetect_folders(parent_folder_id:str, folder_name:str, create_folder:bool, log:bool=False)
```

#### **Use case:**
- Search for folder by name in target Drive folder
- If folder already exists, return found folder data
- If folder does not exist
	- If `create_folder=True`, create a folder by the name `folder_name` and return created folder data
	- Return an empty list if `create_folder=False`

#### **Return value:**
- Type: Python List
- Returns `[folder_id, folder_name, last modified]` as folder data if folder is found or created
- Returns an empty Python list if folder is not found and not created

---