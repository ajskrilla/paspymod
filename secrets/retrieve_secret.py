#!/usr/bin/env python3
from paspymod.funct_tools import query_request, other_requests
from paspymod.logger import logging as log
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get secret info.")
    parser.add_argument('-n','--Name', type=str, required=True, help= 'Name of Secret')
    args = parser.parse_args()
    
log.info("Querying ID for secret: {0}....".format(args.Name))
id = query_request(sql="SELECT DataVault.ID FROM DataVault WHERE UPPER(DataVault.SecretName) = '{0}'".format(args.Name.upper())).parsed_json
if id['Result']['Count'] == 0:
    log.error("Secret not found OR you do not have view access to the secret.")
sid = id['Result']['Results'][0]['Row']['ID']
log.info("Using endpoint /ServerManage/RetrieveSecretContents....")
log.info("Found Secret.")
other_requests(Call="/ServerManage/RetrieveSecretContents", ID=sid, Debug=True)