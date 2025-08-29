from google.cloud import bigquery as bq

'''
Mandatory
'''

# content mimetype for Google Sheets ad GCP
content_data = {
	'.csv': {'content_type': 'text/csv', 'type_name': 'CSV'},
	'.txt': {'content_type': 'text/plain', 'type_name': 'Text'},
	'.xlsx': {'content_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'type_name': 'Excel'},
	'.log': {'content_type': 'text/plain', 'type_name': 'Log'}
}

# example of extra formats: BigQuery schema definition
school_terms_schema = [
	bq.SchemaField("id", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("finishDate", "DATETIME", mode="NULLABLE"),
	bq.SchemaField("name", "STRING", mode="NULLABLE"),
	bq.SchemaField("schoolYear", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("startDate", "DATETIME", mode="NULLABLE"),
]