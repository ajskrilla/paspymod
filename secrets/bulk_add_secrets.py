import json
from paspymod.funct_tools import query_request, other_requests, sanitizedict, boolize
from paspymod.logger import logging as log
import argparse
import os
import csv
import ast
# Test to see if file path works. It more than likely will
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add a list of secrets from a CSV file, JSON file, or list. All headers in file match the values of the API page. Check example_files to compare.")
    parser.add_argument('-p','--Path', type=str, required=False, default=None, help= 'Path to the csv file. Point to csv in arg path and use forward slashes in the path if using windows.')
    parser.add_argument('-l','--List', type=ast.literal_eval, required=False, default=None, help= 'Array of secrets. Please input as a list such as .')
    parser.add_argument('-j','--JSON', type=str, required=False, default=None, help= 'JSON file of secrets. Please input the full file path.')
    args = parser.parse_args()

if args.Path != None:
    path = os.path.abspath(args.Path)
    log.info("Path to the csv file to add resources is: {0}".format(path))
    with open(path, 'r') as f:
        d_reader = csv.DictReader(f)
        for line in d_reader:
            args = sanitizedict(dict(line))
            log.info("Passing secret with args: {0}".format(args.items()))
            other_requests(Call='/ServerManage/AddSecret', **args, Debug=True)