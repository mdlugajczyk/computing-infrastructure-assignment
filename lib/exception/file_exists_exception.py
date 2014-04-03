class FileExistsException(Exception):

    def __init__(self):
        super(FileExistsException, self).__init__("File aready exists.")
