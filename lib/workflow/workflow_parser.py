from lib.exception.file_format_exception import FileFormatException

class WorkflowParser:

    def parse(self, file_path):
        self._read_file(file_path)
        self._extract_lines()
        self._parse_statements()
        return self._jobs, self._relations

    def _read_file(self, file_path):
        with open(file_path, 'r') as f:
            self._content = f.read()

    def _extract_lines(self):
        self._statements = [s.split() for s in self._content.split("\n")]

    def _parse_statements(self):
        self._jobs = []
        self._relations = []
        try:
            self._try_parse_statements()
        except Exception:
            raise FileFormatException

    def _try_parse_statements(self):
        for stmt in self._statements:
            self._parse_statement(stmt)

    def _parse_statement(self, stmt):
        if len(stmt) == 0:
            return
        elif self._is_job_definition(stmt):
            self._parse_job(stmt)
        elif self._is_relation_definition(stmt):
            self._parse_relation(stmt)

    def _parse_job(self, job):
        name = job[1]
        cmd = job[2]
        args = job[3:]
        self._jobs.append((name, cmd, " ".join(args)))

    def _parse_relation(self, rel):
        child_index = rel.index("CHILD")
        parents = rel[1:child_index]
        children = rel[child_index+1:]
        self._relations.append((parents, children))

    def _is_job_definition(self, stmt):
        return stmt[0] == "JOB"

    def _is_relation_definition(self, stmt):
        return stmt[0] == "PARENT"
