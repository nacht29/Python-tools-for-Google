# formats.py

## Introduction

This module contains one dictionary only:

```py
content_data = {
	'.csv': {'content_type': 'text/csv', 'type_name': 'CSV'},
	'.txt': {'content_type': 'text/plain', 'type_name': 'Text'},
	'.xlsx': {'content_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'type_name': 'Excel'},
	'.log': {'content_type': 'text/plain', 'type_name': 'Log'}
}
```

It stores the standardization of file extensions and their `MIME types` used in functions for the Google services this package is used for. Hence, it is important that you do not edit the contents in this dictionary.

---

## What other developers can do:

You are allowed to add definitions here, e.g. BigQuery schema definitions, and import this module into your code. This serves as a way of standardizing your definitions in one place.

In `formats.py`:

```py
from google.cloud import bigquery as bq

# example of extra formats: BigQuery schema definition
school_terms_schema = [
	bq.SchemaField("id", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("finishDate", "DATETIME", mode="NULLABLE"),
	bq.SchemaField("name", "STRING", mode="NULLABLE"),
	bq.SchemaField("schoolYear", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("startDate", "DATETIME", mode="NULLABLE"),
]
```

In another `.py` file:

```py
from python_utils.formats import school_terms_schema
from python_utils.bigqiery import df_to_bq

df_to_bq(
	bq_client,
	df=my_df,
	table_id:"my_project.school_info.school_terms",
	mode:"'t,
	schema=school_terms_schama,
	autodetect:bool=True
)
```

