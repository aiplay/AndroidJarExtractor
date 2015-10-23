#!/usr/bin/env python
# encoding: utf-8

import os
import sys
from src.extractor import Extractor

def main():
    if len(sys.argv) == 2:
        jar_path = sys.argv[1]
    else:
        print ('[ERROR] jar path need input!')
        return
    extractor = Extractor(jar_path)
    extractor.start()

if __name__ == '__main__':
    main()
