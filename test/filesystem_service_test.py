from lib.filesystem_service import FilesystemService
from lib.filesystem_service import FileExistsException
from mock import Mock
import unittest
from saga.exceptions import DoesNotExist
import saga

class FilesystemServiceTest(unittest.TestCase):

    def setUp(self):
        self._setup_destination()
        self._setup_files()
        self._file = Mock(side_effect=self.file_side_effect)
        self._dir = Mock(side_effect=self.directory_side_effect)
        self._service = FilesystemService(self._file, self._dir)

    def test_copy_overwrite_copies_file(self):
        self._service.copy_and_overwrite([self._src1_path, self._src2_path],
                                         self._dst_path)
        self._files_are_copied(self._dst_path, self._src1, self._src2)

    def test_copy_copies_file(self):
        self._service.copy([self._src1_path, self._src2_path],
                           self._dst_path)
        self._files_are_copied(self._dst_path, self._src1, self._src2)

    def test_copy_throws_if_file_exists_in_directory(self):
        self._given_file_exists()
        self._expect_file_exists_exception()

    def test_copy_to_file_raise_if_overwrite(self):
        self._given_dst_is_file("/path/to/some/file.py")
        self._expect_file_exists_exception()

    def test_copy_copies_to_file_which_does_not_exists(self):
        dst = "/some/random/path.py"
        self._service.copy([self._src1_path, self._src2_path], dst)
        self._files_are_copied(dst, self._src1, self._src2)

    def test_rm_deletes_all_files(self):
        self._service.remove([self._src1_path, self._src2_path])
        self._src1.remove.assert_called_once_with(saga.filesystem.RECURSIVE)
        self._src2.remove.assert_called_once_with(saga.filesystem.RECURSIVE)

    def test_cat_writes_content_to_file(self):
        concatenation = self._src1_content + self._src2_content
        self._given_dst_is_file(self._dst_path)
        self._service.cat_to_file([self._src1_path, self._src2_path],
                                  self._dst_path)
        self._dst.write.assert_called_once_with(concatenation)

    def test_cat_creates_output_file_if_required(self):
        concatenation = self._src1_content + self._src2_content
        self._service.cat_to_file([self._src1_path, self._src2_path],
                                  self._new_file_path)
        self._new_file.write.assert_called_once_with(concatenation)

    def test_cat_return_concatenated_files(self):
        concat = self._service.cat([self._src1_path, self._src2_path])
        self.assertEquals(concat, self._src1_content + self._src2_content)

    def test_ls_list_dir_content(self):
        files = self._given_dst_has_files()
        result = self._service.list_dir(self._dst_path)
        self.assertEquals(result, files)

    def directory_side_effect(self, arg):
        if arg == self._dst_path:
            return self._dst
        else:
            raise DoesNotExist
        
    def file_side_effect(self, arg, flags=None):
        if flags == saga.filesystem.CREATE and arg == self._new_file_path:
            return self._new_file
        files = {self._src1_path: self._src1,
                 self._src2_path: self._src2,
                 self._dst_path: self._dst}
        try:
            return files[arg]
        except KeyError:
            raise DoesNotExist(arg)

    def _setup_files(self):
        self._reads_from_src1 = 0
        self._src1_content = "content src1"
        self._src1_path = "/path/to/first/file/src1"
        self._src1 = Mock()
        self._src2_content = "content src2"
        self._src2_path = "/path/to/second/file/src2"
        self._src2 = Mock()
        self._src1.is_file = Mock(return_value=True)
        self._src2.is_file = Mock(return_value=True)
        self._src1.read = Mock(side_effect=self._failing_read_from_file)
        self._src2.read = Mock(return_value=self._src2_content)
        self._new_file_path = self._dst_path + "/file.txt"
        self._new_file = Mock()

    def _setup_destination(self):
        self._dst_path = "/path/to/dst"
        self._dst = Mock()
        self._dst.is_file = Mock(return_value=False)
        self._dst.list = Mock(return_value=[])
        self._dst.create = Mock(side_effect=self._create_file_side_effect)

    def _files_are_copied(self, dst, *files):
        for file in files:
            file.copy.assert_called_once_with(dst)

    def _given_file_exists(self):
        url = Mock()
        url.path = "src1"
        self._dst.list.return_value = [url]

    def _expect_file_exists_exception(self):
        try:
            self._service.copy([self._src1_path, self._src2_path],
                               self._dst_path)
            assert False
        except FileExistsException:
            assert True

    def _given_dst_is_file(self, path):
        self._dst_path = path
        self._dst.is_file = Mock(return_value=True)
        self._dst.list.side_effect = self._raise_exception

    def _raise_exception(self):
        raise AttributeError

    def _create_file_side_effect(self, arg):
        if arg == self._new_file_path:
            return self._new_file

    def _failing_read_from_file(self):
        if self._reads_from_src1 > 0:
            return self._src1_content
        else:
            self._reads_from_src1 += 1
            raise IOError

    def _given_dst_has_files(self):
        name1 = "src1"
        name2 = "src2"
        url1 = Mock()
        url1.path = name1
        url2 = Mock()
        url2.path = name2
        self._dst.list.return_value = [url1, url2]
        return [name1, name2]
