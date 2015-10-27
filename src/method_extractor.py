#!/usr/bin/env python
# encoding: utf-8

TAG = "[MethodExtractor] "

class MethodExtractor:

    def __init__(self, file_path):
        self.file_path = file_path

    def extract(self):
        __temp = 0
        method_item = list()
        for line in open(self.file_path):
            line = line.strip()
            # 不检查注释开头的行
            if line and line[0] != '/':
                if line[-1] == ')' and line[0] == 'p':
                    method_item = list()
                    method_item.append(line)
                    __temp = 1
                else:
                    if __temp > 0:
                        method_item.append(line)
                        if line == '{':
                            __temp += 1
                        if line == '}':
                            __temp -= 1
                            if __temp == 1:
                                __temp == 0
                                print method_item
            pass
