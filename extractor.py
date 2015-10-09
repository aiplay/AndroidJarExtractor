#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import shutil

def create_tmp_dirs():
    print ("create tmp dirs in")
    jar_path = sys.argv[1]
    base = os.path.basename(jar_path)
    print (base)

def main():
    print ('extractor main in')
    create_tmp_dirs()

if __name__ == '__main__':
    main()
