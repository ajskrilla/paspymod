#!/usr/bin/env python3
from paspymod.funct_tools import query_request, other_requests
from paspymod.logger import logging as log
import argparse
#https://developer.centrify.com/reference#post_servermanage-deleteaccount
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="deletes an account")
    parser.add_argument('-n','--Name', type=str, required=False, default=None, help= 'Name of the account')
    args = parser.parse_args()

log.info("Using endpoint /ServerManage/DeleteAccount....")
log.info("Querying for ID........")
try:
    a_query = query_request(sql= """SELECT User.ID FROM User WHERE User.Name = '{0}'""".format(args.Name)).parsed_json
    if a_query['Result']['Count'] == 0:
        log.error("Account: {0} not found".format(args.Name))
    else:
        other_requests(Call="/ServerManage/DeleteAccount", ID=a_query["Result"]["Results"][0]["Row"]['ID'])
        log.info("Account {0} Deleted.".format(args.Name))
except:
    log.error("An internal error occurred while try to execute endpoint /ServerManage/DeleteAccount.")
