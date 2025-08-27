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
5. Feel free to expand the `python_utils` folder with your custom modules that is needed for any projects
---

### Modules

#### **[bigquery.py](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/bigquery.md)**
- Functions for working with BigQuery

#### **[google_drive.py](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/google_drive.md)**
- Class and methods for working with Google Drive

#### **[gcs_bucket.py](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/google_drive.md)**
- Functions for working with Google Cloud Storage Bucket

#### **[api.py](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/api.md)**
- Functions for working with APIs 

#### **[utils.py](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/utils.md)**
- Utility functions
