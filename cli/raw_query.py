#!/usr/bin/env python3
from paspymod.funct_tools import query_request
from paspymod.logger import logging as log
import argparse
import pprint

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Have a SQL query to tenant.")
    parser.add_argument('-q','--Query', type=str, required=True, help= 'Query to the tenant.')
    args = parser.parse_args()

log.info("Using SQL query: {0}".format(args.Query))
log.info("Executing query....")
query_request(sql=args.Query, Debug=True)