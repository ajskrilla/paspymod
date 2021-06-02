#!/usr/bin/env python3
from paspymod.funct_tools import query_request, other_requests
from paspymod.logger import logging as log
import argparse
#https://developer.centrify.com/reference#post_servermanage-checkinpassword
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check in PW of a managed account.")
    parser.add_argument('-n','--Name', type=str, required=True, help= 'Name of the managed account.')
    args = parser.parse_args()

log.info('Using argument values: {0}'.format(args))
log.info("Using endpoint /ServerManage/CheckinPassword ...")
log.info('Querying for ID.......')
id = query_request(sql= "Select VaultAccount.ID FROM VaultAccount WHERE Upper(VaultAccount.User) = '{0}'".format(args.Name.upper())).parsed_json
if id['Result']['Count'] == 0:
	log.error("Account not found")
other_requests(Call= "/ServerManage/CheckinPassword", ID=id["Result"]["Results"][0]["Row"]['ID'], Debug=True)