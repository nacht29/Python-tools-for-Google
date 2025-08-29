import pandas as pd
from io import BytesIO
from datetime import datetime
from google.cloud import bigquery as bq

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

def bq_to_df(bq_client, sql_script:str, replace_in_query:list=[], log=False, ignore_error=False):
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

# read SQL script and query data from BQ
# write data to excel binary
# returns [(filename1, buffer1), (filename2, buffer2), ...]
def bq_to_excel(bq_client,
				sql_script:str,
				slice_row:int,
				outfile_name:str,
				replace_in_query:list=[],
				log=False,
				ignore_eror=False
) -> tuple:

	if not 0 < slice_row <= 1000000:
		raise ValueError('Invalid slice length.')

	results_df = bq_to_df(bq_client, sql_script, replace_in_query, log, ignore_eror)
	excel_buffers = []

	if slice_row == 0:
		try:
			if log:
				print(f'{datetime.now()} creating xlsx binary file for {outfile_name}')

			cur_buffer = BytesIO()
			with pd.ExcelWriter(cur_buffer, engine='xlsxwriter') as file_buffer:
				results_df.to_excel(file_buffer, index=False, header=True)
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
			for cur_row in range(0, len(results_df), slice_row):
				file_ver = cur_row // slice_row + 1
				subset_df = results_df.iloc[cur_row:cur_row + slice_row]
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