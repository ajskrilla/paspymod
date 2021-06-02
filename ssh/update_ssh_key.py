#!/usr/bin/env python3
from paspymod.funct_tools import query_request, other_requests, rem_null
from paspymod.logger import logging as log
import argparse
#https://developer.centrify.com/reference#post_servermanage-updatesshkey
def cl():
    parser = argparse.ArgumentParser(description="Update SSH key.")
    parser.add_argument('-c','--Comment', type=str, required=False, help= 'Passphrase to use for encrypting the PrivateKey.')
    parser.add_argument('-un','--UpdatedName', type=str, required=False, help= 'Which key to retrieve from the pair, must be either PublicKey, PrivateKey, or PPK')
    parser.add_argument('-n','--Name', type=str, required=True, help= 'The name of the SSH key to query.')
    return parser.parse_args()

if __name__ == "__main__":
    args = vars(cl())

def update_ssh_key(**kwargs):
    kwargs = rem_null(args)
    log.info("args are : {0}".format(kwargs))
    query = query_request(sql = "SELECT SshKeys.ID FROM SshKeys WHERE UPPER(SshKeys.Name) = '{0}'".format(args['Name'].upper())).parsed_json

    if query['Result']['Count'] == 0:
        log.error("SSH Key: {0} n.ot found".format(args.Name))
    
    if kwargs['UpdatedName']:
        kwargs['Name'] = kwargs.pop('UpdatedName')
        print(kwargs['Name'])
    
    other_requests(Call='/ServerManage/UpdateSshKey', **kwargs, ID=query["Result"]["Results"][0]["Row"]['ID'], Debug=True)

update_ssh_key()