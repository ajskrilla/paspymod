#!/usr/bin/env python3
from paspymod.funct_tools import query_request, other_requests
from paspymod.logger import logging as log
import argparse
#https://developer.centrify.com/reference#post_servermanage-deleteresource
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete a system. Use IP or Name.")
    parser.add_argument('-n','--Name', type=str, required=True, help= 'Name or IP address of the system.')
    args = parser.parse_args()
def delete_system():
    try:
        log.info("Using endpoint /ServerManage/DeleteResource....")
        log.info("Querying System.....")
        query = query_request(sql = "Select Server.ID FROM Server WHERE Server.Name  = '{0}'".format(args.Name)).parsed_json
        if query['Result']['Count'] == 0:
            log.error("System: {0} Not found".format(args.Name))
        else:
            log.info("System: {0} will be deleted".format(args.Name))
            other_requests(Call="/ServerManage/DeleteResource", Debug= True, ID=query["Result"]["Results"][0]["Row"]['ID'] )
            log.info("System: {0} will be deleted".format(args.Name))
    except:
        log.error("Internal error occured at delete_system.py")
delete_system()
