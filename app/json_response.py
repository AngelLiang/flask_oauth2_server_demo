# coding=utf-8

import copy
from flask import request


class JsonResponse(object):

    success_dict = {"status": 1, "messge": "success!"}

    fail_dict = {"status": 0, "messge": "fail!"}

    miss_param = {"status": -1, "messge": "miss parameters!"}

    def deepcopy_and_update(self, json_dict: dict, data):
        temp = copy.deepcopy(json_dict)
        temp.update({"request": request.base_url, "data": data or {}})
        return temp

    def make_success(self, data=None) -> dict:
        return self.deepcopy_and_update(self.success_dict, data)

    def make_fail(self, data=None) -> dict:
        return self.deepcopy_and_update(self.fail_dict, data)

    def make_miss_param(self, data=None) -> dict:
        return self.deepcopy_and_update(self.miss_param, data)


singleton_json_response = JsonResponse()
