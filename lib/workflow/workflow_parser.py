from lib.exception.file_format_exception import FileFormatException

class WorkflowParser:

    def parse(self, file_path):
        self._read_file(file_path)
        self._extract_lines()
        return [self._parse_job(job) for job in self._jobs]

    def parse_job(self, job):
        elements = job.split()
        return elements

    def _read_file(self, file_path):
        with open(file_path, 'r') as f:
            self._content = f.read()

    def _extract_lines(self):
        self._jobs = [job.split() for job in self._content.split("\n")]

    def _parse_job(self, job):
        if len(job) == 0:
            return None, None
        if len(job) < 3:
            raise FileFormatException
        cmd = job[2]
        args = job[3:]
        return cmd, " ".join(args)
