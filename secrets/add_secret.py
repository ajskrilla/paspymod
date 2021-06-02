#!/usr/bin/env python3
from paspymod.funct_tools import query_request, other_requests
from paspymod.logger import logging as log
import argparse
#https://developer.centrify.com/reference#post_servermanage-addsecret
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Adds a secret.")
    parser.add_argument('-sfp','--SecretFilePath', type=str, required=False, help= 'The file path from a call to for file type secrets.')
    parser.add_argument('-n','--SecretName', type=str, required=True, help= 'The secret name.')
    parser.add_argument('-fid','--FolderId', type=str, required=False, help= '(optional) The folder to add the secret to.')
    parser.add_argument('-wfdo','--WorkflowDefaultOptions', type=str, required=False, help= 'Stringified JSON object detailing default options. Example: {"GrantMin":60}.')
    parser.add_argument('-sfs','--SecretFileSize', type=str, required=False, help= 'The file size from a call to for file type secrets.')
    parser.add_argument('-st','--SecretText', type=str, required=False, help= 'The secret text contents for text type secrets.')
    parser.add_argument('-wfs','--WorkflowSent', type=bool, required=False, help= 'Informs whether or not this is a workflow change.')
    parser.add_argument('-sfpw','--SecretFilePassword', type=str, required=False, help= 'The password for a protected secret file.')
    parser.add_argument('-t','--Type', type=str, required=True, help= 'The secret type (Text or File).')
    parser.add_argument('-wfe','--WorkflowEnabled', type=bool, required=False, help= 'Determines whether you are removing or adding/updating a workflow.')
    parser.add_argument('-sfd','--Description', type=str, required=False, help= 'The secret description.')
    args = parser.parse_args()

def sanitizedict(d):
    return dict([(k,v) for k,v in d.items() if v != None])
def add_secret(**kwargs):
    kwargs = vars(args)
    log.info("Using Endpoint /ServerManage/AddSecret.....")
    log.info('Using argument values: {0}'.format(vars(args)))
    n_d = sanitizedict(dict(kwargs))
    try:
        other_requests(Call='/ServerManage/AddSecret', Debug=True, **n_d)
    except:
        log.error('Issue running add_secret.py')

add_secret()
