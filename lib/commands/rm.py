#!/usr/bin/env python

import sys
from filesystem_service import FilesystemService

def main():
    if len(sys.argv) < 2:
        print "Usage: %s file1 file2... filen" % sys.argv[0]
        sys.exit(1)
    service = FilesystemService()
    service.remove(sys.argv[1:])

if __name__ == '__main__':
    main()
