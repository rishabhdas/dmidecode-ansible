#!/usr/bin/python

# Written By - Rishabh Das <rishabh5290@gmail.com>
#
# This program is a free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the license, or(at your option) any
# later version. See http://www.gnu.org/copyleft/gpl.html for the full text of
# the license.

##############################################################################

DOCUMENTATION = '''
---
module: dmidecode
version_added: "0.1"
short_description: Get dmidecode information for your infrastructure.
description:
    - Get the dmidecode information of your infrastructure.
options:
    save:
        description:
            - Store dmidecode output to dmidecode.json in user home directory.
        default: False

'''

EXAMPLES = '''
# dmidecode module takes in 'save' as a paramter. If set True,
# this stores the dmidecode JSON output on the target machine.
# This by default is set to False.

# Usage Examples -

- name: Get dmidecode data
  action: dmidecode

- name: Get dmidecode data and save to file
  action: dmidecode save=True

'''

import dmidecode
import json

def get_bios_specs():
    BIOSdict = {}
    BIOSlist = []
    for item in dmidecode.bios().values():
        if type(item) == dict and item['dmi_type'] == 0:
            BIOSdict["Name"] = str((item['data']['Vendor']))
            BIOSdict["Description"] = str((item['data']['Vendor']))
            BIOSdict["BuildNumber"] = str((item['data']['Version']))
            BIOSdict["SoftwareElementID"] = str((item['data']['BIOS Revision']))
            BIOSdict["primaryBIOS"] = "True"
            BIOSlist.append(BIOSdict)
    return BIOSlist


def get_proc_specs():
    PROCdict = {}
    PROClist = []
    for item in dmidecode.processor().values():
        if type(item) == dict and item['dmi_type'] == 4:
            PROCdict['Vendor'] = str(item['data']['Manufacturer']['Vendor'])
            PROCdict['Version'] = str(item['data']['Version'])
            PROCdict['Thread Count'] = str(item['data']['Thread Count'])
            PROCdict['Characteristics'] = str(item['data']['Characteristics'])
            PROCdict['Core Count'] = str(item['data']['Core Count'])
            PROClist.append(PROCdict)
    return PROClist


def get_system_specs():
    SYSdict = {}
    SYSlist = []
    for item in dmidecode.system().values():
        if item['dmi_type'] == 1:
            SYSdict['Manufacturer'] = str(item['data']['Manufacturer'])
            SYSdict['Family'] = str(item['data']['Family'])
            SYSdict['Serial Number'] = str(item['data']['Serial Number'])
            SYSlist.append(SYSdict)
    return SYSlist


def main():
    module = AnsibleModule(
        argument_spec = dict(
            save = dict(required=False, default=False, type='bool'),
        )
    )
    dmi_data = json.dumps({
        'Hardware Specs' : {
            'BIOS' : get_bios_specs()[0],
            'Processor' : get_proc_specs()[0],
            'System' : get_system_specs()[0]
        }
    })
    save = module.params.get('save')
    if save:
        with open('dmidecode.json', 'w') as dfile:
            dfile.write(str(dmi_data))
    module.exit_json(changed=True, msg=str(dmi_data))


from ansible.module_utils.basic import *
main()
