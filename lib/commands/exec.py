#!/usr/bin/env python

from saga_service.job_submission_service import JobSubmissionService
from saga_service.filesystem_service import FilesystemService
import argparse
import saga

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", help="Connection string.",
                        nargs=1, required=True)
    parser.add_argument("-stdin", help="Command's input file.", nargs=1)
    parser.add_argument("-stdout", help="Command's output file.", nargs=1)
    parser.add_argument("command",
                        help="Command to invoke.",
                        nargs=1)
    parser.add_argument("arguments", help="Command's arguments.", nargs="*")
    return parser.parse_args()

def main():
    args = parse_args()
    service = JobSubmissionService(saga, saga.job, FilesystemService())
    input_file = None
    output_file = None
    if args.stdin is not None:
        input_file = args.stdin[0]
    if args.stdout is not None:
        output_file = args.stdout[0]
        
    print service.submit_job(args.command, " ".join(args.arguments),
                             input_file, output_file, args.r[0])

if __name__ == '__main__':
    main()
