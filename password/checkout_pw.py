#!/usr/bin/env python3
from paspymod.funct_tools import query_request, other_requests
from paspymod.logger import logging as log
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check out PW of a managed account.")
    parser.add_argument('-n','--Name', type=str, required=True, help= 'Name of the managed account.')
    parser.add_argument('-l','--Lifetime', type=int, required=False, default= None, help= 'Lifetime of the checkout. If applicable.')
    parser.add_argument('-d','--Description', type=str, required=False, default= None, help= 'Description of the checkout action.')
    args = parser.parse_args()

log.info('Using argument values: {0}'.format(args))
log.info("Using endpoint /ServerManage/CheckoutPassword...")
log.info('Querying for ID.......')
id = query_request(sql= "Select VaultAccount.ID FROM VaultAccount WHERE Upper(VaultAccount.User) = '{0}'".format(args.Name.upper())).parsed_json
if id['Result']['Count'] == 0:
	log.error("Account not found")
other_requests(Call= "/ServerManage/CheckoutPassword", ID=id["Result"]["Results"][0]["Row"]['ID'], Description=args.Description, Lifetime=args.Lifetime, Debug=True)


