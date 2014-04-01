#!/usr/bin/env python

import argparse
from lib.command.command_template import CommandTemplate
from lib.saga_service.filesystem_service import FilesystemService


class ListCommand(CommandTemplate):

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("dir_name", help="Directory name")
        self.args = parser.parse_args()

    def execute_command(self):
        service = FilesystemService()
        for entry in service.list_dir(self.args.dir_name):
            print entry
