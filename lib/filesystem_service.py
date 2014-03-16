from saga.exceptions import DoesNotExist
import saga

class FileExistsException(Exception):
    pass

    
class FilesystemService:
    
    def __init__(self, file_class=saga.filesystem.File,
                 dir_class=saga.filesystem.Directory):
        self._file = file_class
        self._dir = dir_class

    def copy_and_overwrite(self, src, dst):
        for path in src:
            self._copy_file(path, dst)

    def copy(self, src, dst):
        if self._is_directory(dst):
            self._copy_to_directory(src, dst)
        else:
            self._copy_to_file(src, dst)

    def remove(self, files):
        for path in files:
            f = self._file(path)
            f.remove(saga.filesystem.RECURSIVE)

    def cat_to_file(self, sources, destination):
        concat = self._concatenate_sources(sources)
        output = self._open_file(destination)
        output.write(concat)

    def cat(self, sources):
        return self._concatenate_sources(sources)

    def list_dir(self, directory_path):
        content = []
        for url in self._dir_content(directory_path):
            content.append(url.path)
        return content

    def _open_file(self, path):
        if self._file_exists(path):
            return self._file(path)
        else:
            return self._create_file(path)

    def _concatenate_sources(self, sources):
        concat = ""
        for path in sources:
            f = self._file(path)
            concat += self._read_file(f)
        return concat

    def _create_file(self, path):
        return self._file(path, flags=saga.filesystem.CREATE)

    def _is_directory(self, path):
        if self._file_exists(path):
            f = self._file(path)
            return not f.is_file()
        else:
            return False

    def _copy_to_file(self, src, dst):
        for f in src:
            if self._will_overwrite_file(f, dst):
                raise FileExistsException
            self._copy_file(f, dst)

    def _will_overwrite_file(self, src, dst):
        return self._file_exists(dst)
            
    def _copy_to_directory(self, src, dst):
        dst_files = self._dir_content(dst)
        for file_path in src:
            if self._file_exists_in_directory(file_path, dst_files):
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

    def _file_exists_in_directory(self, file_path, dir_content):
        file_name = self._file_name(file_path)
        for f in dir_content:
            if f.path == file_name:
                return True
        return False

    def _file_exists(self, path):
        exists = True
        try:
            f = self._file(path)
        except DoesNotExist:
            exists = False
        return exists

    def _read_file(self, f):
        # Workaround for Saga-Python issue #314
        content = None
        try:
            content = f.read()
        except IOError:
            content = f.read()
        return content
