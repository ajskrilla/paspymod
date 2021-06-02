#!/usr/bin/env python3
import json
from paspymod.funct_tools import query_request, other_requests
from paspymod.logger import logging as log
import argparse
import csv
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete a list of accounts from a CSV file, JSON file, or list. All headers in file match the values of the API page. Check example_files to compare.")
    parser.add_argument('-p','--Path', type=str, required=False, default=None, help= 'Path to the csv file. Point to csv in arg path and use forward slashes in the path if using windows.')
    parser.add_argument('-l','--List', type=ast.literal_eval, required=False, default=None, help= 'Array of account names. Please input as a list such as .')
    parser.add_argument('-j','--JSON', type=str, required=False, default=None, help= 'JSON file of account names. Please input the full file path.')
    args = parser.parse_args()

if args.Path != None:
    path = os.path.abspath(args.Path)
    with open(path, newline='') as f:
        reader = csv.reader(f)
        data = [tuple(row) for row in reader if row != None]
        altered = data[1:]
        empty_tuple = ()
        for row in altered:
            empty_tuple = empty_tuple + row
    ID_query = query_request(sql ="SELECT User.ID FROM User WHERE User.DisplayName  IN %s" % str(empty_tuple)).parsed_json
    ids = [0]
    for i in range (ID_query["Result"]["Count"]):
        qIds = ID_query["Result"]["Results"][i]["Row"]['ID']
        ids = [ids.append(format(qIds))]
    other_requests(Call="ServerManage/MultiAccountDelete", Debug=True, ID=ids)

if args.List != None:
    log.info("List of accounts is: {0}".format(args.List))
    other_requests(Call='/ServerManage/MultiAccountDelete', ID=args.List, Debug=True)

elif args.JSON != None:
    log.info("JSON file being used.")
    path = os.path.abspath(args.JSON)
    log.info("Path to the JSON file to add resources is: {0}".format(path))
    with open(path, 'r') as f:
        other_requests(Call='/ServerManage/MultiAccountDelete', ID=json.load(f), Debug=True)
        
else:
    log.error("Need to input an argument.")