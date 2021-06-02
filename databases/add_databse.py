#!/usr/bin/env python3
from paspymod.funct_tools import query_request, other_requests
from paspymod.logger import logging as log
import argparse
import json
#https://developer.centrify.com/reference#post_servermanage-adddatabase
def cl():
    parser = argparse.ArgumentParser(description="Add a DataBase")
    parser.add_argument('-des','--Description', type=str, required=True, help= 'Description of the resource')
    parser.add_argument('-dn','--FQDN', type=str, required=True, help='Fully-qualified domain name or IP address of the system')
    parser.add_argument('-ppid','--PasswordProfileID', type=str, default=None, required=False, help= 'Password profile ID for the system') 
    parser.add_argument('-dc', '--DatabaseClass', type=str, required=True, help='Database type: Oracle, SQLServer')
    parser.add_argument('-in','--InstanceName', type=bool, default=None, required=False, help= 'The instance name of the database. Applicable to SQL Server only.')
    parser.add_argument('-sn','--ServiceName', type=str, required=True, help= 'The service name of the database. Applicable to Oracle Database only.')
    parser.add_argument('-p','--Port',s type=str, required=False, default=None, help= 'Display name of the system')
    parser.add_argument('-n','--Name', type=str, required=True, help= 'Display name of the system')
    return parser.parse_args()
if __name__ == "__main__":
    args = vars(cl())
def add_database():
    new_args = dict((k, v) for k, v in args.items() if v != None)
    log.info("Using endpoint ServerManage/AddDatabase...")
    try:
        log.info("Adding DataBase resource: {0}.....".format(args['FQDN']))
        req = other_requests(Call="ServerManage/AddDatabase", **new_args, Debug=True)
        log.info("Added Database resource: {0}".format(args['FQDN']))
    except:
        log.error("An Internal error occured during ServerManage/AddDatabase. Please check logs")
add_database()