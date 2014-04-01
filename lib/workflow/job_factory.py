from lib.command.list_command import ListCommand
from lib.command.cat_command import CatCommand
from lib.command.copy_command import CopyCommand
from lib.command.remove_command import RemoveCommand
from lib.command.exec_command import ExecCommand

class JobFactory:

    def __init__(self, filesystem, job_submission):
        self._filesystem = filesystem
        self._job_submission = job_submission
        self._commands_mapping = {"ls": ListCommand,
                                  "cat": CatCommand,
                                  "copy": CopyCommand,
                                  "rm": RemoveCommand,
                                  "exec": ExecCommand}

    def create_job(self, cmd, args):
        cls = self._commands_mapping[cmd]
        command = cls(filesystem=self._filesystem,
                      job_submission=self._job_submission)
        command.parse_args(args.split())
        return command
