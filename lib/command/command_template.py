from lib.saga_service.filesystem_service import FilesystemService
from lib.saga_service.job_submission_service import JobSubmissionService
from lib.exception.file_exists_exception import FileExistsException


class CommandTemplate:
    """
    Template for a Unix like command running on GRID using SAGA library.
    """

    def __init__(self, filesystem=FilesystemService(),
                 job_submission=JobSubmissionService()):
        """
        Creates new instance of CommandTemplate.

        :param filesystem: Service for performing filesystem operations on GRID
        :param job_submission: Service for submitting jobs to GRID
        """
        self._filesystem = filesystem
        self._job_submission = job_submission
        self.name = None

    def parse_args(self, args):
        """
        Template method for parsing command arguments.

        :param args: Arguments to parse.
        """
        raise Exception("Not implemented")

    def execute_command(self):
        """
        Template method for executing the command.
        """
        raise Exception("Not implemented")

    def run(self):
        """
        Runs the command using template methods for executing it,
        and parsing its arguments.

        All exceptions are catched.
        """
        try:
            self.parse_args(None)
            self.execute_command()
        except FileExistsException, e:
            print "Can't copy file as destination already exists."
            print "Exiting..."
        except Exception, e:
            print "Exception occured: %s\nExiting..." % e

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.name == other.name)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)
                           
