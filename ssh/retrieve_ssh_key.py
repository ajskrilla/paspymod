#!/usr/bin/env python3
from paspymod.funct_tools import query_request, other_requests, rem_null
from paspymod.logger import logging as log
import argparse
import os
#https://developer.centrify.com/reference#post_servermanage-retrievesshkey

def cl():
    parser = argparse.ArgumentParser(description="Retrieve SSH key as JSON string")
    parser.add_argument('-sftp','--SaveFiletoPath', type=str, required=False, help= 'Key will be saved to a file. Input OS path.')
    # Set this up as a file handler to write to the path provided
    parser.add_argument('-p','--Passphrase', type=str, required=False, help= 'Passphrase to use for encrypting the PrivateKey.')
    parser.add_argument('-kpt','--KeyPairType', type=str, required=True, help= 'Which key to retrieve from the pair, must be either PublicKey, PrivateKey, or PPK')
    parser.add_argument('-n','--Name', type=str, required=True, help= 'The name of the SSH key.')
    return parser.parse_args()

if __name__ == "__main__":
    args = vars(cl())

def retrieve_ssh_key(**kwargs):
    kwargs = rem_null(args)
    log.info("args are : {0}".format(kwargs))
    query = query_request(sql = "SELECT SshKeys.ID FROM SshKeys WHERE UPPER(SshKeys.Name) = '{0}'".format(args['Name'].upper())).parsed_json

    if query['Result']['Count'] == 0:
        log.error("SSH Key: {0} Not found".format(args.Name))

    ssh = other_requests(Call='/ServerManage/RetrieveSshKey', ID=query["Result"]["Results"][0]["Row"]['ID'], **kwargs, Debug=True).parsed_json
    if args['SaveFiletoPath']:    
        try:
            with open(kwargs['SaveFiletoPath'], 'w+') as f:
                f.write(ssh['Result'])
        except OSError:
            print("Error making the file. Is this a valid path")
retrieve_ssh_key()    
