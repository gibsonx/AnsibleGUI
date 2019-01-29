from ansiblepy.common.AnsibleExec import AnsibleExec



if __name__ == '__main__':
    current_run = AnsibleExec()
    host_list = ['localhost']
    task_list = [
            dict(action=dict(module='shell', args='ls')),
            dict(action=dict(module='shell', args='pwd')),
         ]
    current_run.runansible(host_list,task_list);
    # current_run.get_result()
