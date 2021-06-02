#!/usr/bin/env python3
from paspymod.funct_tools import query_request, other_requests, sanitizedict
from paspymod.logger import logging as log
import argparse
# https://developer.centrify.com/reference#post_servermanage-updatesecret
# NEED TO UPDATE TO HAVE SECRET TYPE!
def cl():
    parser = argparse.ArgumentParser(description="Update secret info.")
    parser.add_argument('-n','--SecretName', type=str, required=True, help= 'Name of Secret')
    parser.add_argument('-sfp','--SecretFilePath', type=str, required=False, help= 'The file path from a call to for file type secrets')
    parser.add_argument('-id','--ID', type=str, required=False, help= 'The ID for the secret')
    parser.add_argument('-t','--Type', type=str, required=True, help= 'The secret type (Text or File).')
    parser.add_argument('-sfs','--SecretFileSize', type=str, required=False, help= 'The file size from a call to for file type secrets')
    parser.add_argument('-st','--SecretText', type=str, required=False, help= 'The secret text contents for text type secrets')
    parser.add_argument('-sfpw','--SecretFilePassword', type=str, required=False, help= 'The password for a protected secret file')
    parser.add_argument('-des','--Description', type=str, required=False, help= 'The secret description')
    return parser.parse_args()

if __name__ == "__main__":
    args = vars(cl())

new_args = dict((k, v) for k, v in args.items() if v != None)
log.info('Args are {}'.format(new_args))
log.info('Using argument values: {0}'.format(new_args))
id = query_request(sql="SELECT DataVault.ID FROM DataVault WHERE UPPER(DataVault.SecretName) = '{0}'".format(args['SecretName'].upper())).parsed_json

if id['Result']['Count'] == 0:
    log.error("Secret not found OR you do not have view access to the secret.")

log.info("Using endpoint /ServerManage/UpdateSecret.")
new_args['ID'] = id['Result']['Results'][0]['Row']['ID']
other_requests(Call='/ServerManage/UpdateSecret', **new_args, Debug=True)