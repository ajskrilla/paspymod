#!/usr/bin/env python3
from paspymod.funct_tools import query_request, other_requests
from paspymod.logger import logging as log
import argparse
import csv
import os
import errno

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Save a connector check as a csv. Please give valid path.")
	parser.add_argument('-p','--Path', type=str, required=True, help= 'Path to the csv file. Point to csv in arg path and use forward slashes in the path if using windows.')
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

def conn_check():
	log.info("Using endpoint /Core/CheckProxyHealth.")
	#try:
	query = other_requests(Call= "/Core/CheckProxyHealth", Debug=True).parsed_json
	wanted = [dict(x["ConnectorInfo"]) for x in query["Result"]["Connectors"]]
	write_to_csv(wanted)
	log.info("Finished Connector report.")
	#except:
	#	log.error("Error occurred on connector_report.py")
conn_check()