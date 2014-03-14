class FileExistsException(Exception):
    pass

    
class CopyService:

    def __init__(self, file_class, dir_class):
        self._file = file_class
        self._dir = dir_class

    def copy_and_overwrite(self, src, dst):
        for path in src:
            self._copy_file(path, dst)

    def copy(self, src, dst):
        dst_files = self._dir_content(dst)
        for file_path in src:
            if self._file_exists(file_path, dst_files):
                raise FileExistsException
            self._copy_file(file_path, dst)
        
    def _copy_file(self, src, dst):
        f = self._file(src)
        f.copy(dst)

    def _dir_content(self, path):
        directory = self._dir(path)
        return directory.list()

    def _file_name(self, file):
        return file.split("/")[-1]

    def _file_exists(self, file_path, dir_content):
        file_name = self._file_name(file_path)
        for f in dir_content:
            if f.path == file_name:
                return True
        return False
