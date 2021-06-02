#!/usr/bin/env python3
from paspymod.funct_tools import query_request, other_requests
from paspymod.logger import logging as log
import argparse
#https://developer.centrify.com/reference#post_serveragent-verifypasswordv2
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verifies the PW of a vaulted.")
    parser.add_argument('-p','--Password', type=str, required=True, help= 'The folder description.')
    parser.add_argument('-n','--Name', type=str, required=True, help= 'The name of the account.')
    parser.add_argument('-ape','--AllowPasswordExpiration', type=bool, required=False, default=False, help= 'If true, an expired password will be considered valid. Otherwise, an expired password is considered an error.')
    args = parser.parse_args()

log.info("Using endpoint /ServerAgent/VerifyPasswordV2.")
log.info("Querying for account: {0}".format(args.Name))
query = query_request(sql="Select VaultAccount.ID from VaultAccount WHERE UPPER(VaultAccount.User) = '{0}'".format(args.Name.upper())).parsed_json
if query['Result']['Count'] == 0:
    log.error('Account not found')
else:
    other_requests(Call='/ServerAgent/VerifyPasswordV2', Password=args.Password, UUID=query["Result"]["Results"][0]["Row"]['ID'], AllowPasswordExpiration=args.AllowPasswordExpiration, Debug=True)