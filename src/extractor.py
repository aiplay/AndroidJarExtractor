#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import string
import shutil
from src.method_extractor import MethodExtractor

TAG = "[Extractor] "

class Extractor:

    def __init__(self, jar_path):
        self.jar_path = jar_path
        self.tool_path = os.getcwd()

    def start(self):
        self.__create_tmp_dirs()
        self.uncompress_jar()
        self.decode_class()
        self.extract_android_module()
        # self.print_modules()
        self.extract_method()

# 创建相应tmp目录存储生成的缓存文件
    def __create_tmp_dirs(self):
        print (TAG.join('create tmp dirs in'))
        file_name = os.path.basename(self.jar_path)
        jar_name = os.path.splitext(file_name)[0]
        tmp_path = os.path.join(self.tool_path, jar_name + '_tmp')
        if os.path.exists(tmp_path):
            shutil.rmtree(tmp_path)
        os.mkdir(tmp_path)
        self.class_dir = os.path.join(tmp_path, 'class')
        os.mkdir(self.class_dir)
        self.jad_dir = os.path.join(tmp_path, 'jad')
        os.mkdir(self.jad_dir)

# 解压Jar包
    def uncompress_jar(self):
        os.chdir(self.class_dir)
        os.system('jar xf ' + self.jar_path)

# 利用jad工具反编译class文件
    def decode_class(self):
        shutil.copy(os.path.join(self.tool_path, 'jad'), self.jad_dir)
        os.chdir(self.jad_dir)
        list_files = os.walk(self.class_dir)
        for root, dirs, files in list_files:
            for f in files:
                if os.path.splitext(f)[1] == '.class':
                    cmd = './jad -o -r -s java ' + os.path.join(root, f)
                    os.popen(cmd)

    def extract_android_module(self):
        list_files = os.walk(self.jad_dir)
        self.android_modules = dict()
        for root, dirs, files in list_files:
            for f in files:
                for line in open(os.path.join(root, f)):
                    line = line.strip('\n')
                    head = string.strip(line, ' ')[0:6]
                    if head == 'import':
                        package = string.splitfields(line.strip(';'), ' ')[1]
                        if 'android' in package:
                            module = string.splitfields(package, '.')[-1]
                            if module != '*':
                                file_key = os.path.join(root, f)
                                module_list = self.android_modules.get(file_key) or []
                                module_list.append(module)
                                self.android_modules[file_key] = module_list
        return self.android_modules

    def extract_method(self):
        list_files = os.walk(self.jad_dir)
        for root, dirs, files in list_files:
            for f in files:
                if f == 'b.java':
                    method_extractor = MethodExtractor(os.path.join(root, f))
                    method_extractor.extract()

    def print_modules(self):
        print ('\n***************** MODULE OUTPUT *****************')
        for file_name, module_list in self.android_modules.items():
            print ('<%s>' % (file_name))
            print (module_list)
            print ('')

# def check_module(line, module):
    # chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # index = line.find(module)
    # if index > 0:
        # return line[line.find(module) - 1] not in chars
    # else:
        # return True

# def search_method():
    # global output__
    # for module in android_modules__.keys():
        # if module != "View":
            # continue
        # file_info = {}
        # for file in android_modules__.get(module):
            # obj_info = {}
            # for line in open(file):
                # if 'import' not in line and 'implements' not in line and module in line:
                    # index = string.find(line, module, 0, -1)
                    # if index != -1:
                        # if not check_module(line, module):
                            # continue
                        # start = index + len(module) + 1
                        # end = line.find(' ', start, -1)
                        # if end == -1:
                            # end = line.find(';', start, -1)
                        # obj = string.strip(line[start:end])
                        # if obj[-1] == ')':
                            # obj = obj[0:len(obj) - 1]
                        # print ('obj : ' + obj)
                        # print ('line : ' + line)
                        # if ',' in obj:
                            # obj = obj[0:(obj.find(','))]
                        # if obj != '':
                            # obj_info[obj] = None
            # invoke_list = []
            # for obj in obj_info.keys():
                # for line in open(file):
                    # if 'import' not in line and 'implements' not in line and check_module(line, module):
                        # if obj + '.' in line:
                            # invoke_list.append(line)
                        # if module + '.' in line:
                            # invoke_list.append(line)
                # obj_info[obj] = invoke_list
            # file_info[file] = obj_info
        # file_list = output__.get(module) or []
        # file_list.append(file_info)
        # output__[module] = file_list
    # # print output__

# def generate_output():
    # output_path = TOOL_PATH + '/output'
    # if os.path.exists(output_path):
        # os.remove(output_path)
    # fp = open(output_path, 'wa')
    # for module, file_list in output__.iteritems():
        # fp.writelines('[' + module + ']\n')
        # for file_info in file_list:
            # for file, obj_info in file_info.iteritems():
                # fp.writelines('    <' + file + '>\n')
                # for obj, invoke_list in obj_info.iteritems():
                    # for invoke in invoke_list:
                        # fp.writelines('        ' + string.strip(invoke) + '\n')
    # fp.close()


# # def main():
    # # print ('extractor main in')
    # # create_tmp_dirs()
    # # uncompress_jar()
    # # decode_class()
    # # extract_android_module()
    # # search_method()
    # # generate_output()
