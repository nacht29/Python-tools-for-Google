# google_drive.py

## Set up

1. Create a Google Drive Service.
2. Create a class for the Google Drive that you are working on.
3. Parameters:
    - `is_shared_drive`: `True` if the target Drive is a shared drive and `False` otherwise. This is because handling files in shared drives and owned drives is slightly different. 
    - `main_drive_id`: The folder Id of your root direcotry in Google Drive. Folder Ids are the last part of the link to a Drive Folder (after the '/'). Ignore if the Drive is not a shared drive.

```py
from python_utils.google_drive import build_drive_service

# create Drive service
service = build_drive_service("Path to your service account JSON key file")

# create Class for target Drive
target_drive = Google_Drive(service, is_shared_drive=True, main_drive_id="YEWFHWEII01XIO")
```

---

### Methods

#### **Definition:**
```py
def drive_autodetect_folders(self, parent_folder_id:str, folder_name:str, create_folder:bool, log:bool=False) -> list:
```

#### **Method call:**
```py
target_drive.drive_autodetect_folders(
    parent_folder_id="Id of folder preeceding target folder",
    folder_name="Name of target folder",
    create_folder=True, log=False
)
```

#### **Use case:**
- Search for folder by name in target Drive folder
- If folder already exists, return found folder data
- If folder does not exist
	- If `create_folder=True`, create a folder by the name `folder_name` and return created folder data
	- Return an empty list if `create_folder=False`
- `log=True` to enable status and error output for logging, otherwise `log=False`

#### **Return value:**
- Type: Python List
- Returns `[folder_id, folder_name, last modified]` as folder data if folder is found or created
- Returns an empty Python list if folder is not found and not created
