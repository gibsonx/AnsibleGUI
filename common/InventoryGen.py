# -- coding:utf8 --

import os
import sys
import logging
logger = logging.getLogger('django')
import json, sys, os
import logging
from ansible import constants
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.inventory.host import Host, Group
from ansible.plugins.callback import CallbackBase
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor



class DynamicInventory(object):
    '''
    resource = [{'hostid': '1231', 'hostname': 'h1', 'hostip': '1.1.1.1'},
                {'hostid': '2345', 'hostname': 'h2', 'hostip': '2.2.2.2'},
                ]
    resource = {'groupname1': {
        'hosts': [
            {'hostid': '1231', 'hostname': 'h1', 'hostip': '1.1.1.1'},
            {'hostid': '2231', 'hostname': 'h2', 'hostip': '1.1.1.2'},
                 ],
        'groupvars': {"k1":"v1"}
                              },
                'groupname2': {'hosts': [], 'groupvars': {}},
                              }
    '''

    # edit ori code  ansible/inventory/manage.pay line215  try if C.InventoryManager_PARSE_NOSOURCE:pass
    constants.InventoryManager_PARSE_NOSOURCE = True

    def __init__(self, resource):
        self.resource = resource
        self.loader = DataLoader()
        # self.inventory=InventoryManager(loader=self.loader,sources=['/etc/ansible/inventory/hosts'])
        self.inventory = InventoryManager(loader=self.loader)
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self._parse(self.resource)

    def _parse(self, resource):
        if isinstance(resource, list):
            self._addGroupHosts(self.resource)
        elif isinstance(resource, dict):
            # logging.info('parsing resuorce: %s'%(self.resource))
            for groupname, hosts_and_groupvars in self.resource.items():
                print("[1] groupname: %s |hostsandvars: %s" % (groupname, hosts_and_groupvars))  # debug [1]
                self._addGroupHosts(hosts_and_groupvars.get('hosts'), groupname, hosts_and_groupvars.get('groupvars'))
        else:
            logging.error('resource error ,need dict or list')

    def _addGroupHosts(self, hosts, groupname=None, groupvars=None):
        self.inventory.add_group(group=groupname)
        group = Group(groupname)
        if groupvars:
            for k, v in groupvars.items():
                group.set_variable(k, v)


        # hosts=[{'hostid':'123','hostname':'h1','hostip':'192.168.188.20'}
        for host in hosts:
            hostid = host.get('hostid')
            hostname = host.get('hostname')
            hostip = host.get('hostip')
            username = host.get('username')
            password = host.get('password')
            port = host.get('port', 22)
            sshkey = host.get('sshkey')
            if hostname:
                self.inventory.add_host(host=hostname, group=groupname)  # by default, indentify by hostname and need
                hostobj = self.inventory.get_host(hostname=hostname)  # add host= , get hostname=

                self.variable_manager.set_host_variable(host=hostobj, varname='ansible_ssh_host', value=hostip)
                self.variable_manager.set_host_variable(host=hostobj, varname='ansible_ssh_port', value=port)
                self.variable_manager.set_host_variable(host=hostobj, varname='ansible_ssh_user', value=username)
                self.variable_manager.set_host_variable(host=hostobj, varname='ansible_ssh_pass', value=password)
                self.variable_manager.set_host_variable(host=hostobj, varname='ansible_ssh_private_key_file',
                                                        value=sshkey)

                # TODO: other vars such as become-method-user-pass
                # hostobj.set_variable('ansible_ssh_port',port)
                for k, v in host.items():
                    if k not in ['hostip', 'port', 'username', 'password', 'sshkey']:
                        hostobj.set_variable(k, v)
                        self.variable_manager.set_host_variable(host=hostobj, varname=k,value=v)
            else:
                logging.warning('resource error:cant get hostname from | %s' % self.resource)

    def testcase(self):
        print(self.inventory.get_groups_dict())
        host = self.inventory.get_host(hostname='h1')
        print(self.variable_manager.get_vars(host=host))
