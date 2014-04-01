#!/usr/bin/env python

import argparse
from lib.saga_service.filesystem_service import FilesystemService
from lib.command.command_template import CommandTemplate

class RemoveCommand(CommandTemplate):
    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("files", help="Files to remove.", nargs="+")
        self.args = parser.parse_args()
        
    def execute_command(self):
        service = FilesystemService()
        service.remove(self.args.files)
