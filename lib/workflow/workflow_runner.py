from lib.workflow.workflow_parser import WorkflowParser
from lib.workflow.job_factory import JobFactory
from lib.workflow.job_scheduler import JobScheduler
import time

class WorkflowRunner:

    def __init__(self, filesystem, job_submission):
        self._parser = WorkflowParser()
        self._job_factory = JobFactory(filesystem, job_submission)
        self._job_scheduler = JobScheduler()

    def run(self, file_path):
        parsed_jobs, self._relations = self._parser.parse(file_path)
        self._create_jobs(parsed_jobs)
        self._schedule_jobs()
        return self._run_jobs()

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
        while len(self._scheduled_jobs) > 0:
            if not self._run_scheduled_job():
                break
            self._scheduled_jobs.pop(0)
        return [job.name for job in self._scheduled_jobs]

    def _run_scheduled_job(self):
        """
        Run a job, in case of a failure retry after 5 seconds.
        """
        job = self._scheduled_jobs[0]
        if self._execute(job):
            return True
        else:
            print "Retrying to run the job in 5 seconds..."
            time.sleep(5)
            return self._execute(job)

    def _execute(self, job):
        success = False
        try:
            print "Running job: %s" % job.name
            job.execute_command()
            success = True
        except Exception, e:
            print "Job %s failed (%s)." % (job.name, str(e))
        return success
