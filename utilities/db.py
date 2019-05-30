#Connect to ArchivesSpace database through SSH Tunnel

import pymysql
import yaml
import csv
import pandas as pd

#add error handling, logging
#don't forget to close the connection
class DBConn():
	"""Class to connect to ArchivesSpace database via SSH and run queries."""
	def __init__(self, config_file=None):
		self.config_file = self._get_config(config_file)
		self.sql_hostname = self.config_file['local_sql_hostname']
		self.sql_username = self.config_file['local_sql_username']
		self.sql_password = self.config_file['local_sql_password']
		self.sql_database = self.config_file['local_sql_database']
		self.sql_port = self.config_file['local_sql_port']
		self.conn = self._start_conn()

	#looks for user-provided config file. If not present looks in cwd
	def _get_config(self, cfg):
		"""Gets config file"""
		if cfg != None:
			return cfg
		else:
			cfg = yaml.load(open('config.yml', 'r', encoding='utf-8'))
			return cfg

	def _start_conn(self):
		"""Starts the connection."""
		connect = pymysql.connect(host=self.sql_hostname, user=self.sql_username, passwd=self.sql_password, db=self.sql_database, port=self.sql_port)
		return connect

	#what is the point of creating a pandas dataframe and then converting to a list? wouldn't that take longer??
	def run_query(self, query):
		"""Runs a query."""
		data = pd.read_sql_query(query, self.conn)
		return data

	# def run_query(self, query):
	# 	cursor = self.conn.cursor()
	# 	cursor.execute(query)
	# 	data = cursor.fetchall()
	# 	for i in data:
	# 		yield data

	def close_conn(self):
		"""Close both db connection and ssh server. Must do this before quitting Python.
		Need to find a way to do this even if user does not call method."""
		self.conn.close()

	#This works well, but not if the query data requires additional processing
	def write_output(self, query_data, output_dir, filename):
		"""Writes the query output to a CSV file."""
		column_list = list(query_data.columns)
		datalist = query_data.values.tolist()
		newfile = open(output_dir + '/' + filename + '_results.csv', 'a', encoding='utf-8', newline='')
		writer = csv.writer(newfile)
		writer.writerow(column_list)
		writer.writerows(datalist)
		newfile.close()

	#Should do the cgi thing to process HTML tags and remove
