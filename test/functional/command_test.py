import unittest
import shutil
from subprocess import call, Popen, PIPE
import filecmp
import os
import shlex

class CommandTest(unittest.TestCase):

    def setUp(self):
        self.src = "/tmp/functional-test-src"
        self.dst = "/tmp/functional-test-dst"
        self.workflow_file_1 = "/tmp/workflow-saga-file-1"
        self.workflow_file_2 = "/tmp/workflow-saga-file-2"
        self.workflow_file_3 = "/tmp/workflow-saga-file-3"
        self.workflow_file_4 = "/tmp/workflow-saga-file-4"
        self.remove_files()

    def test_cat(self):
        cat_path = "../../cat.py"
        shutil.copyfile(cat_path, self.src)
        call([cat_path, self.full_path(self.src), "-o", self.full_path(self.dst)])
        self.assertTrue(filecmp.cmp(self.src, self.dst))

    def test_cp(self):
        cp_path = "../../cp.py"
        shutil.copyfile(cp_path, self.src)
        call([cp_path, self.full_path(self.src),  self.full_path(self.dst)])
        self.assertTrue(filecmp.cmp(self.src, self.dst))

    def test_rm(self):
        rm_path = "../../rm.py"
        shutil.copyfile(rm_path, self.src)
        call([rm_path, self.full_path(self.src)])
        self.assertEqual(os.path.isfile(self.src), False)

    def test_ls(self):
        ls_path = "../../ls.py"
        file_name = 'ls.py'
        os.mkdir(self.dst)
        shutil.copy(ls_path, self.dst)
        cmd = "%s %s" % (ls_path, self.full_path(self.dst))
        args = shlex.split(cmd)
        output,error = Popen(args,stdout = PIPE,
                             stderr= PIPE).communicate()
        self.assertEqual(output.strip(), file_name)

    def test_exec(self):
        exec_path = "../../exec.py"
        shutil.copyfile(exec_path, self.src)
        call([exec_path, "-stdout", self.full_path(self.dst),
              "-r", "ssh://localhost", "cat", self.src])
        self.assertTrue(filecmp.cmp(self.src, self.dst))

    def test_workflow_runs_sync_jobs(self):
        call("cp workflows/sync_jobs.txt /tmp/workflow-saga-file-1".split())
        call("../../run_workflow.py workflows/sync_jobs.txt".split())
        self.assertTrue(filecmp.cmp(self.workflow_file_1,
                                    self.workflow_file_2))
        self.assertTrue(filecmp.cmp(self.workflow_file_1,
                                    self.workflow_file_3))

    def test_workflow_schedules_jobs(self):
        call("cp workflows/scheduled_jobs.txt /tmp/workflow-saga-file-1".split())
        call("../../run_workflow.py workflows/scheduled_jobs.txt".split())
        self.assertTrue(filecmp.cmp("workflows/scheduled_jobs.txt",
                                    self.workflow_file_2))
        self.assertTrue(filecmp.cmp("workflows/scheduled_jobs.txt",
                                    self.workflow_file_3))
        self.assertEqual(os.path.isfile(self.workflow_file_1), False)

    # expected job order: E -> C -> A -> B -> D -> F
    def test_workflow_handle_many_children_many_parent_relationships(self):
        call("cp workflows/scheduled_jobs.txt /tmp/workflow-saga-file-1".split())
        call("../../run_workflow.py workflows/many_children_many_parents.txt".split())
        self.assertTrue(filecmp.cmp("workflows/scheduled_jobs.txt",
                                    self.workflow_file_2))
        self.assertTrue(filecmp.cmp("workflows/scheduled_jobs.txt",
                                    self.workflow_file_3))
        self.assertTrue(os.path.isfile(self.workflow_file_4))
        self.assertEqual(os.path.isfile(self.workflow_file_1), False)

    def full_path(self, path):
        return "ssh://localhost%s" % path

    def remove_files(self):
        self.remove_file_or_dir(self.src)
        self.remove_file_or_dir(self.dst)
        self.remove_file_or_dir(self.workflow_file_1)
        self.remove_file_or_dir(self.workflow_file_2)
        self.remove_file_or_dir(self.workflow_file_3)
        self.remove_file_or_dir(self.workflow_file_4)

    def remove_file_or_dir(self, path):
        call(["rm", "-rf", path])
