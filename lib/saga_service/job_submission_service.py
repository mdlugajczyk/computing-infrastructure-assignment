from lib.saga_service.filesystem_service import FilesystemService
import time
import saga

class JobSubmissionService:

    def __init__(self, saga=saga, saga_job=saga.job,
                 filesystem=FilesystemService()):
        self._saga = saga
        self._saga_job = saga_job
        self._filesystem = filesystem
        self._job_output = None

    def submit_job(self, command, arguments, input_file,
                   output_file, connection_string):
        self._connection_string = connection_string
        self._prepare_input_file(input_file)
        self._set_output_file(output_file)
        job = self._create_job(command, arguments)
        job.run()
        job.wait()
        self._handle_output(output_file)
        return self._job_output

    def _create_job(self, command, arguments):
        session = self._get_session()
        js = self._saga_job.Service(self._connection_string, session=session)
        jd = self._get_job_description(command, arguments)
        return js.create_job(jd)
        
    def _get_session(self):
        connection_type = self._connection_string.split("://")[0]
        ctx = self._saga.Context(connection_type)
        session = self._saga.Session()
        session.add_context(ctx)
        return session

    def _get_job_description(self, command, arguments):
        jd = self._saga_job.Description()
        jd.executable = command
        jd.arguments = [arguments]
        if self._input_file:
            jd.input = self._input_file
        jd.output = self._job_output_file
        return jd

    def _set_output_file(self, output_file):
        if output_file is not None and self._is_local_file(output_file):
            self._job_output_file = output_file
        else:
            current_time = time.time()        
            self._job_output_file = "/tmp/s210664-saga-output"
            self._job_output_file += "-%s" % current_time
    
    def _prepare_input_file(self, input_file):
        if input_file is None:
            self._input_file =  None
        elif self._is_local_file(input_file):
            self._input_file = input_file
        else:
            self._copy_input_file(input_file)

    def _is_local_file(self, file_path):
        host_index = file_path.find("://")
        return host_index == -1

    def _copy_input_file(self, input_file):
        local_path = self._path_in_staging_directory(input_file)
        dst_path = self._saga_file_path(local_path)
        self._filesystem.copy_and_overwrite(input_file, dst_path)
        self._input_file = local_path

    def _handle_output(self, output_file):
        self._copy_output_file(output_file)
        if output_file is None:
            self._capture_job_output()

    def _copy_output_file(self, output_file):
        if output_file is None:
            return
        is_remote = not self._is_local_file(output_file)
        if is_remote:
            src = self._saga_file_path(self._job_output_file)
            self._filesystem.copy_and_overwrite([src], output_file)

    def _saga_file_path(self, path):
        return self._connection_string + path

    def _path_in_staging_directory(self, path):
        return "/tmp" + path[path.rfind("/"):]

    def _capture_job_output(self):
        path = self._connection_string + self._job_output_file
        self._job_output = self._filesystem.cat([path])
