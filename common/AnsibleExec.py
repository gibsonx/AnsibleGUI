# !/usr/bin/env python

import json
import logging as logger
import os,sys
from common.InventoryGen import DynamicInventory
from common.ResultCallback import ADhocCallback,PlayBookCallback
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible import constants
from ansible.plugins.callback import CallbackBase
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor


class AnsibleExec():
    def __init__(self,resource=None):
        self.Options = namedtuple('Options',
                                  ['connection',
                                   'remote_user',
                                   'ask_sudo_pass',
                                   'verbosity',
                                   'ack_pass',
                                   'module_path',
                                   'forks',
                                   'become',
                                   'become_method',
                                   'become_user',
                                   'check',
                                   'listhosts',
                                   'listtasks',
                                   'listtags',
                                   'syntax',
                                   'sudo_user',
                                   'sudo',
                                   'diff'])

        self.ops = self.Options(connection='smart',
                                remote_user=None,
                                ack_pass=None,
                                sudo_user=None,
                                forks=5,
                                sudo=None,
                                ask_sudo_pass=False,
                                verbosity=5,
                                module_path=None,
                                become=None,
                                become_method=None,
                                become_user=None,
                                check=False,
                                diff=False,
                                listhosts=None,
                                listtasks=None,
                                listtags=None,
                                syntax=None)
        self.resource = resource
        self.loader = DataLoader()
        self.passwords = dict()


        #self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.inventory = InventoryManager(loader=self.loader, sources=['/etc/ansible/inventory/hosts'])
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        if self.resource:
            dynamicinventory = DynamicInventory(self.resource)
            self.variable_manager = dynamicinventory.variable_manager
            self.inventory = dynamicinventory.inventory



    def runansible(self, host_list, task_list):
        self.results_callback = ADhocCallback()
        '''
         ansible group1 -m shell -a 'ls /tmp'
        '''
        play_source = dict(
            name="Ansible Play",
            hosts=host_list,
            gather_facts='no',
            tasks=task_list
        )
        # play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
        play = Play().load(play_source,
                           variable_manager=self.variable_manager,
                           loader=self.loader)
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.ops,
                passwords=self.passwords,
                run_tree=False,
                stdout_callback=self.results_callback
            )
            tqm.run(play)
            # tqm._stdout_callback = self.results_callback
            constants.HOST_KEY_CHECKING = False
            self.results_raw = self.results_callback.result_row
        except Exception as err:
            print(err)
        finally:
            if tqm is not None:
                tqm.cleanup()

    def run_playbook(self, playbookpath):
        print('playbook Host参数:%s' % self.inventory.get_groups_dict())
        host = self.inventory.get_host(hostname='localhost')
        print('playbook vars参数:%s' % self.variable_manager.get_vars(host=host))
        self.results_callback = PlayBookCallback()
        try:
            # self.variable_manager.extra_vars = extra_vars
            executor = PlaybookExecutor(
                playbooks=[playbookpath],
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.ops,
                passwords=self.passwords,
            )
            executor._tqm._stdout_callback = self.results_callback
            constants.HOST_KEY_CHECKING = False  # 关闭第一次使用ansible连接客户端是输入命令
            executor.run()
            self.results_raw = self.results_callback.result_row
        except Exception as err:
            print (err)
            return err
