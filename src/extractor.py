#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import string
import shutil
from src.method_extractor import MethodExtractor
from src.invoke_extractor import InvokeExtractor

TAG = "[Extractor] "

class Extractor:

    def __init__(self, jar_path):
        self.jar_path = jar_path
        self.tool_path = os.getcwd()

    # 启动解析
    def start(self):
        self.__create_tmp_dirs()
        self.read_ignore_config()
        #  self.uncompress_jar()
        #  self.decode_class()
        #  self.extract()
        #  self.generate_output()

    def extract(self):
        self.extract_android_module()
        self.print_modules()
        self.extract_method()
        self.extract_invoke()

    # 创建相应tmp目录存储生成的缓存文件
    def __create_tmp_dirs(self):
        print (TAG.join('create tmp dirs in'))
        file_name = os.path.basename(self.jar_path)
        jar_name = os.path.splitext(file_name)[0]
        self.tmp_path = os.path.join(self.tool_path, jar_name + '_tmp')
        if os.path.exists(self.tmp_path):
            shutil.rmtree(self.tmp_path)
        os.mkdir(self.tmp_path)
        self.class_dir = os.path.join(self.tmp_path, 'class')
        os.mkdir(self.class_dir)
        self.jad_dir = os.path.join(self.tmp_path, 'jad')
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

    # 通过import语句提取使用了哪些Android模块
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

    # 提取包含Android模块的方法
    def extract_method(self):
        self.method_collection = dict()
        for file_path, module_list in self.android_modules.items():
            # if os.path.basename(file_path) == 'a.java':
            method_extractor = MethodExtractor(file_path)
            method_extractor.extract(module_list)
            self.method_collection[file_path] = method_extractor
        return self.method_collection

    # 提取收集调用语句
    def extract_invoke(self):
        self.file_invoke_collection = dict()
        for file_path, method_extractor in self.method_collection.items():
            module_invoke_dict = dict()
            for module, method_list in method_extractor.module_method_dict.items():
                invoke_extractor = InvokeExtractor(module, method_list)
                invoke_extractor.collect_invoke()
                invoker_list = list()
                invoker_list.append(invoke_extractor)
                module_invoke_dict[module] = invoker_list
            self.file_invoke_collection[file_path] = module_invoke_dict

    def print_modules(self):
        print ('\n***************** MODULE OUTPUT *****************')
        for file_name, module_list in self.android_modules.items():
            print ('<%s>' % (file_name))
            print (module_list)
            print ('')

    def generate_output(self):
        output_path = os.path.join(self.tmp_path, 'output')
        if os.path.exists(output_path):
            os.remove(output_path)
        output_file = open(output_path, 'wa')
        for file_path, module_invoke_dict in self.file_invoke_collection.items():
            output_file.write('<%s>\n' % (file_path))
            for module, invoker_list in module_invoke_dict.items():
                output_file.write('    [%s]\n' % (module))
                for invoke_extractor in invoker_list:
                    for line in invoke_extractor.static_invoke_list:
                        output_file.write('        %s\n' % (line))
                    for line in invoke_extractor.obj_invoke_list:
                        output_file.write('        %s\n' % (line))
        output_file.close()

    def read_ignore_config(self):
        config_path = os.path.join(self.tool_path, 'ignore.cfg')
        for line in open(config_path):
            if line:
                print line
        pass
