# dmidecode-ansible
Extending Ansible, dmidecode module for ansible collects system information
<br/>
such as BIOS specs, Processor specs and System specs and returns results in
<br/>
JSON. This uses dmidecode Python API and Ansible Python API. <br/>

# Usage:

- Add remote machine IP to 'remote' section in hosts
- Play the ansible playbook

```sh
$ ansible-playbook -i hosts dmidecode.yaml
```
