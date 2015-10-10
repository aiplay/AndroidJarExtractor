#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import string
import shutil

# 脚本执行所在的工具目录
TOOL_PATH = os.getcwd()

# 传入的待解析的Jar的绝对路径
JAR_PATH = ''

# 解压出的class文件存放的目录
CLASS_DIR = ''

# 反编译生成的jad文件存放的目录
JAD_DIR = ''

info__ = {}

# 创建相应tmp目录存储生成的缓存文件
def create_tmp_dirs():
    print ("create tmp dirs in")
    global JAR_PATH, CLASS_DIR, JAD_DIR
    if len(sys.argv) == 2:
        JAR_PATH = sys.argv[1]
    else:
        print ('miss input path!')
    file_name = os.path.basename(JAR_PATH)
    jar_name = os.path.splitext(file_name)[0]
    tmp_path = os.path.join(TOOL_PATH, jar_name + '_tmp')
    if os.path.exists(tmp_path):
        shutil.rmtree(tmp_path)
    os.mkdir(tmp_path)
    CLASS_DIR = os.path.join(tmp_path, 'class')
    os.mkdir(CLASS_DIR)
    JAD_DIR = os.path.join(tmp_path, 'jad')
    os.mkdir(JAD_DIR)

# 解压Jar包
def uncompress_jar():
    os.chdir(CLASS_DIR)
    os.system('jar xf ' + JAR_PATH)

# 利用jad工具反编译class文件
def decode_class():
    shutil.copy(os.path.join(TOOL_PATH, 'jad'), JAD_DIR)
    os.chdir(JAD_DIR)
    list_files = os.walk(CLASS_DIR)
    for root, dirs, files in list_files:
        for f in files:
            if os.path.splitext(f)[1] == '.class':
                cmd = './jad -o -r ' + os.path.join(root, f)
                os.popen(cmd)

def extract_jad():
    list_files = os.walk(JAD_DIR)
    global info__
    for root, dirs, files in list_files:
        for f in files:
            for line in open(os.path.join(root, f)):
                line = line.strip('\n')
                head = string.strip(line, ' ')[0:6]
                if head == 'import':
                    package = string.splitfields(line.strip(';'), ' ')[1]
                    if 'android' in package:
                        module = string.splitfields(package, '.')[-1]
                        print module


def main():
    print ('extractor main in')
    create_tmp_dirs()
    uncompress_jar()
    decode_class()
    extract_jad()

if __name__ == '__main__':
    main()
