# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import argparse
import os
import sys
def process_bmp ():
    parser = argparse.ArgumentParser(description='BMP reader')
    parser.add_argument('--bmp', metavar='<bmp file name>', help='image file to parse', default= 'image.bmp',required=True)
    args = parser.parse_args()
    file_name = args.bmp
    if not os.path.isfile(file_name):
        print('"{}" does not exist'.format(file_name), file=sys.stderr)
        sys.exit(-1)
    print('Success Opening {}...'.format(file_name))

if __name__ == '__main__':
    process_bmp()
    sys.exit(0)

