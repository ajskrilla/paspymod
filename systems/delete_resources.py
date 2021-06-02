#!/usr/bin/env python3
import json
import ast
from paspymod.funct_tools import query_request, other_requests, sanitizedict, boolize
from paspymod.logger import logging as log
import argparse
import csv
import os
#https://developer.centrify.com/reference#post_servermanage-deleteresources
#Must provide either Ids or SetQuery for request.
def cl():
    parser = argparse.ArgumentParser(description="Delete a list of resources from a CSV file, JSON file, or list. All headers in file match the values of the API page. Check example_files to compare.")
    parser.add_argument('-p','--Path', type=str, required=False, default=None, help= 'Path to the csv file. Point to csv in arg path and use forward slashes in the path if using windows.')
    parser.add_argument('-l','--List', type=ast.literal_eval, required=False, default=None, help= 'Array of resource ids. Please input as a list.')
    parser.add_argument('-j','--JSON', type=str, required=False, default=None, help= 'JSON file of resource names. Please input the full file path.')
    parser.add_argument('-sn','--SecretName', type=str, required=False, default=None, help= 'Name of secret for account passwords')
    parser.add_argument('-rs','--RunSync', type=bool, required=False, default=False, help= 'The operation will be executed synchronously if set to true. Defaults to false..')
    parser.add_argument('-sts','--SaveToSecrets', type=bool, required=False, default=False, help= 'Choose to save passwords for resource\'s accounts to a csv secret file')
    parser.add_argument('-sq','--SetQuery', type=str, required=False, default=False, help= 'Choose to save passwords for resource\'s accounts to a csv secret file')
    #marked as a string on docs for some reason
    parser.add_argument('-skipapps','--SkipIfHasAppsOrServices', type=bool, required=False, default=False, help= 'Choose to save passwords for resource\'s accounts to a csv secret file')
    return parser.parse_args()

if __name__ == "__main__":
	args = vars(cl())

if None in {args['Path'] or args['List'] or args['JSON'] or args['SetQuery']}:
    log.error("Need to input a valid arg. Use JSON, CSV, SetQuery, or a List of IDs to continue")
#change this to a function to be used in funct_tools
new_args = dict((k, v) for k, v in args.items() if v != None)

log.info('Using endpoint /ServerManage/DeleteResources.')

if args['SetQuery'] != None:
    other_requests(Call='/ServerManage/DeleteResources', **args, Debug=True)

if args['Path'] != None:
    path = os.path.abspath(args['Path'])
    with open(path, newline='') as f:
        reader = csv.reader(f)
        data = [tuple(row) for row in reader if row != None]
        altered = data[1:]
        empty_tuple = ()
        for row in altered:
            empty_tuple = empty_tuple + row
        print(empty_tuple)
    ID_query = query_request(sql ="SELECT Server.ID FROM Server WHERE Server.FQDN  IN %s" % str(empty_tuple)).parsed_json
    ids = [0]
    for i in range (ID_query["Result"]["Count"]):
        qIds = ID_query["Result"]["Results"][i]["Row"]['ID']
        ids = [ids.append(format(qIds))]
    other_requests(Call="/ServerManage/DeleteResources", Debug=True, ID=ids, **args)

if args['List'] != None:
    log.info("List of accounts is: {0}".format(args.List))
    other_requests(Call='/ServerManage/DeleteResources', ID=args.List, Debug=True, **args)

elif args['JSON'] != None:
    log.info("JSON file being used.")
    path = os.path.abspath(args.JSON)
    log.info("Path to the JSON file to add resources is: {0}".format(path))
    with open(path, 'r') as f:
        other_requests(Call='/ServerManage/DeleteResources', ID=json.load(f), Debug=True, **args)