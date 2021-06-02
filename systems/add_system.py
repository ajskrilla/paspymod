#!/usr/bin/env python3
from paspymod.funct_tools import query_request, other_requests
from paspymod.logger import logging as log
import argparse
#https://developer.centrify.com/reference#post_servermanage-addresource
def cl():
    parser = argparse.ArgumentParser(description="Add a resource")
    parser.add_argument('-des','--Description', type=str, required=True, help= 'Description of the resource')
    parser.add_argument('-dn','--FQDN', type=str, required=True, help='Fully-qualified domain name or IP address of the system')
    parser.add_argument('-pu','--ProxyUser', type=str, default=None, required=False, help= 'Name for the "proxy" account')
    parser.add_argument('-ppid','--PasswordProfileID', type=str, default=None, required=False, help= 'Password profile ID for the system') 
    parser.add_argument('-cc', '--ComputerClass', type=str, required=True, help='System type: Windows, Unix, CiscoIOS, CiscoNXOS, JuniperJunos, HpNonStopOS, IBMi, CheckPointGaia, PaloAltoNetworksPANOS, F5NetworksBIGIP, CiscoAsyncOS, VMwareVMkernel, GenericSsh, Customssh')
    parser.add_argument('-pism','--ProxyUserIsManaged', type=bool, default=None, required=False, help= 'Whether the password for the "proxy" account is managed')
    parser.add_argument('-st','--SessionType', type=str, required=True, help= 'Session type: Rdp, Ssh')
    parser.add_argument('-amlau','--AllowManualLocalAccountUnlock', type=bool, required=False, default=None, help='Allow local account manual unlock using a privileged account')
    parser.add_argument('-pup','--ProxyUserPassword', type=str, default=None, required=False, help= 'Password for the "proxy" account')
    parser.add_argument('-spid','--SystemProfileId', type=str, default=None, required=False, help= 'The resource profile ID for systems with ComputerClass CustomSsh')
    parser.add_argument('-aalam','--AllowAutomaticLocalAccountMaintenance', type=str, default=None, required=False, help= 'Allow local account automatic maintenance using a privileged account')
    parser.add_argument('-n','--Name', type=str, required=True, help= 'Display name of the system')
    return parser.parse_args()
if __name__ == "__main__":
    args = vars(cl())
def add_account():
    new_args = dict((k, v) for k, v in args.items() if v != None)
    log.info("Using endpoint /ServerManage/AddResource...")
    log.info('Using argument values: {0}'.format(new_args))
    try:
        log.info("Adding system resource: {0}.....".format(args['FQDN']))
        req = other_requests(Call="/ServerManage/AddResource", **new_args, Debug=True)
        req.parsed_json['Result'] == False
        log.info("Added system resource: {0}".format(args['FQDN']))
    except:
        log.error("An Internal error occured during /ServerManage/AddResource. Please check logs")
add_account()
