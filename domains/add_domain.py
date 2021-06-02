#!/usr/bin/env python3
from paspymod.funct_tools import query_request, other_requests
from paspymod.logger import logging as log
import argparse
#https://developer.centrify.com/reference#post_servermanage-addresource
def cl():
    parser = argparse.ArgumentParser(description="Add a resource")
    parser.add_argument('-des','--Description', type=str, required=True, help= 'Description of the resource')
    parser.add_argument('-ppid','--PasswordProfileID', type=str, default=None, required=False, help= 'Password profile ID for the domain.') 
    parser.add_argument('-amlau','--AllowManualLocalAccountUnlock', type=bool, required=True, default=None, help='Allow local account manual unlock using a privileged account')
    parser.add_argument('-pup','--ProxyUserPassword', type=str, default=None, required=False, help= 'Password for the "proxy" account')
    parser.add_argument('-spid','--SystemProfileId', type=str, default=None, required=False, help= 'The resource profile ID for systems with ComputerClass CustomSsh')
    parser.add_argument('-aalam','--AllowAutomaticLocalAccountMaintenance', type=str, default=None, required=False, help= 'Allow local account automatic maintenance using a privileged account')
    parser.add_argument('-amau','--AllowManualAccountUnlock', type=str, default=None, required=False, help= 'Allow Domain administrative account on the domain to manually unlock domain accounts')
    parser.add_argument('-aaam','--AllowAutomaticAccountMaintenance', type=str, default=None, required=False, help= 'Allow Domain administrative account on the domain to reset domain account passwords')
    parser.add_argument('-n','--Name', type=str, required=True, help= 'Display name of the system')
    return parser.parse_args()
if __name__ == "__main__":
    args = vars(cl())
def add_account():
    new_args = dict((k, v) for k, v in args.items() if v != None)
    log.info("Using endpoint /ServerManage/AddDomain...")
    try:
        log.info("Adding domain: {0}.....".format(args['FQDN']))
        req = other_requests(Call="/ServerManage/AddDomain", **new_args, Debug=True)
        log.info("Added domain resource: {0}".format(args['FQDN']))
    except:
        log.error("An Internal error occured during /ServerManage/AddDomain. Please check logs")
add_account()