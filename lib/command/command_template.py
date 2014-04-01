from lib.saga_service.exceptions.file_exists_exception import FileExistsException


class CommandTemplate:

    def parse_args(self):
        pass

    def execute_command(self):
        pass

    def run(self):
        try:
            self.parse_args()
            self.execute_command()
        except FileExistsException, e:
            print "Can't copy file as destination already exists."
            print "Exiting..."
        except Exception, e:
            print "Exception occured: %s\nExiting..." % e
