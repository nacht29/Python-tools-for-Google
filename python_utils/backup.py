import pandas as pd
from io import BytesIO
from datetime import datetime
from google.cloud import bigquery as bq

def bq_to_csv(bq_client,
			  sql_script:str,
			  slice_row:int,
			  outfile_name:str,
			  replace_in_query:list=[],
			  sep:str=',',
			  encoding:str='utf-8',
			  index:bool=False,
			  header:bool=True,
			  log:bool=False,
			  ignore_error:bool=False
) -> tuple:

	if not 0 < slice_row <= 1000000:
		raise ValueError('Invalid slice length.')

	results_df = bq_to_df(bq_client, sql_script, replace_in_query, log, ignore_error)
	csv_buffers = []

	if slice_row == 0:
		try:
			if log:
				print(f'{datetime.now()} creating CSV binary file for {outfile_name}')
			
			file_buffer = BytesIO()
			results_df.to_csv(
				path_or_buf=file_buffer, 
				sep=sep,
				encoding=encoding,
				index=index, 
				header=header
			)
			file_buffer.seek(0)
			csv_buffers.append((outfile_name, file_buffer))

			if log:
				print(f'{datetime.now()} {outfile_name} CSV binary created')

		except Exception as error:
			print(f"Failed to create CSV binary file for {outfile_name}.\n\n{error}")
			if not ignore_error:
				raise

	else:
		for cur_row in range(0, len(results_df), slice_row):
			try:
				file_ver = cur_row // slice_row + 1
				subset_df = results_df.iloc[cur_row:cur_row + slice_row]
				new_outfile_name = outfile_name.replace('.csv', f'_{file_ver}.csv')

				if log:
					print(f'{datetime.now()} creating CSV binary file for {new_outfile_name}')

				cur_buffer = BytesIO()
				subset_df.to_csv(
					path_or_buf=cur_buffer, 
					sep=sep,
					encoding=encoding,
					index=index, 
					header=header
				)
				cur_buffer.seek(0)
				csv_buffers.append((new_outfile_name, cur_buffer))

				if log:
					print(f'{datetime.now()} {new_outfile_name} CSV binary created')

			except Exception as error:
				print(f"Error creating {new_outfile_name}.\n\n{error}")
				if not ignore_error:
					raise

	return csv_buffers
