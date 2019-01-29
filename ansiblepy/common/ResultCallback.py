from ansible.plugins.callback import CallbackBase
import os
import sys
import logging
import json
import shutil

class ResultsCollector(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result,**kwargs):
        self.host = result._host
        print(json.dumps({self.host.name: result._result}, indent=4))

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host = result._host
        print(json.dumps({self.host.name: result._result}, indent=4))

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host = result._host
        print(json.dumps({self.host.name: result._result}, indent=4))

