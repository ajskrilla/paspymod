#!/usr/bin/env python3
from paspymod.funct_tools import query_request, other_requests
from paspymod.logger import logging as log
import argparse
#https://developer.centrify.com/reference#post_servermanage-addsecretsfolder

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Adds a secret folder.")
    parser.add_argument('-d','--Description', type=str, required=False, help= 'The folder description.')
    parser.add_argument('-n','--FolderName', type=str, required=True, help= 'The folder name.')
    args = parser.parse_args()

def sanitizedict(d):
    return dict([(k,v) for k,v in d.items() if v != None])
def add_secret(**kwargs):
    kwargs = vars(args)
    log.info("Using Endpoint /ServerManage/AddSecretFolder.....")
    log.info('Using argument values: {0}'.format(vars(args)))
    n_d = sanitizedict(dict(kwargs))
    try:
        other_requests(Call='/ServerManage/AddSecretFolder', Debug=True, **n_d)
    except:
        log.error('Issue running add_secret_folder.py')

add_secret()