#!/usr/bin/env python

from filesystem_service import FilesystemService
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", help="File to which output will be written.")
    parser.add_argument("inputs", nargs="+")
    return parser.parse_args()

def main():
    args = parse_args()
    service = FilesystemService()
    if args.o:
        service.cat_to_file(args.inputs, args.o)
    else:
        print service.cat(args.inputs)

if __name__ == '__main__':
    main()

    
