class FileExistsException(Exception):
    """
    An exception thrown when destination of copy already exists and
    flag "-f" has not been supplied.
    """

    def __init__(self):
        super(FileExistsException, self).__init__("File aready exists.")
