from common.AnsibleExec import AnsibleExec
import json, sys, os
import logging

resource={'defualt':{'hosts':[{'hostid':'123','hostname':'localhost','hostip':'127.0.0.1','k1':'v1'},
                 ],
        'groupvars':{"gkey":"value"}},
    }


def RunAPI():
    task_list = [
      # dict(action=dict(module='shell', args='ls')),
      dict(action=dict(module='debug', args=dict(msg='{{ k1 }}'))),
    ]
    runner = AnsibleExec(resource)
    runner.runansible(host_list=['localhost'],task_list=task_list)
    result = runner.results_raw
    print(result)


def RunPlaybook():
    runner = AnsibleExec(resource)
    runner.run_playbook(playbookpath='/etc/ansible/test.yaml')
    result = runner.results_raw
    print(result)

if __name__ == '__main__':
    RunAPI()
    RunPlaybook()