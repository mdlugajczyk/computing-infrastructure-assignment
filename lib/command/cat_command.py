from lib.saga_service.filesystem_service import FilesystemService
from lib.command.command_template import CommandTemplate
import argparse


class CatCommand(CommandTemplate):
    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-o",
                            help="File to which output will be written.")
        parser.add_argument("inputs", nargs="+")
        self.args = parser.parse_args()

    def execute_command(self):
        service = FilesystemService()
        if self.args.o:
            service.cat_to_file(self.args.inputs, self.args.o)
        else:
            print service.cat(self.args.inputs)
    
