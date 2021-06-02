#!/usr/bin/env python3
from paspymod.funct_tools import query_request, other_requests, sanitizedict, rem_null
from paspymod.logger import logging as log
import argparse
import ast
import os 
import csv
# https://developer.centrify.com/reference#post_servermanage-updateresource
# Workaround to bug:
# CPSSUP-1047
# BE SURE TO USE A FILE AS THAT IS COMMA SEPARATED VALUE FILE AND NOT UTF ENCODED. WILL THROW OFF THE CSV HEADER READ. 
# May write something to handle that as a regex
def cl():
    parser = argparse.ArgumentParser(description="Update a resource.")
    #maybe query for ID? But what if the CU wants to update the name
    parser.add_argument('-n','--Name', type=str, required=False, help= 'Name of the system to query ID for.')
    parser.add_argument('-p','--Path', type=str, required=False, help= 'Path to a CSV file of the systems to update. Please follow the same structure as in example files.')
    parser.add_argument('-un','--UpdatedName', type=str, required=False, help= 'Updated Name of the system to update.')
    parser.add_argument('-cae','--CertAuthEnable', type=bool, required=False, help= 'Whether "Use My Account" is configured on this system.')
    parser.add_argument('-ldp','--LoginDefaultProfile', type=str, required=False, help= 'ID of the Default System Login Profile, which is used if no policy conditions match..')
    parser.add_argument('-ar','--AllowRemote', type=bool, required=False, help= 'System Security: Whether remote connections from a public network are allowed for this system')
    parser.add_argument('-pup','--ProxyUserPassword', type=str, required=False, help= 'Password for the "proxy" account.')
    parser.add_argument('-des','--Description', type=str, required=False, help= 'Any descriptive information for the system.')
    # API states string, but des states list?
    parser.add_argument('-pcl','--ProxyCollectionList', type=str, required=False, help= 'List of connector IDs for the system. Centrify agent for Linux provides another option to specify the connectors.')
    parser.add_argument('-dct','--DefaultCheckoutTime', type=int, required=False, help= 'Account Security: The number of minutes a checked out password is valid on this system. The default is 60 minutes.')
    parser.add_argument('-mp','--ManagementPort', type=int, required=False, help= 'Name of the system to update.')
    parser.add_argument('-st','--SessionType', type=str, required=False, help= 'Session type: Rdp, Ssh.')
    parser.add_argument('-phcd','--PasswordHistoryCleanUpDuration', type=int, required=False, help= 'Maintenance option: The number of days after which retired passwords should be deleted if the "AllowPasswordHistoryCleanUp" policy is set to true. Retired passwords that were last modified either equal to or greater than the number of days specified here will be deleted automatically. The minimum value is 90 days.')
    parser.add_argument('-pt','--Port', type=int, required=False, help= 'Port number for remote sessions.')
    parser.add_argument('-did','--DomainId', type=str, required=False, help= 'ID of the domain to which the system is joined.')
    parser.add_argument('-spid','--SystemProfileId', type=str, required=False, help= 'The resource profile ID for systems with ComputerClass CustomSsh.')
    parser.add_argument('-cc','--ComputerClass', type=str, required=False, help= 'Computer classes: Windows, Unix, CiscoIOS, CiscoNXOS, JuniperJunos, GenericSsh, WebSite, HpNonStopOS, IBMi, CheckPointGaia, PaloAltoNetworksPANOS, F5NetworksBIGIP, CiscoAsyncOS, VMwareVMkernel, CustomSsh.')
    parser.add_argument('-prd','--PasswordRotateDuration', type=str, required=False, help= 'Security option: The maximum number of days between password changes for managed accounts if the "AllowPasswordRotation" policy is set to true. The default is 90 days.')
    # Test this line
    parser.add_argument('-lr','--LoginRules', type=ast.literal_eval, required=False, help= 'List of Rules and Conditions that must be satisfied for successful login to the system..')
    #
    parser.add_argument('-pu','--ProxyUser', type=str, required=False, help= 'Name for the "proxy" account.')
    parser.add_argument('-f','--FQDN', type=str, required=False, help= 'Fully-qualified domain name or IP address of the system.')
    parser.add_argument('-amc','--AllowMultipleCheckouts', type=bool, required=False, help= 'Security option: Whether multiple users can have the same account password checked out at the same time.')
    parser.add_argument('-rpup','--ResetProxyUserPassword', type=bool, required=False, help= 'Rotate managed proxy user password')
    parser.add_argument('-tzid','--TimeZoneID', type=str, required=False, help= 'Time zone ID for the system. Valid time zone values can be found for a Windows system in the registry under the "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Time Zones" registry branch.')
    parser.add_argument('-mm','--ManagementMode', type=str, required=False, help= 'Account mangagement type (for Windows Remote Management (WinRM) or HTTPS): Unknown, Smb, WinRMOverHttp, WinRMOverHttps, HTTPS.')
    parser.add_argument('-aphc','--AllowPasswordHistoryCleanUp', type=bool, required=False, help= 'Maintenance option: Whether retired passwords should be deleted periodically.')
    # Again Docs state use a list, but the obj type in doc is string
    parser.add_argument('-ds','--DmcScopes', type=str, required=False, help= 'List of scopes limiting which APIs are allowed to be invoked by this machine credential. Scope is defined by name and contains a list of regular expressions')
    parser.add_argument('-aalam','--AllowAutomaticLocalAccountMaintenance', type=str, required=False, help= 'Allow local account automatic maintenance using a privileged account.')
    parser.add_argument('-doe','--DomainOperationsEnabled', type=bool, required=False, help= 'Whether to allow using the domain administrative account to enable zone role workflow requests for the system. If true, a valid "DomainId" setting must be set or specified.')
    parser.add_argument('-amlau','--AllowManualLocalAccountUnlock', type=bool, required=False, help= 'Allow local account manual unlock using a privileged account.')
    parser.add_argument('-zrwe','--ZoneRoleWorkflowEnabled', type=bool, required=False, help= 'Whether to enable zone role workflow requests for the system. The default setting is to use the zone role workflow settings defined for the domain. If true, the "DomainOperationsEnabled" setting must be set to true..')
    parser.add_argument('-mpa','--MinimumPasswordAge', type=int, required=False, help= 'Security option: Minimum number of days that a managed password must have been in use before it can be rotated.')
    parser.add_argument('-apr','--AllowPasswordRotation', type=bool, required=False, help= 'Security option: Whether managed passwords should be changed periodically.')
    parser.add_argument('-ppid','--PasswordProfileID', type=str, required=False, help= 'Security option: ID of the password complexity profile for this system.')
    parser.add_argument('-puim','--ProxyUserIsManaged', type=bool, required=False, help= 'Whether the password for the "proxy" account is managed.')
    return parser.parse_args()

