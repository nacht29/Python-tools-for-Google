import os
import pandas as pd
from io import BytesIO
from datetime import datetime
from google.cloud import bigquery as bq
from typing import List, Tuple

# ===============
# = local to BQ = 
# ===============

# load Pandas Dataframe data to BigQuery
def df_to_bq(bq_client, df:pd.DataFrame, table_id:str, mode:str, schema=None, autodetect:bool=True):
	if mode == 'a':
		write_disposition = 'WRITE_APPEND'
	elif mode == 't':
		write_disposition ="WRITE_TRUNCATE"
	else:
		raise ValueError(f"{mode} is not recognised. Use 'a' for append or 't' for truncate")

	try:
		job_config = bq.LoadJobConfig(schema=schema, write_disposition=write_disposition, autodetect=autodetect)
		job = bq_client.load_table_from_dataframe(df, table_id, job_config=job_config)
		job.result()
		return job
	except Exception:
		raise

# ===============
# = BQ to local = 
# ===============

# extract BQ query data to Pandas DF
def bq_to_df(bq_client, sql_script:str, replace_in_query:list=[], log=False, ignore_error=False) -> pd.DataFrame:
	with open(sql_script, 'r') as cur_script:
		if log:
			print(f'\n\n{datetime.now()} Query: {sql_script}')

		try:
			query = ' '.join([line for line in cur_script])
			for find, replace in replace_in_query:
				query = query.replace(find, replace)
			results_df = bq_client.query(query).to_dataframe()
		except Exception:
			print(f'{sql_script} query failed.')
			if ignore_error:
				results_df = pd.DataFrame() 
				return results_df
			raise

		if log:
			print(f'Results: {results_df.shape}')

	return (results_df)

# export DF as CSV file
def df_to_csv(df:pd.DataFrame, slice_row:int, outfile_path:str, sep:str=',', dlt_dir:bool=False, log:bool=False, ignore_error:bool=False):
	if not 0 < slice_row <= 1000000:
		raise ValueError('Invalid slice length.')
	
	if '/' in outfile_path:
		dir = os.path.dirname(outfile_path)
		os.makedirs(dir, exist_ok=True)
		if log:
			print(f"{datetime.now()} created directory: {dir}")

	if slice_row == 0:
		try:
			if log:
				print(f'{datetime.now()} creating CSV file {outfile_path}')
			
			# Create directory if it doesn't exist
			os.makedirs(os.path.dirname(outfile_path), exist_ok=True)
			
			df.to_csv(
				path_or_buf=outfile_path, 
				sep=sep,
				encoding='utf-8',
				index=False,
				header=True
			)

			if log:
				print(f'{datetime.now()} {outfile_path} created')

		except Exception as error:
			print(f"Failed to create CSV file {outfile_path}.\n\n{error}")
			if not ignore_error:
				raise

	else:
		for cur_row in range(0, len(df), slice_row):
			try:
				file_ver = cur_row // slice_row + 1
				subset_df = df.iloc[cur_row:cur_row + slice_row]
				new_outfile_path = outfile_path.replace('.csv', f'_{file_ver}.csv')

				if log:
					print(f'{datetime.now()} creating CSV file {new_outfile_path}')

				# Create directory if it doesn't exist
				os.makedirs(os.path.dirname(new_outfile_path), exist_ok=True)
				
				subset_df.to_csv(
					path_or_buf=new_outfile_path, 
					sep=sep,
					encoding='utf-8',
					index=False,
					header=True
				)

				if log:
					print(f'{datetime.now()} {new_outfile_path} created')

			except Exception as error:
				print(f"Error creating {new_outfile_path}.\n\n{error}")
				if not ignore_error:
					raise
	if dlt_dir:
		os.rmdir(dir)
		if log:
			print(f"{datetime.now()} deleted {dir}")

