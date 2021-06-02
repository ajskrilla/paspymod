from paspymod.funct_tools import other_requests, query_request
from paspymod.logger import logging as log
import argparse
# This will get the secret permissions of the current user
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get secret permission of current user/machine.")
    parser.add_argument('-n','--Name', type=str, required=True, help= 'Name of Secret')
    args = parser.parse_args()

log.info("Using endpoint /ServerManage/GetSecretRightsAndChallenges")
log.info("Translating name of secret to ID.")
id = query_request(sql="Select DataVault.ID FROM DataVault WHERE UPPER(DataVault.SecretName) = '{0}'".format(args.Name.upper())).parsed_json
if id['Result']['Count'] == 0:
    log.error("Secret not found")
log.info("Got ID now making call to tenant.")
other_requests(Call='/ServerManage/GetSecretRightsAndChallenges', ID=id['Result']['Results'][0]['Row']['ID'], Debug=True)