#!/usr/bin/env python3
from paspymod.funct_tools import query_request, other_requests
from paspymod.logger import logging as log
import pprint
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get a system or all systems in tenant.")
    parser.add_argument('-n','--Name', type=str, required=False, help= 'FQDN of the system')
    args = parser.parse_args()
# set this up as its own fucking module library so that the return function can be imported
class get_system:
    def __init__(self):
        log.info('Querying Domain(s)....')
        if args.Name == None:
            self.query = query_request(sql = """SELECT VaultAccount.Healthy, VaultAccount.ID, VaultAccount.LastHealthCheck, VaultAccount.Name, \
            VaultAccount.User FROM VaultAccount WHERE VaultAccount.User Like '%'""").parsed_json
        else:
            self.query = query_request(sql = """SELECT VaultAccount.Healthy, VaultAccount.ID, VaultAccount.LastHealthCheck, VaultAccount.Name, \
            VaultAccount.User FROM VaultAccount WHERE VaultAccount.User = '{0}'""".format(args.Name)).parsed_json
        if self.query["Result"]["Count"] == 0:
            log.error("Account not found")
            return None
        elif self.query["Result"]["Count"] > 0:
            log.info("Domain(s) found")
            pp = pprint.PrettyPrinter(indent=4)
            for i in range(self.query["Result"]["Count"]):
                self.sys_dict = {
                    'Name' : self.query["Result"]["Results"][i]["Row"]['Name'],
                    'ID' : self.query["Result"]["Results"][i]["Row"]['ID'],
                    'User' : self.query["Result"]["Results"][i]["Row"]['User'],
                    'Healthy' :self.query["Result"]["Results"][i]["Row"]['Healthy'],
                    'LastHealthCheck' : self.query["Result"]["Results"][i]["Row"]['LastHealthCheck']
                }
                pp.pprint(self.sys_dict)
    #maybe trash as this is not valid in a CL arg. More of an SDK/Module
    @property
    def dict_sys(self):
        return self.sys_dict

get_system()