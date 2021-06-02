#!/usr/bin/env python3
from paspymod.funct_tools import other_requests, rem_null
from paspymod.logger import logging as log
import argparse
import os
#https://developer.centrify.com/reference#post_servermanage-addsshkey

def cl():
    parser = argparse.ArgumentParser(description="Add SSH key from path to SSH Key")
    parser.add_argument('-c','--Comment', type=str, required=False, help= 'The comment for the SSH key.')
    parser.add_argument('-ir','--ImplicitRename', type=bool, required=False, help= 'If true and the key Name given is not unqiue, will rename the key to avoid collision')
    parser.add_argument('-pk','--PrivateKey', type=str, required=True, help= 'The SSH private key to store.')
    parser.add_argument('-p','--Passphrase', type=str, required=False, help= 'The passphrase for the SSH key, if encrypted.')
    parser.add_argument('-n','--Name', type=str, required=False, help= 'The name of the SSH key.')
    return parser.parse_args()

if __name__ == "__main__":
    args = vars(cl())

def ssh_key_add(**kwargs):
    if not os.path.isfile(args['PrivateKey']):
        log.error("PrivateKey is not there")
        
    kwargs = rem_null(args)
    kwargs['PrivateKey'] = os.path.abspath(kwargs['PrivateKey'])
    log.info("args are : {0}".format(kwargs))
    log.info("Path to the key PrivateKey is: {0}".format(args['PrivateKey']))
    log.info("Using Endpoint")

    with open(kwargs['PrivateKey'], 'r') as f:
        kwargs['PrivateKey'] = f.read()
        other_requests(Call='/ServerManage/AddSshKey', **kwargs, Debug=True)

ssh_key_add()
