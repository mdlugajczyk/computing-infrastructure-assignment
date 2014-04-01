from lib.saga_service.filesystem_service import FilesystemService
from lib.command.command_template import CommandTemplate
import argparse


class CatCommand(CommandTemplate):

    def parse_args(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument("-o",
                            help="File to which output will be written.")
        parser.add_argument("inputs", nargs="+")
        self.args = parser.parse_args(args)

    def execute_command(self):
        if self.args.o:
            self._filesystem.cat_to_file(self.args.inputs, self.args.o)
        else:
            print self._filesystem.cat(self.args.inputs)
    
