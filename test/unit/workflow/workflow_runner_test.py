import unittest
from lib.workflow.workflow_runner import WorkflowRunner
from lib.exception.file_format_exception import FileFormatException
from mockito import Mock, verify, when, any, inorder
from mock import mock_open, patch

class WorkflowRunnerTest(unittest.TestCase):

    def setUp(self):
        self.workflow_file_content = ""
        self.filesystem = Mock()
        self.job_submission = Mock()
        self.workflow_file_path = "/path/to/workflow/file"
        self.workflow = WorkflowRunner(self.filesystem,
                                       self.job_submission)
        when(self.filesystem).list_dir(any()).thenReturn([])

    def test_opens_right_file(self):
        self.run_workflow()
        self.open_mocked.assert_called_with(self.workflow_file_path, 'r')

    def test_runs_ls_job(self):
        self.workflow_file_content = "JOB A ls ssh://localhost/tmp"
        self.run_workflow()
        verify(self.filesystem).list_dir("ssh://localhost/tmp")

    def test_runs_cat_job(self):
        self.workflow_file_content = "JOB B cat ssh://localhost/tmp/file"
        self.run_workflow()
        verify(self.filesystem).cat(["ssh://localhost/tmp/file"])

    def test_handles_two_jobs(self):
        self.workflow_file_content = "JOB A ls ssh://localhost/tmp\n\n"
        self.workflow_file_content += "\nJOB B cat ssh://localhost/tmp/file"
        self.run_workflow()
        verify(self.filesystem).list_dir("ssh://localhost/tmp")
        verify(self.filesystem).cat(["ssh://localhost/tmp/file"])

    def test_parses_jobs_argument(self):
        job = "JOB A cat ssh://host/tmp/file1 -o ssh://host/tmp/file2"
        self.workflow_file_content = job
        self.run_workflow()
        verify(self.filesystem).cat_to_file(["ssh://host/tmp/file1"],
                                             "ssh://host/tmp/file2")

    def test_runs_cp_job(self):
        job = "JOB B copy ssh://host1/src ssh://host2/dst"
        self.workflow_file_content = job
        self.run_workflow()
        verify(self.filesystem).copy(["ssh://host1/src"], "ssh://host2/dst")

    def test_runs_rm_job(self):
        self.workflow_file_content = "JOB A rm ssh://host/file"
        self.run_workflow()
        verify(self.filesystem).remove(["ssh://host/file"])

    def test_runs_exec_job(self):
        self.workflow_file_content = "JOB a exec -r ssh://host ls /tmp"
        self.run_workflow()
        verify(self.job_submission).submit_job("ls", "/tmp", None,
                                               None, "ssh://host")

    def test_raise_exception_invalid_file_format(self):
        self.workflow_file_content = "JOB\nPARENT A CHILD A"
        try:
            self.run_workflow()
            self.assertTrue(False)
        except FileFormatException:
            pass

    def test_schedules_job_with_one_child_one_parent(self):
        self.workflow_file_content = "JOB A ls ssh://host/dir\n"
        self.workflow_file_content += "JOB B rm ssh://host/file\n"
        self.workflow_file_content += "PARENT B CHILD A"
        self.run_workflow()
        inorder.verify(self.filesystem).remove(["ssh://host/file"])
        inorder.verify(self.filesystem).list_dir("ssh://host/dir")

    def test_schedules_job_with_two_children(self):
        self.workflow_file_content = "JOB A ls ssh://host/dir\n"
        self.workflow_file_content += "JOB B rm ssh://host/file\n"
        self.workflow_file_content += "JOB C ls ssh://host/dir2\n"
        self.workflow_file_content += "JOB D cat ssh://host/file2\n"
        self.workflow_file_content += "PARENT B D CHILD A C\n"
        self.workflow_file_content += "PARENT B CHILD D \n"
        self.workflow_file_content += "PARENT A CHILD C\n"
        self.run_workflow()
        inorder.verify(self.filesystem).remove(["ssh://host/file"])
        inorder.verify(self.filesystem).cat(["ssh://host/file2"])
        inorder.verify(self.filesystem).list_dir("ssh://host/dir")
        inorder.verify(self.filesystem).list_dir("ssh://host/dir2")
        
    def run_workflow(self):
        self.open_mocked = mock_open(read_data=self.workflow_file_content)
        with patch('__builtin__.open', self.open_mocked):
            self.workflow.run(self.workflow_file_path)