# export DF as Excel file
def df_to_excel(df, slice_row:int, outfile_path:str, dlt_dir:bool=False,  log:bool=False, ignore_error:bool=False):
	if not 0 < slice_row <= 1000000:
		raise ValueError('Invalid slice length.')
	
	# Extract dir path from file path and create dir if it doesn't exist yet.
	if '/' in outfile_path:
		dir = os.path.dirname(outfile_path)
		os.makedirs(dir, exist_ok=True)
		if log:
			print(f"{datetime.now()} created directory: {dir}")

	if slice_row == 0:
		try:
			if log:
				print(f'{datetime.now()} creating Excel file {outfile_path}')

			# Create directory if it doesn't exist
			os.makedirs(os.path.dirname(outfile_path), exist_ok=True)
			
			with pd.ExcelWriter(outfile_path, engine='xlsxwriter') as writer:
				df.to_excel(writer, index=False, header=True)

			if log:
				print(f'{datetime.now()} {outfile_path} created')

		except Exception as error:
			print(f"Failed to create Excel file {outfile_path}.\n\n{error}")
			if not ignore_error:
				raise

	else:
		for cur_row in range(0, len(df), slice_row):
			try:
				file_ver = cur_row // slice_row + 1
				subset_df = df.iloc[cur_row:cur_row + slice_row]
				new_outfile_path = outfile_path.replace('.xlsx', f'_{file_ver}.xlsx')

				if log:
					print(f'{datetime.now()} creating Excel file {new_outfile_path}')

				with pd.ExcelWriter(new_outfile_path, engine='xlsxwriter') as writer:
					subset_df.to_excel(writer, index=False, header=True)

				if log:
					print(f'{datetime.now()} {new_outfile_path} created')

			except Exception as error:
				print(f"Failed to create Excel file {new_outfile_path}.\n\n{error}")
				if not ignore_error:
					raise
	
	if dlt_dir:
		os.rmdir(dir)
		if log:
			print(f"{datetime.now()} deleted {dir}")

# export DF as CSV binary file
def df_to_csv_bin(df:pd.DataFrame, slice_row:int, outfile_name:str, sep:str=',', log:bool=False, ignore_error:bool=False) -> List[Tuple]:
	if not 0 < slice_row <= 1000000:
		raise ValueError('Invalid slice length.')
	
	csv_buffers = []

	if slice_row == 0:
		try:
			if log:
				print(f'{datetime.now()} creating CSV binary file for {outfile_name}')
			
			file_buffer = BytesIO()
			df.to_csv(
				path_or_buf=file_buffer, 
				sep=sep,
				encoding='utf-8',
				index=False,
				header=True
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
		for cur_row in range(0, len(df), slice_row):
			try:
				file_ver = cur_row // slice_row + 1
				subset_df = df.iloc[cur_row:cur_row + slice_row]
				new_outfile_name = outfile_name.replace('.csv', f'_{file_ver}.csv')

				if log:
					print(f'{datetime.now()} creating CSV binary file for {new_outfile_name}')

				cur_buffer = BytesIO()
				subset_df.to_csv(
					path_or_buf=cur_buffer, 
					sep=sep,
					encoding='utf-8',
					index=False,
					header=True
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

# export DF as Excel binary file
def df_to_excel_bin(df, slice_row:int, outfile_name:str, log=False, ignore_eror=False) -> List[Tuple]:
	if not 0 < slice_row <= 1000000:
		raise ValueError('Invalid slice length.')

	excel_buffers = []

	if slice_row == 0:
		try:
			if log:
				print(f'{datetime.now()} creating xlsx binary file for {outfile_name}')

			cur_buffer = BytesIO()
			with pd.ExcelWriter(cur_buffer, engine='xlsxwriter') as file_buffer:
				df.to_excel(file_buffer, index=False, header=True)
			excel_buffers.append(outfile_name, cur_buffer.seek(0))

			if log:
				print(f'{datetime.now()} {outfile_name} binary created')

		except Exception as error:
			print(f"Failed to create Excel binary for {outfile_name}.\n\n{error}")
			if not ignore_eror:
				raise

	else:
		try:
			# slice the results of each script
			for cur_row in range(0, len(df), slice_row):
				file_ver = cur_row // slice_row + 1
				subset_df = df.iloc[cur_row:cur_row + slice_row]
				new_outfile_name = outfile_name.replace('.xlsx', f'_{file_ver}.xlsx')

				if log:
					print(f'{datetime.now()} creating xlsx binary file for {new_outfile_name}')

				# init binary buffer for xlsx file
				cur_buffer = BytesIO()

				with pd.ExcelWriter(cur_buffer, engine='xlsxwriter') as writer:
					subset_df.to_excel(writer, index=False, header=True)
				cur_buffer.seek(0)

				# add the buffer data and file name to the main list
				excel_buffers.append((new_outfile_name, cur_buffer))

				if log:
					print(f'{datetime.now()} {new_outfile_name} binary created')

		except Exception as error:
			print(f"Failed to create xlsx binary file for {new_outfile_name}.\n\n{error}")
			if not ignore_eror:
				raise

	return excel_buffers
