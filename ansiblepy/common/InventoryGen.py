# -- coding:utf8 --

import os
import sys
import logging
logger = logging.getLogger('django')

# from collections import namedtuple
import json
import shutil
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
import ansible.constants as C


class DynamicInventory(InventoryManager,VariableManager):

  def __init__(self, resource, loader, variable_manager):

    '''
    @resource:
    {
        "group1": {
            "hosts": [{"hostname": "10.0.0.0", "port": "22", "username": "test", "password": "pass"}, ...],
            "vars": {"var1": value1, "var2": value2, ...}
        }
    }
    '''

    self.resource = resource
    self.variable_manager = VariableManager
    self.inventory = InventoryManager(loader=loader, variable_manager=variable_manager, host_list=[])
    self.gen_inventory()
  #
  # def Dynamic_add_group(self, hosts, groupname, groupvars=None):
  #
  #       '''
  #   Dynamic generate group list of ansible inventory
  #   :param hosts:
  #   :param groupname:
  #   :param groupvars:
  #   :return:
  #   '''
  #
  #   NewGroup = Group(name=groupname)
  #
  #   if groupvars:
  #       for key, value in groupvars.iteritems():
  #           NewGroup.set_variable(key, value)
  #
  #   for host in hosts:
  #       hostname = host.get("hostname")
  #       hostport = host.get("port")
  #       username = host.get("username")
  #       password = host.get("password")
  #       # ssh_key = host.get("ssh_key")
  #       GeneralHost = Host(name=hostname, port=hostport)
  #       GeneralHost.set_variable('ansible_ssh_host', hostname)
  #       GeneralHost.set_variable('ansible_ssh_port', hostport)
  #       GeneralHost.set_variable('ansible_ssh_user', username)
  #       GeneralHost.set_variable('ansible_ssh_pass', password)
  #       # GeneralHost.set_variable('ansible_ssh_private_key_file', ssh_key)
  #
  #       for key, value in host.iteritems():
  #           if key not in ["hostname", "port", "username", "password"]:
  #               GeneralHost.set_variable(key, value)
  #       NewGroup.add_host(GeneralHost)
  #
  #       return self.inventory.add_group(NewGroup)
  #
  # def gen_inventory(self):
  #
  #   '''
  #   Dynamic generate host inventory of ansible
  #   :return:
  #   '''
  #
  #   if isinstance(self.resource, list):
  #       self.Dynamic_add_group(self.resource, 'default_group')
  #   elif isinstance(self.resource, dict):
  #       for groupname, hosts_and_vars in self.resource.iteritems():
  #           self.Dynamic_add_group(hosts_and_vars.get("hosts"), groupname, hosts_and_vars.get("vars"))