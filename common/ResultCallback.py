from ansible.plugins.callback import CallbackBase
import os
import sys
import logging
import json
import shutil

class PlayBookCallback(CallbackBase):
    # CALLBACK_VERSION = 2.0
    def __init__(self, *args, **kwargs):
        super(PlayBookCallback, self).__init__(*args, **kwargs)
        self.result_row = {'ok': {}, 'failed': {}, 'unreachable': {}, 'skipped': {}, 'status': {}}

    def v2_runner_on_ok(self, result, *args, **kwargs):
        # print(result._host.get_name())
        # print("run on ok %s"%result._result)
        self.result_row['ok'][result._host.get_name()] = result._result

    def v2_runner_on_unreachable(self, result, *args, **kwargs):
        self.result_row['unreachable'][result._host.get_name()] = result._result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.result_row['failed'][result._host.get_name()] = result._result

    def v2_runner_on_skipped(self, result):
        self.result_row['skipped'][result._host.get_name()] = result._result

    def v2_playbook_on_stats(self, stats):
        # print(stats)
        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)
            self.result_row['status'][h] = {
                "ok": t['ok'],
                "changed": t['changed'],
                "unreachable": t['unreachable'],
                "skipped": t['skipped'],
                "failed": t['failures']
            }


class ADhocCallback(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ADhocCallback, self).__init__(*args, **kwargs)
        self.result_row={'ok':{},'failed':{},'unreachable':{}}

    def v2_runner_on_ok(self, result,  *args, **kwargs):
        self.result_row['ok'][result._host.get_name()] = result._result
        logging.info('===v2_runner_on_ok===host=%s===result=%s' % (result._host.get_name(), result._result))


    def v2_runner_on_unreachable(self, result,*args,**kwargs):
        self.result_row['unreachable'][result._host.get_name()]=result._result

    def v2_runner_on_failed(self, result,  *args, **kwargs):
        self.result_row['failed'][result._host.get_name()]=result._result
    # def v2_runner_on_ok(self, result, **kwargs):
    #     """Print a json representation of the result
    #
    #     This method could store the result in an instance attribute for retrieval later
    #     """
    #     host = result._host
    #     print(json.dumps({host.name: result._result}, indent=4))