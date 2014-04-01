import unittest
import shutil
import time
from subprocess import call, Popen, PIPE
import filecmp
import os
import shlex


class CommandTest(unittest.TestCase):

    def setUp(self):
        current_time = time.time()
        self.src = "/tmp/functional-test-src-%s" % current_time
        self.dst = "/tmp/functional-test-dst-%s" % current_time

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
        file_name = ls_path[ls_path.rfind('/')+1:]
        os.mkdir(self.dst)
        shutil.copy(ls_path, self.dst)
        cmd = "%s %s" % (ls_path, self.full_path(self.dst))
        args = shlex.split(cmd)
        output,error = Popen(args,stdout = PIPE,
                             stderr= PIPE).communicate()
        print self.dst
        self.assertTrue(output.strip(), file_name)

    def test_exec(self):
        exec_path = "../../exec.py"
        shutil.copyfile(exec_path, self.src)
        call([exec_path, "-stdout", self.full_path(self.dst),
              "-r", "ssh://localhost", "cat", self.src])
        self.assertTrue(filecmp.cmp(self.src, self.dst))

        

    def full_path(self, path):
        return "ssh://localhost%s" % path
