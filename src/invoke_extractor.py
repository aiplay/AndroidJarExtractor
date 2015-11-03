#!/usr/bin/env python
# encoding: utf-8

TAG = "[InvokeExtractor] "

class InvokeExtractor:

    def __init__(self, module, method_list):
        self.module = module
        self.method_list = method_list

    def collect_invoke(self):
        self.get_static_invoke(self.module, self.method_list)
        self.get_obj_invoke(self.module, self.method_list)

    def get_static_invoke(self, module, method_list):
        self.static_invoke_list = list()
        for method in method_list:
            for line in method:
                if module + '.' in line:
                    self.static_invoke_list.append(line)

    def get_obj_invoke(self, module, method_list):
        self.obj_invoke_list = list()
        for method in method_list:
            obj_list = self.get_obj(module, method)
            if obj_list:
                # print obj_list
                for obj in obj_list:
                    for line in method:
                        if obj in line:
                            # print line
                            self.obj_invoke_list.append(line)

    def get_obj(self, module, method):
        obj_list = list()
        for line in method:
            index = line.find(module)
            if index != -1:
                if index == 0 or line[index-1] in ['', ' ', ',', '(']:
                    start = index + len(module)
                    if line[start] != ' ':
                        continue
                    remain = line[index:len(line)].split(' ')
                    # print remain
                    for i, item in enumerate(remain):
                        if item == '':
                            continue
                        if item == module and i < len(remain) - 1:
                            obj = remain[i+1]
                            if obj[len(obj)-1] in [',', ')']:
                                obj = obj[:-1]
                            obj_list.append(obj)
        pass
        if len(obj_list) > 0:
            return obj_list

