#!/usr/bin/python

# Written By - Rishabh Das <rishabh5290@gmail.com>
#
# This program is a free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the license, or(at your option) any
# later version. See http://www.gnu.org/copyleft/gpl.html for the full text of
# the license.

##############################################################################

from ansible.playbook import PlayBook
from ansible.inventory import Inventory
from ansible import callbacks
from ansible import utils

import jinja2
from tempfile import NamedTemporaryFile
import os

utils.VERBOSITY = 4
playbook_cbck = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
stats = callbacks.AggregateStats()
runner_cbck = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)

# Dynamic Inventory Jinja 2 Template

inventory = """
[remote]
{% for ip in hosts %}
{{ ip }}
{% endfor %}
"""

# Render Inventory
# Change target machine IP
target = ['192.168.122.58']
inv_template = jinja2.Template(inventory)
render_inv = inv_template.render({
    'hosts': target
})

# Write Inventory File

hosts = NamedTemporaryFile(delete=False)
hosts.write(render_inv)
hosts.close()

# Call Ansible play

playobj = PlayBook(
        playbook='dmidecode.yaml',
        host_list=hosts.name,
        remote_user='rdas',
        stats=stats,
        callbacks=playbook_cbck,
        runner_callbacks=runner_cbck,
        private_key_file='~/.ssh/id_rsa'
)
playresult = playobj.run()

# Remove Temporary Inventory File
os.remove(hosts.name)

# Print aggregated Results
print playresult
