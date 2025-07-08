import dask.dataframe as dd
from io import BytesIO
from datetime import datetime
from google.cloud import bigquery as bq

def df_to_bq(bq_client, df, table_path:str, mode:str):
	if mode == 'a':
		write_disposition = 'WRITE_APPEND'
	elif mode == 't':
		write_disposition ="WRITE_TRUNCATE"
	else:
		raise ValueError(f"{mode} is not recognised. Use 'a' for append or 't' for truncate")

	try:
		job_config = bq.LoadJobConfig(write_disposition='WRITE_TRUNCATE', autodetect=True)
		job = bq_client.load_table_from_dataframe(df, table_path, job_config=job_config)
		job.result()
		return job
	except Exception:
		raise
