#!/usr/bin/env python

from lib.saga_service.job_submission_service import JobSubmissionService
from lib.saga_service.filesystem_service import FilesystemService
from lib.command.command_template import CommandTemplate
import argparse


class ExecCommand(CommandTemplate):
    
    def parse_args(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument("-r", help="Connection string.",
                            nargs=1, required=True)
        parser.add_argument("-stdin", help="Command's input file.", nargs=1)
        parser.add_argument("-stdout", help="Command's output file.",
                            nargs=1)
        parser.add_argument("command",
                            help="Command to invoke.",
                            nargs=1)
        parser.add_argument("arguments", help="Command's arguments.",
                            nargs="*")
        self.args = parser.parse_args(args)

    def execute_command(self):
        input_file = None
        output_file = None
        if self.args.stdin is not None:
            input_file = self.args.stdin[0]
        if self.args.stdout is not None:
            output_file = self.args.stdout[0]
        arguments = " ".join(self.args.arguments)
        output = self._job_submission.submit_job(self.args.command[0],
                                                 arguments,
                                                 input_file,
                                                 output_file,
                                                 self.args.r[0])
        if output:
            print output
