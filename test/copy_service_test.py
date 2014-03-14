from lib.copy_service import CopyService, FileExistsException
from mock import Mock
import unittest

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
        self._files_are_copied(self._src1, self._src2)

    def test_copy_copies_file(self):
        self._service.copy([self._src1_str, self._src2_str],
                           self._dst_str)
        self._files_are_copied(self._src1, self._src2)

    def test_copy_throws_if_file_exists(self):
        self._given_file_exists()
        try:
            self._service.copy([self._src1_str, self._src2_str],
                               self._dst_str)
            raise Exception()
        except FileExistsException:
            pass

    def directory_side_effect(self, arg):
        if arg == self._dst_str:
            return self._dst
            
    def file_side_effect(self, arg):
        files = {self._src1_str: self._src1,
                 self._src2_str: self._src2}
        return files[arg]

    def _setup_source_files(self):
        self._src1_str = "/path/to/first/file/src1"
        self._src1 = Mock()
        self._src2_str = "/path/to/second/file/src2"
        self._src2 = Mock()
        self._src1.is_file = True
        self._src2.is_file = True

    def _setup_destination(self):
        self._dst_str = "dst"
        self._dst = Mock()
        self._dst.is_file = False
        self._dst.list = Mock(return_value=[])

    def _files_are_copied(self, *files):
        for file in files:
            file.copy.assert_called_once_with(self._dst_str)

    def _given_file_exists(self):
        url = Mock()
        url.path = "src1"
        self._dst.list.return_value = [url]
