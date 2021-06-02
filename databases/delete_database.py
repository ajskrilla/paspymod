#!/usr/bin/env python3
from paspymod.funct_tools import query_request, other_requests
from paspymod.logger import logging as log
import argparse
#https://developer.centrify.com/reference#post_servermanage-deletedatabase
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete a Database. Use IP or Name.")
    parser.add_argument('-n','--Name', type=str, required=True, help= 'Name or IP address of the database.')
    args = parser.parse_args()
def delete_database():
    try:
        log.info("Using endpoint /ServerManage/DeleteDatabase ....")
        log.info("Querying Database.....")
        query = query_request(sql = "Select VaultDatabase.ID FROM VaultDatabase WHERE VaultDatabase.FQDN  = '{0}'".format(args.Name)).parsed_json
        if query['Result']['Count'] == 0:
            log.error("Database: {0} Not found".format(args.Name))
        else:
            log.info("Database: {0} will be deleted".format(args.Name))
            other_requests(Call="/ServerManage/DeleteDatabase", Debug= True, ID=query["Result"]["Results"][0]["Row"]['ID'] )
            log.info("Database: {0} is deleted".format(args.Name))
    except:
        log.error("Internal error occured at delete_database.py")
delete_database()