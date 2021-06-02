#!/usr/bin/env python3
from paspymod.funct_tools import query_request, other_requests
from paspymod.logger import logging as log
import argparse
#https://developer.centrify.com/reference#post_servermanage-getaccountsforresource
#API request call
def cl():
    #make CL arg for RRFormat=True, will support
    parser = argparse.ArgumentParser(description="Get accounts of a computer resource")
    parser.add_argument('-n','--Name', type=str, required=False, default=None, help= 'Name of the system (FQDN)')
    return parser.parse_args()
if __name__ == "__main__":
    args = vars(cl())
class get_accounts_for_resource:
    log.info("Using endpoint /ServerManage/GetAccountsforResource")
    log.info("Getting Resource.....")
    def __init__(self):
        sys_query = query_request(sql ="""SELECT Server.ID FROM Server WHERE UPPER(Server.FQDN) = '%s'""" % args['Name'].upper()).parsed_json
        if sys_query["Result"]["Count"] == 0:
            log.error("Account not found")
            return None
        self._id = sys_query["Result"]["Results"][0]["Row"]['ID']
        try:
            other_requests(Call="/ServerManage/GetAccountsForResource", Computer=self._id, Debug=True)
            log.info("Sucessfully got the resource")
        except:
            log.error("An internal error occurred. Please check logs. Failed on /ServerManage/GetAccountsforResource")
get_accounts_for_resource()