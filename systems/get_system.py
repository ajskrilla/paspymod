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
        log.info('Querying system(s)....')
        if args.Name == None:
            self.query = query_request(sql = """SELECT Server.ComputerClass, Server.FQDN, Server.HealthStatus, Server.ID, Server.LastHealthCheck, Server.LastState, \
                Server.Name, Server.SessionType FROM Server WHERE Server.FQDN Like '%'""").parsed_json
        else:
            self.query = query_request(sql = """SELECT Server.ComputerClass, Server.FQDN, Server.HealthStatus, Server.ID, Server.LastHealthCheck, Server.LastState, \
                Server.Name, Server.SessionType FROM Server WHERE UPPER(Server.FQDN) = '{0}'""".format(args.Name.upper())).parsed_json
        if self.query["Result"]["Count"] == 0:
            log.error("System not found")
            return None
        elif self.query["Result"]["Count"] > 0:
            log.info("System(s) found")
            pp = pprint.PrettyPrinter(indent=4)
            for i in range(self.query["Result"]["Count"]):
                self.sys_dict = {
                    'Name' : self.query["Result"]["Results"][i]["Row"]['Name'],
                    'ID' : self.query["Result"]["Results"][i]["Row"]['ID'],
                    'Session' : self.query["Result"]["Results"][i]["Row"]['SessionType'],
                    'Computer Class' : self.query["Result"]["Results"][i]["Row"]['ComputerClass'],
                    'Health Check' :self.query["Result"]["Results"][i]["Row"]['HealthCheck'],
                    'LastHealthCheck' : self.query["Result"]["Results"][i]["Row"]['LastHealthCheck'],
                    'LastState' : self.query["Result"]["Results"][i]["Row"]['LastState']
                }
                log.info("System Return info: {0}".format(self.sys_dict))
                pp.pprint(self.sys_dict)
    #maybe trash as this is not valid in a CL arg. More of an SDK/Module
    @property
    def dict_sys(self):
        return self.sys_dict

get_system()
                   
