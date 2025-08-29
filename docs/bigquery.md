<!-- <h1 style="text-align: center;"> -->
# bigquery.py
<!-- </h1> -->

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
def df_to_bq(bq_client, df:pd.DataFrame, table_id:str, mode:str, schema=None, autodetect:bool=True)
```

#### **Parameters:**
- `bq_client`: BigQuery client created during [set up](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/bigquery.md#set-up).
- `df`: The Pandas Dataframe containing the data to be uploaded to BigQuery.
- `table_id`: Id of the BigQuery for the data to be uploaded to. Usually in `project_id.dataset_name_table_name`.
- `schema`: Schema definition for the data to be uploaded. This hard-sets the data type of the uploaded data. See the expandable part in [function call](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/bigquery.md#function-call).
- `autodetect`: If `True`, automatically creates a new table if the current `table_id` doesn't exist.

#### **Function call:**

<details>
<summary>Expand to see how to define schema for BQ upload</summary>

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
df_to_bq(
	bq_client,
	df=my_df,
	table_id:str,
	mode:str,
	schema=schema,
	autodetect:bool=True
)
```

#### **Use case:**
Loads data from Python Pandas Dataframe to BigQuery.

#### **Return value:**
No return value.

---

## bq_to_df

#### **Definition:**
```py
def bq_to_df(bq_client, sql_script:str, replace_in_query:list=[], log=False, ignore_error=False):
```

#### **Parameters:**
- `bq_client`: BigQuery client created during [set up](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/bigquery.md#set-up).
- `sql_script`: File path to the SQL script to query data from BigQuery.
- `replace_in_query`: Search and replace parts in your SQL script. Best for repititive queries.
- `log`: Enable printing messages for logging.
- `ignore_error`: `True` to continue the extraction process even if error occurs. `False` otherwise.

#### **Function call:**
<details>
<summary>Example query (with parts to replace)</summary>

- Replace `cur_dept` with `"1%"`, `"2%"` etc. The function can then be called in a for loop to query for each department.
- Replace table_id `project_id.dataset.table` with `project_id.dataset.table01`. The dunction can be called in a for loop to query for table 01-05.

```sql
SELECT *
FROM `project_id.dataset.table`
WHERE
	BizDate = DATE_SUB(CURRENT_DATE('+08:00'), INTERVAL 1 DAY)
	AND dept like cur_dept
ORDER BY dept, Itemcode, Location
```

</details>

```py
bq_to_df(
	bq_client,
	sql_script="/home/project/sql_scripts/script.sql",
	replace_in_query=[(".table", ".table01"), ("cur_dept", "'1%'")],
	log=True,
	ignore_error=False
)
```

#### **Use case:**
Extract BigQuery query results into a Pandas Dataframe.

#### **Return value:**
Pandas Dataframe containing query results.

---

## df_to_csv_bin

#### **Definition:**
```py
def df_to_csv_bin(df:pd.DataFrame, slice_row:int, outfile_name:str, sep:str=',', log:bool=False, ignore_error:bool=False):
```

#### **Parameters:**
- `df`: The dataframe to be exported to binary CSV file.
- `slice_row`: Slice the data by every n rows. E.g. `slice_row = 10` from a dataframe containing 100 rows will produce 10 binary CSV files, each with 10 different rows of data. Accept values 0 to 1000000 (0 = no slicing).
- `sep`: The seperator for the binary CSV file. Uses comma `,` by default but can be changed to `|` or other symbols if the data contains commas.
- `outfile_name`: Name of the resulting binary CSV file.
- `log`: Enable printing messages for logging.
- `ignore_error`: `True` to continue the extraction process even if error occurs. `False` otherwise.

#### **Function call:**
```py
df_to_csv_bin(
	df=df,
	slice_row=100,
	outfile_name="sales.csv",
	sep='|', 
	log=True,
	ignore_error=False
)
```

#### **Use case:**
- Export Pandas Dataframe to binary CSV file.
- Best used when writing large query results into CSV files that does not need to be stored locally. 
- E.g. Exporting query results as CSV to Google Drive. This is used in conjunction with the [`bin_file_to_drive`](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/google_drive.md#bin_file_to_drive) function.

#### **Return value:**
List of tuples in the form of `[(file_name, file_buffer)]`.

---

## df_to_excel_bin

#### **Definition:**
```py
def df_to_excel_bin(df, slice_row:int, outfile_name:str, log=False, ignore_eror=False):
```

#### **Parameters:**
- `df`: The dataframe to be exported to binary Excel file.
- `slice_row`: Slice the data by every n rows. E.g. `slice_row = 10` from a dataframe containing 100 rows will produce 10 binary Excel files, each with 10 different rows of data. Accept values 0 to 1000000 (0 = no slicing).
- `outfile_name`: Name of the resulting binary Excel file.
- `log`: Enable printing messages for logging.
- `ignore_error`: `True` to continue the extraction process even if error occurs. `False` otherwise.

#### **Function call:**
```py
df_to_excel_bin(
	df=df,
	slice_row:int,
	outfile_name:str,
	log=False,
	ignore_eror=False
):
```

#### **Use case:**
- Export Pandas Dataframe to binary Excel file.
- Best used when writing large query results into binary Excel files that does not need to be stored locally. 
- E.g. Exporting query results as Excel to Google Drive. This is used in conjunction with the [`bin_file_to_drive`](https://github.com/nacht29/Python-tools-for-Google/blob/main/docs/google_drive.md#bin_file_to_drive) function.

#### **Return value:**
List of tuples in the form of `[(file_name, file_buffer)]`.

---

## df_to_csv
#### **Definition:**
```py
def df_to_csv(df: pd.DataFrame, slice_row: int, outfile_path: str, sep: str = ',', log: bool = False, ignore_error: bool = False):
```

#### **Parameters:**
- `df`: The dataframe to be exported to local CSV file.
- `slice_row`: Slice the data by every n rows. E.g. `slice_row = 10` from a dataframe containing 100 rows will produce 10 output files, each with 10 different rows of data. Accept values 0 to 1000000 (0 = no slicing).
- `sep`: The seperator for the CSV file. Uses comma `,` by default but can be changed to `|` or other symbols if the data contains commas.
- `outfile_name`: Name of the resulting CSV file.
- `log`: Enable printing messages for logging.
- `ignore_error`: `True` to continue the extraction process even if error occurs. `False` otherwise.

#### **Function call:**
```py
df_to_csv(
	df=df,
	slice_row=100,
	outfile_name="sales.csv",
	sep='|',
	log=True,
	ignore_error=False
)
```

#### **Use case:**
Export Pandas Dataframe data to a local CSV file.

#### **Return value:**
No return value.

---

## df_to_excel
#### **Definition:**
```py
def df_to_excel(df: pd.DataFrame, slice_row: int, outfile_path: str, log: bool = False, ignore_error: bool = False):
```

#### **Parameters:**
- `df`: The dataframe to be exported to local Excel file.
- `slice_row`: Slice the data by every n rows. E.g. `slice_row = 10` from a dataframe containing 100 rows will produce 10 output files, each with 10 different rows of data. Accept values 0 to 1000000 (0 = no slicing).
- `outfile_name`: Name of the resulting Excel file.
- `log`: Enable printing messages for logging.
- `ignore_error`: `True` to continue the extraction process even if error occurs. `False` otherwise.

#### **Function call:**
```py
df_to_excel(
	df,
	slice_row=100,
	outfile_name="sales.xlsx",
	log=True,
	ignore_error=False
)
```

#### **Use case:**
Export Pandas Dataframe data to a local Excel file.

#### **Return value:**
No return value.