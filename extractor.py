#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import shutil

TOOL_PATH = os.getcwd()

def create_tmp_dirs():
    print ("create tmp dirs in")
    if len(sys.argv) == 2:
        jar_path = sys.argv[1]
    else:
        print ('miss input path!')
    file_name = os.path.basename(jar_path)
    jar_name = os.path.splitext(file_name)[0]
    tmp_path = TOOL_PATH + '/' + jar_name + '_tmp'
    if os.path.exists(tmp_path):
        shutil.rmtree(tmp_path)
    os.mkdir(tmp_path)

def main():
    print ('extractor main in')
    create_tmp_dirs()

if __name__ == '__main__':
    main()
