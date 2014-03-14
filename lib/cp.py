import saga
import sys
from copy_service import CopyService

def parse_args():
    src = []
    dst = ""
    override = "-f" in sys.argv
    if override:
        sys.argv.remove("-f")
    if len(sys.argv) < 3:
        print "Usage: %s [-f] src1 ... srcN dst" % sys.argv[0]
        sys.exit(1)
    return sys.argv[1:-1], sys.argv[-1], override

def main():
    service = CopyService(saga.filesystem.File, saga.filesystem.Directory)
    src, dst, override = parse_args()
    if override:
        service.copy_and_overwrite(src, dst)
    else:
        service.copy(src, dst)
    
if __name__ == '__main__':
    main()




