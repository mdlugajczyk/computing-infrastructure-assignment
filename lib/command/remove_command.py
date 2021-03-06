#!/usr/bin/env python

import argparse
from lib.saga_service.filesystem_service import FilesystemService
from lib.command.command_template import CommandTemplate

class RemoveCommand(CommandTemplate):
    """
    A UNIX like rm command for removing files.

    Directories are not supported.
    """

    def parse_args(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument("files", help="Files to remove.", nargs="+")
        self.args = parser.parse_args(args)
        
    def execute_command(self):
        self._filesystem.remove(self.args.files)
