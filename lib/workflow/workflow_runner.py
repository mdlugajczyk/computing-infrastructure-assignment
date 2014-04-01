from lib.workflow.workflow_parser import WorkflowParser
from lib.workflow.job_factory import JobFactory


class WorkflowRunner:

    def __init__(self, filesystem, job_submission):
        self._parser = WorkflowParser()
        self._job_factory = JobFactory(filesystem, job_submission)

    def run(self, file_path):
        jobs = self._parser.parse(file_path)
        self._run_jobs(jobs)

    def _run_jobs(self, jobs):
        for cmd, args in jobs:
            self._run_job(cmd, args)

    def _run_job(self, cmd, args):
        if cmd is None or args is None:
            return
        job = self._job_factory.create_job(cmd, args)
        job.execute_command()
