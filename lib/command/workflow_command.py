from lib.workflow.workflow_runner import WorkflowRunner
from lib.command.command_template import CommandTemplate
import argparse

class WorkflowCommand(CommandTemplate):

    def __init__(self):
        CommandTemplate.__init__(self)
        self.workflow_runner = WorkflowRunner(self._filesystem,
                                              self._job_submission)

    def parse_args(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument("input_file", help="Workflow file.")
        self.args = parser.parse_args(args)

    def execute_command(self):
        failed_jobs = self.workflow_runner.run(self.args.input_file)
        if failed_jobs:
            print "Following jobs have not been executed: %s" % failed_jobs
        
