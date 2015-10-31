#!/usr/bin/env python
# encoding: utf-8

TAG = "[MethodExtractor] "

class MethodExtractor:

    def __init__(self, file_path):
        self.file_path = file_path
        self.method_list = list()
        self.module_method_dict = dict()

    def __collect(self):
        temp = 0
        method_item = list()
        for line in open(self.file_path):
            line = line.strip()
            # 不检查注释开头的行
            if line and line[0] != '/':
                # 方法头，以p开头和)结尾，如 private void foo()
                if line[-1] == ')' and line[0] == 'p':
                # if line[-1] == ')':
                    method_item = list()
                    method_item.append(line)
                    # 用于表示匹配{}的临时变量
                    temp = 1
                else:
                    if temp > 0:
                        method_item.append(line)
                        if '{' in line:
                            temp += 1
                        if '}' in line:
                            temp -= 1
                            if temp == 1:
                                temp = 0
                                self.method_list.append(method_item)
        # print self.method_list

    def extract(self, module_list):
        self.__collect()
        for module in module_list:
            methods = list()
            for method in self.method_list:
                for line in method:
                    if module in line:
                        methods.append(method)
                        self.module_method_dict[module] = methods
        # print self.module_method_dict
