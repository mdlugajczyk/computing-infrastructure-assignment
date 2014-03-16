#!/usr/bin/env python

import sys
from filesystem_service import FilesystemService

def parse_args():
    if len(sys.argv) != 2:
        print "Usage: %s dir_name" % sys.argv[0]
        sys.exit(1)
    return sys.argv[1]

def main():
    dir_name = parse_args()
    service = FilesystemService()
    for entry in service.list_dir(dir_name):
        print entry
    
if __name__ == '__main__':
    main()
