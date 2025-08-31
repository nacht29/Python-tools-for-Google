# google_drive.py

## Set up

1. Add a service account to the target Google Drive an editor. 

2. Create a Google Drive API client service object using the service account key. This allows your Python script/programme to communicate with Google Drive.

```py
from python_utils.google_drive import build_drive_service

# define path service account key JSON file 
JSON_KEYS_PATH = '/home/directory-for-keys'
SERVICE_ACCOUNT = f'{JSON_KEYS_PATH}/key.json'

# create Drive service
service = build_drive_service(SERVICE_ACCOUNT)
```

3. Then, import the `Google_Drive` class and create a class for your target Google Drive folder.

- If you own the Drive:
```py
from python_utils.google_drive import Google_Drive

# create Class for target Drive
target_drive = Google_Drive(service, is_shared_drive=True)
```

- If the Drive is shared with you:
```py
from python_utils.google_drive import Google_Drive

# create Class for target Drive
target_drive = Google_Drive(service, is_shared_drive=True, main_drive_id="0ABcDeFgHiJkLmNoPqRsTuVwXyZ123456")
```

**Parameters:**
- `is_shared_drive`: `True` if the target Drive is a shared drive and `False` otherwise. This is because handling files in shared drives and owned drives is slightly different. 
- `main_drive_id`: The folder ID of your root direcotry in Google Drive.

