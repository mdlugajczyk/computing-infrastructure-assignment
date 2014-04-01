import argparse
from lib.saga_service.filesystem_service import FilesystemService
from lib.command.command_template import CommandTemplate

class CopyCommand(CommandTemplate):
    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-f", help="Overwrites existing file.",
                            action="store_true")
        parser.add_argument("sources", nargs="+")
        parser.add_argument("destination", nargs=1)
        self.args = parser.parse_args()        

    def execute_command(self):
        service = FilesystemService()
        if self.args.f:
            service.copy_and_overwrite(self.args.sources,
                                       self.args.destination[0])
        else:
            service.copy(self.args.sources, self.args.destination[0])
