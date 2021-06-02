from paspymod.funct_tools import query_request, other_requests, rem_null
from paspymod.logger import logging as log
import argparse
#https://developer.centrify.com/reference#post_servermanage-updateaccount

def cl():
    parser = argparse.ArgumentParser(description="Add a domain, database, or system account")
    parser.add_argument('-des','--Description', type=str, required=False, default='null', help= 'Description of the account')
    parser.add_argument('-u','--User', type=str, required=False, help= 'Username of the account')
    parser.add_argument('-d','--Domain', type=str, required=False, default=None, help= 'Domain ID')
    parser.add_argument('-db','--Database', type=str, required=False, default=None,  help= 'Database ID') 
    parser.add_argument('-s', '--Host', type=str, required=False, help= 'Host ID')
    parser.add_argument('-n','--Name', type=str, required=True, default=False, help= 'Name of the ')
    parser.add_argument('-uw','--UseWheel', type=bool, required=False, default=False, help= 'if account is managed')

def update_account(**kwargs):
    log.info("Using args: {0}".format(args))
    log.info("Using endpoint /ServerManage/UpdateAccount.")
    kwargs = rem_null(args)
    a_query = query_request(sql= """SELECT VaultAccount.ID FROM User WHERE VaultAccount.Name = '{0}'""".format(args.Name)).parsed_json
    if a_query['Result']['Count'] == 0:
        log.error("Account: {0} not found".format(args.Name))
    del args['Name']
    other_requests(Call='/ServerManage/UpdateAccount', ID =a_query["Result"]["Results"][0]["Row"]['ID'] ,**kwargs, Debug=True)

if __name__ == "__main__":
	args = vars(cl())
	update_account()