4. Please refer to the [appendix](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/google_drive.md#appendix) for more information on Drive ID and Drive folder ID.

---

## **Methods**

## drive_autodetect_folders

#### **Definition:**
```py
def drive_autodetect_folders(self, parent_folder_id:str, folder_name:str, create_folder:bool, log:bool=False) -> list:
```

#### **Parameters:**
- `parent_folder_id`: The folder ID preceeding your target folder. E.g. you are searching/creating the for `folder1/folder2`, you need to provide the ID of `folder1/`. 
- `folder_name`: Name of the target folder you care seaching/creating.
- `create_folder`: `True` to create a folder with the name `folder_name` if the folder with `folder_name` isn't found in the parent folder.
- `log`: `True` to enable printing messages for logging. `False` otherwise.

#### **Method call:**
```py
folder_data = target_drive.drive_autodetect_folders(
	parent_folder_id="ID of folder preeceding target folder",
	folder_name="Name of target folder",
	create_folder=True, log=False
)
```

#### **Use case:**
- Search for folder by name in target Drive folder.
- If folder already exists, return found folder data.
- If folder does not exist
	- If `create_folder=True`, create a folder by the name `folder_name` and return created folder data.
	- Return an empty list if `create_folder=False`.
- `log`: `True` to enable printing messages for logging. `False` otherwise.

#### **Return value:**
- Type: List of tuples.
- Returns list containing folder data: `[folder_id, folder_name, last modified]` if folder is found or created.
- Returns an empty Python list if folder is not found and not created.

---

## drive_search_filename
#### **Definition:**
```py
def drive_search_filename(self, parent_folder_id: str, file_name:str) -> List[Tuple]:
```

#### **Parameters:**
- `parent_folder_id`: The folder ID preceeding your target folder. E.g. you are searching/creating the for `folder1/folder2`, you need to provide the ID of `folder1/`. 
- `file_name`: Name of the file to be searched in the Drive folder.

#### **Method call:**
```py
file_data = drive_search_filename(parent_folder_id="1ABCdEfGH2IJK-LMnOpQ3RSTuv4WXYZab", file_name="sample.csv")
```

#### **Use case:**
Search for files in Drive folder by file name.

#### **Return value:**
- Type: List of tuples.
- Returns a list of file data in the form of `[(file_id, file_name, last_modified)]`.

---

## local_file_to_drive

#### **Definition:**
```py
def local_file_to_drive(self, dst_folder_id:str, file_path:str, update_dup=True, log=False):
```

#### **Parameters:**
- `dst_folder_id`: The ID of the Drive folder to upload the files to. It can also be your root Drive folder.
- `file_path`: Path to the file to be uploaded.
- `update_dup`: `True` to truncate existing file with the same name in the target folder. `False` to ignore existing files and allow duplicate files.
- `log`: `True` to enable printing messages for logging. `False` otherwise.

#### **Method call:**
```py
target_drive.local_file_to_drive(
	dst_folder_id:"1ABCdEfGH2IJK-LMnOpQ3RSTuv4WXYZab",
	file_path:"/home/folder1/sample_file",
	update_dup=True,
	log=False
)
```

#### **Use case:**
Upload a file from local machine to Google Drive.

#### **Return value:**
No return value.

---

## bin_file_to_drive

#### **Definition:**

```py
def bin_file_to_drive(self, dst_folder_id:str, file_data:List[Tuple], update_dup=True, log=False):
```

#### **Parameters:**
- `dst_folder_id`: The ID of the Drive folder to upload the files to. It can also be your root Drive folder.
- `file_data`: List of `(file_name, file_buffer)` pair. Can be obtained from [`df_to_csv_bin`](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/bigquery.md#df_to_csv_bin) and [`df_to_excel_bin`](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/bigquery.md#df_to_excel_bin).
- `update_dup`: `True` to truncate existing file with the same name in the target folder. `False` to ignore existing files and allow duplicate files.
- `log`: `True` to enable printing messages for logging. `False` otherwise.

#### **Method call:**

#### **Use case:**
Upload a file from binary buffer to Google Drive. Recommended use in conjunction with [`df_to_csv_bin`](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/bigquery.md#df_to_csv_bin) and [`df_to_excel_bin`](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/bigquery.md#df_to_excel_bin).

#### **Return value:**
No return value.

---

## Appendix

### Drive ID

There are 2 formats of Drive Ids:

#### 1. **My Drive (owned Drive)**

##### **Introduction**
- Link format: `https://drive.google.com/drive/my-drive`.
- Example: Always "https://drive.google.com/drive/my-drive".
- This is the link to the landing page of your "My Drive" Google Drive. Note that I sometimes refer to this as the root folder.

##### **Parameters parsing:**
- You can ignore any parameters containing `drive_id` when working on My Drive.
- E.g. `main_drive_id` in [`drive_autodetect_folders`]().

#### 2. **Shared Drives**

##### **Introduction**
- Link format: `https://drive.google.com/drive/u/0/folders/DRIVE_ID`.
- Example: "https://drive.google.com/drive/u/0/folders/0ABcDeFgHiJkLmNoPqRsTuVwXyZ123456".
- This is the link to the landing page of your shared Google Drive(s). Note that I sometimes refer to this as the root folder.
- Usually contains `/u/0/` to indicate user domain.

##### **Parameters parsing:**
- You neeed to parse the `DRIVE_ID` part of the link, as a string, into parameters containing `drive_id`.
- In this case, the Drive ID is `0ABcDeFgHiJkLmNoPqRsTuVwXyZ123456`.
- E.g. `main_drive_id="0ABcDeFgHiJkLmNoPqRsTuVwXyZ123456"` (from [`drive_autodetect_folders`](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/google_drive.md#drive_autodetect_folders)).

---

### Folder ID
Each Drive folder is identified by a unique ID.

#### 1. **My Drive folders**
- Link format: `https://drive.google.com/drive/folders/FOLDER_ID`.
- Example: "https://drive.google.com/drive/folders/1ABCdEfGH2IJK-LMnOpQ3RSTuv4WXYZab".
- Folder IDs typically starts with `1` to indicate a folder in a personal Drive.

#### 2. **Shared Drive folders:**
- Link format: `https://drive.google.com/drive/u/0/folders/FOLDER_ID`.
- Example: "https://drive.google.com/drive/u/0/folders/0ABcDeFgHiJkLmNoPqRsTuVwXyZ123456".
- Folder IDs typically starts with `0` to indicate a folder in a personal Drive.
- Usually contains `/u/0/` to indicate user domain.

#### **Parameters and parsing:**
- You will always have to parse the `FOLDER_ID` part of the link, as a string, to any parameters containing `folder_id` regardless of if you are working on personal or shared drives.
- E.g. `parent_folder_id` from [`drive_autodetect_folders`](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/google_drive.md#drive_autodetect_folders) and `dst_folder_id` from [`local_file_to_drive`](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/google_drive.md#local_file_to_drive).