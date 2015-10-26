#!/usr/bin/env python
# encoding: utf-8

TAG = "[MethodExtractor] "

class MethodExtractor:

    def __init__(self, file_path, module_list):
        self.file_path = file_path
        self.module_list = module_list

    def extract(self):
        for line in open(self.file_path):
           # 判断将每个method存入一个链表中以供后用
