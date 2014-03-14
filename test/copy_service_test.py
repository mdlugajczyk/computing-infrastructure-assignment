from lib.copy_service import CopyService, FileExistsException
from mock import Mock
import unittest
from saga.exceptions import DoesNotExist

class CopyServiceTest(unittest.TestCase):

    def setUp(self):
        self._setup_destination()
        self._setup_source_files()
        self._file = Mock(side_effect=self.file_side_effect)
        self._dir = Mock(side_effect=self.directory_side_effect)
        self._service = CopyService(self._file, self._dir)

    def test_copy_overwrite_copies_file(self):
        self._service.copy_and_overwrite([self._src1_str, self._src2_str],
                                         self._dst_str)
        self._files_are_copied(self._dst_str, self._src1, self._src2)

    def test_copy_copies_file(self):
        self._service.copy([self._src1_str, self._src2_str],
                           self._dst_str)
        self._files_are_copied(self._dst_str, self._src1, self._src2)

    def test_copy_throws_if_file_exists_in_directory(self):
        self._given_file_exists()
        self._expect_file_exists_exception()

    def test_copy_to_file_raise_if_overwrite(self):
        self._given_dst_is_file("/path/to/some/file.py")
        self._expect_file_exists_exception()

    def test_copy_copies_to_file_which_does_not_exists(self):
        dst = "/some/random/path.py"
        self._service.copy([self._src1_str, self._src2_str], dst)
        self._files_are_copied(dst, self._src1, self._src2)

    def directory_side_effect(self, arg):
        if arg == self._dst_str:
            return self._dst
        else:
            raise DoesNotExist
        
    def file_side_effect(self, arg):
        files = {self._src1_str: self._src1,
                 self._src2_str: self._src2,
                 self._dst_str: self._dst}
        try:
            return files[arg]
        except KeyError:
            raise DoesNotExist(arg)

    def _setup_source_files(self):
        self._src1_str = "/path/to/first/file/src1"
        self._src1 = Mock()
        self._src2_str = "/path/to/second/file/src2"
        self._src2 = Mock()
        self._src1.is_file = Mock(return_value=True)
        self._src2.is_file = Mock(return_value=True)

    def _setup_destination(self):
        self._dst_str = "dst"
        self._dst = Mock()
        self._dst.is_file = Mock(return_value=False)
        self._dst.list = Mock(return_value=[])

    def _files_are_copied(self, dst, *files):
        for file in files:
            file.copy.assert_called_once_with(dst)

    def _given_file_exists(self):
        url = Mock()
        url.path = "src1"
        self._dst.list.return_value = [url]

    def _expect_file_exists_exception(self):
        try:
            self._service.copy([self._src1_str, self._src2_str],
                               self._dst_str)
            raise Exception()
        except FileExistsException:
            pass

    def _given_dst_is_file(self, path):
        self._dst_str = path
        self._dst.is_file = Mock(return_value=True)
        self._dst.list.side_effect = self._raise_exception

    def _raise_exception(self):
        raise AttributeError
