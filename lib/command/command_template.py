from lib.saga_service.filesystem_service import FilesystemService
from lib.saga_service.job_submission_service import JobSubmissionService
from lib.exception.file_exists_exception import FileExistsException


class CommandTemplate:

    def __init__(self, filesystem=FilesystemService(),
                 job_submission=JobSubmissionService()):
        self._filesystem = filesystem
        self._job_submission = job_submission

    def parse_args(self, args):
        raise Exception("Not implemented")

    def execute_command(self):
        raise Exception("Not implemented")

    def run(self):
        try:
            self.parse_args(None)
            self.execute_command()
        except FileExistsException, e:
            print "Can't copy file as destination already exists."
            print "Exiting..."
        except Exception, e:
            print "Exception occured: %s\nExiting..." % e
