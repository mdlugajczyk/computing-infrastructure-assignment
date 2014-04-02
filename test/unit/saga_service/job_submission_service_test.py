from lib.saga_service.job_submission_service import JobSubmissionService
import unittest
from mockito import Mock, verify, when, any
from mock import Mock as mock_Mock, patch, mock_open

class JobSubmissionServiceTest(unittest.TestCase):

    def setUp(self):
        self.current_time = 1123455.123
        self.connection_string = "ssh://localhost"
        self.setup_saga()
        self.setup_filesystem()
        self.setup_mocks()
        self.command = "grep"
        self.args = "root /etc/password"
        self.service  = JobSubmissionService(self.saga, self.saga_job,
                                             self.filesystem)

    def test_creates_job_service(self):
        self.submit_job()
        verify(self.saga_job).Service(self.connection_string,
                                 session=self.session)

    def test_sets_job_command(self):
        self.submit_job()
        self.assertEqual(self.description.executable, "grep")

    def test_sets_job_arguments(self):
        self.submit_job()
        self.assertEqual(self.description.arguments, [self.args])

    def test_creates_job(self):
        self.submit_job()
        verify(self.saga_job_service).create_job(self.description)

    def test_runs_job(self):
        self.submit_job()
        verify(self.job).run()
        verify(self.job).wait()

    def test_sets_job_output(self):
        expected_output = "/tmp/s210664-saga-output-%s" % self.current_time
        self.submit_job()
        self.assertEqual(self.description.output, expected_output)

    def test_sets_local_input_file(self):
        self.input_file = "/local/file/name"
        self.submit_job()
        self.assertEqual(self.description.input, self.input_file)

    def test_copies_remote_input_file(self):
        self.given_input_file_is_remote()
        self.submit_job()
        self.assertEqual(self.description.input, "/tmp/" + self.file_name)
        verify(self.filesystem).copy_and_overwrite([self.input_file],
                                                   self.expected_dst)

    def test_copies_remote_output_file(self):
        self.given_output_file_is_remote()
        self.submit_job()
        src = self.connection_string + self.get_local_output_file()
        verify(self.filesystem).copy_and_overwrite([src], self.output_file)

    def test_sets_local_output_file(self):
        self.output_file = "/tmp/some-file"
        self.wont_copy_file()
        self.submit_job()
        self.assertEqual(self.description.output, self.output_file)

    def test_prints_output_if_no_output_file(self):
        self.submit_job()
        verify(self.filesystem).cat([self.connection_string + self.get_local_output_file()])

    def setup_saga(self):
        self.job = Mock()
        self.description = mock_Mock()
        self.saga_job = Mock()
        self.saga_job_service = Mock()
        self.session = Mock()
        self.context = Mock()
        self.saga = Mock()
        when(self.saga_job).Description().thenReturn(self.description)
        when(self.saga).Context("ssh").thenReturn(self.context)
        when(self.saga).Session().thenReturn(self.session)
        when_service = when(self.saga_job).Service(self.connection_string,
                                                     session=self.session)
        when_service.thenReturn(self.saga_job_service)
        when_job = when(self.saga_job_service).create_job(self.description)
        when_job.thenReturn(self.job)

    def setup_filesystem(self):
        self.input_file = None
        self.output_file = None
        self.filesystem = Mock()

    def setup_mocks(self):
        self.mocked_time = mock_Mock(return_value=self.current_time)

    def submit_job(self):
        with patch('time.time', self.mocked_time):
            return self.service.submit_job(self.command, self.args,
                                           self.input_file,
                                           self.output_file,
                                           self.connection_string)

    def given_input_file_is_remote(self):
        self.file_name = "file"
        self.input_file = "ssh://some-host/path-to/" + self.file_name
        self.expected_dst = self.connection_string + "/tmp/" + self.file_name

    def wont_copy_file(self):
        when_copy =  when(self.filesystem).copy_and_overwrite(any(), any())
        when_copy.thenRaise(Exception("Shouldn't copy file"))

    def given_output_file_is_remote(self):
        file_name = "output-file"
        self.output_file = "ssh://some-host/path/to/" + file_name
        self.expected_dst = self.connection_string + "/tmp/" + file_name

    def get_local_output_file(self):
        return "/tmp/s210664-saga-output-%s" % self.current_time
