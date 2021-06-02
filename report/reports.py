#!/usr/bin/env python3
from paspymod.funct_tools import query_request, other_requests
from paspymod.logger import logging as log
import argparse
import csv
import os
import errno
#This will query and export a report to a file path
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Save a query as a csv. Please give valid SQL query to tenant.")
	parser.add_argument('-p','--Path', type=str, required=True, help= 'Path to the csv file. Point to csv in arg path and use forward slashes in the path if using windows.')
	parser.add_argument('-q','--Query', type=str, required=True, help= 'Query against the tenant (i.e "Select * From Server").')
	args = parser.parse_args()

def write_to_csv(wanted):
	if ".csv" in args.Path:
		path = os.path.abspath(args.Path)
		if not os.path.exists(os.path.dirname(path)):
			try:
				os.makedirs(os.path.dirname(path))
			except OSError as exc: # Guard against race condition
				if exc.errno != errno.EEXIST:
					raise
		with open(path, 'w') as f:
			writer= csv.DictWriter(f, fieldnames=wanted[0].keys(), delimiter=',')
			writer.writeheader()
			writer.writerows(wanted)
		log.info("Query Saved to {0}".format(path))
	else:
		log.error("Need to have file end in .csv")

def Query(sqlquery= args.Query):
	log.info("SQL Query is: {0}".format(args.Query))
	try:
		query = query_request(sql = args.Query).parsed_json
		wanted = [dict(x["Row"]) for x in query["Result"]["Results"]]
		write_to_csv(wanted)
	except:
		log.error("Error occurred on reports.py")
Query()