if __name__ == "__main__":
    args = vars(cl())
#
# ID 80387657-f747-484a-bd3f-59f4f63f6955
# WIN-70IF3OOSIPG

new_cl_args = rem_null(args)

# Specifically for bulk change on the command line

if args['Path']:
    path = os.path.abspath(args['Path'])
    log.info("Path to the csv file to add resources is: {0}".format(path))
    with open(path, 'r') as f:
        d_reader = csv.DictReader(f)
        for line in d_reader:
            log.info("Querying for ID to use on system whose name is: {0}".format(line['Name']))
            id_q = query_request(sql = "Select Server.ID From Server Where Server.Name = '{0}'".format(line['Name'])).parsed_json
            if id_q["Result"]["Count"] == 0:
                log.error("System not found")
            else:
                id = id_q["Result"]["Results"][0]["Row"]['ID']
            query = query_request(sql = "Select * From Server Where Server.ID = '{0}'".format(id)).parsed_json
            for x in query["Result"]["Results"]:
                if x["Row"] != None:
                    wanted = x["Row"]
            new_args = rem_null(wanted)
            new_args.update(new_cl_args)
            log.info("Updated args are: {0}".format(new_args))
            other_requests(Call='/ServerManage/UpdateResource', **new_args, Debug=True)

elif args['Name']:
    log.info("Querying for ID to use on system whose name is: {0}".format(args['Name']))
    id_q = query_request(sql = "Select Server.ID From Server Where Server.Name = '{0}'".format(args['Name'])).parsed_json
    if id_q["Result"]["Count"] == 0:
        log.error("System not found")
    else:
        id = id_q["Result"]["Results"][0]["Row"]['ID']
    log.info("SQL Querying to get the values of to pack into request.")
    query = query_request(sql = "Select * From Server Where Server.ID = '{0}'".format(id)).parsed_json
    for x in query["Result"]["Results"]:
        if x["Row"] != None:
            wanted = x["Row"]
    new_args = rem_null(wanted)
    log.info("Args for the server are: {0}".format(new_args.items()))
    new_args.update(new_cl_args)
    other_requests(Call='/ServerManage/UpdateResource', **new_args, Debug =True)

else:
    log.error("No valid input")