#!/usr/bin/env python3
from paspymod.funct_tools import query_request, other_requests
from paspymod.logger import logging as log
import argparse
# this will add ONE Account.
# https://developer.centrify.com/reference#post_servermanage-addaccount
# will support mfatokuri at some point
#do
def cl():
    parser = argparse.ArgumentParser(description="Add a domain, database, or system account")
    parser.add_argument('-des','--Description', type=str, required=False, default='null', help= 'Description of the account')
    parser.add_argument('-u','--User', type=str, required=True, help= 'Username of the account')
    parser.add_argument('-d','--Domain', type=str, required=False, default=None, help= 'Domain name (FQDN)')
    parser.add_argument('-db','--Database', type=str, required=False, default=None,  help= 'Database name') 
    parser.add_argument('-s', '--Host', type=str, required=False, help= 'Host name (FQDN)')
    parser.add_argument('-ssh','--SshKeyId', type=str, required=False, help= 'service account of the token')
    parser.add_argument('-p','--Password', type=str, required=True, help= 'pw of account')
    parser.add_argument('-im','--IsManaged', type=bool, required=False, default=False, help= 'if account is managed')
    return parser.parse_args()
#can propabaly steam the add_system new dict idea to clean this up
def delete_bad_keys():
	del args['Domain']
	del args['Database']
	del args['Host']
def Add_Account(**kwargs):
	log.info('Using argument values: {0}'.format(args))
	log.info("Using endpoint /ServerManage/AddAccount...")
	kwargs = args
	if args['Domain'] != None:
		log.info("Adding account to Domain: {0}...".format(args['Domain']))	
		Domain_Query = query_request(sql = """SELECT VaultDomain.ID FROM VaultDomain WHERE UPPER(VaultDomain.Name) = '%s'""" % args['Domain'].upper()).parsed_json
		if Domain_Query['Result']['Count'] == 0:
			log.error("Issue finding Domain {0}".format(args['Domain']))
		else:
			delete_bad_keys()
			args['DomainID'] = Domain_Query["Result"]["Results"][0]["Row"]['ID']
			other_requests(Call="/ServerManage/AddAccount", Debug=True, **kwargs)
			return None
	if args['Host'] != None:
		log.info("Adding account to Host: {0}...".format(args['Host']))
		System_Query = query_request(sql =  """SELECT Server.ID FROM Server WHERE UPPER(Server.Name) = '%s'""" % args['Host'].upper()).parsed_json
		if System_Query['Result']['Count'] == 0:
			log.error("Issue finding system {0}".format(args['Host']))
		else:
			delete_bad_keys()
			args['Host'] = System_Query["Result"]["Results"][0]["Row"]['ID']
			other_requests(Call="/ServerManage/AddAccount", Debug=True, **kwargs)
			return None
	if args['Database'] != None:
		log.info("Adding account to Database: {0}...".format(args['Database']))
		DB_Query = query_request(sql = """SELECT VaultDatabase.ID FROM VaultDatabase WHERE UPPER(VaultDatabase.Name) = '%s'""" % args['Database'].upper()).parsed_json
		if DB_Query['Result']['Count'] == 0:
			log.error("Issue finding database {0}".format(args['Database']))
		else:
			delete_bad_keys()
			args['DatabaseID'] = DB_Query["Result"]["Results"][0]["Row"]['ID']
			other_requests(Call="/ServerManage/AddAccount", Debug=True, **kwargs)
			return None
	log.info("Sucessfully Added account {0}".format(args['User']))
if __name__ == "__main__":
	args = vars(cl())
	Add_Account()