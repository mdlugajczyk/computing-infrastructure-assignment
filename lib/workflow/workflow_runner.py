from lib.workflow.workflow_parser import WorkflowParser
from lib.workflow.job_factory import JobFactory
from lib.workflow.job_scheduler import JobScheduler


class WorkflowRunner:

    def __init__(self, filesystem, job_submission):
        self._parser = WorkflowParser()
        self._job_factory = JobFactory(filesystem, job_submission)
        self._job_scheduler = JobScheduler()

    def run(self, file_path):
        parsed_jobs, self._relations = self._parser.parse(file_path)
        self._create_jobs(parsed_jobs)
        self._schedule_jobs()
        self._run_jobs()

    def _create_jobs(self, parsed_jobs):
        self._jobs = []
        for name, cmd, args in parsed_jobs:
            if cmd is None or args is None:
                continue
            self._jobs.append(self._job_factory.create_job(name, cmd, args))

    def _schedule_jobs(self):
        self._scheduled_jobs = self._job_scheduler.schedule(self._jobs,
                                                            self._relations)

    def _run_jobs(self):
        for job in self._scheduled_jobs:
            job.execute_command()
            
