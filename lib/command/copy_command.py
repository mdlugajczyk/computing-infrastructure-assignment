import argparse
from lib.saga_service.filesystem_service import FilesystemService
from lib.command.command_template import CommandTemplate

class CopyCommand(CommandTemplate):

    def parse_args(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument("-f", help="Overwrites existing file.",
                            action="store_true")
        parser.add_argument("sources", nargs="+")
        parser.add_argument("destination", nargs=1)
        self.args = parser.parse_args(args)

    def execute_command(self):
        if self.args.f:
            self._filesystem.copy_and_overwrite(self.args.sources,
                                                self.args.destination[0])
        else:
            self._filesystem.copy(self.args.sources,
                                  self.args.destination[0])
