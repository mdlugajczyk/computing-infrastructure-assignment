from lib.saga_service.filesystem_service import FilesystemService
import time
import saga

class JobSubmissionService:
    """
    Service for submitting jobs into the GRID.

    Supports submitting jobs over ssh.
    """

    def __init__(self, saga=saga, saga_job=saga.job,
                 filesystem=FilesystemService()):
        """
        Creates new instance of JobSubmissionService.

        :param saga: Saga module.
        :param saga_job: Saga job module.
        :param filesystem: Service for performing filesystem operations.
        """
        self._saga = saga
        self._saga_job = saga_job
        self._filesystem = filesystem
        self._job_output = None

    def submit_job(self, command, arguments, input_file,
                   output_file, connection_string):
        """
        Submits a job to the GRID.

        If input file is specified it's set as job's argument.
        Remote input file is copied to staging directory.

        If not output file is specified, method returns job output.
        If output file is a remote file, it'll be copied.
        
        Temporary files (input/output) are staged to /tmp directory.

        :param command: Command to invoke.
        :param arguments: Command's arguments.
        :param input_file: Optional command's input file.
        :param output_file: Optional command's output file.
        :param connetion_string: String specifying how to connect to remote host. 
        """
        self._connection_string = connection_string
        self._prepare_input_output(input_file, output_file)
        self._run_job(command, arguments)
        self._handle_output(output_file)
        return self._job_output

    def _prepare_input_output(self, input_file, output_file):
        self._prepare_input_file(input_file)
        self._set_output_file(output_file)
        
    def _run_job(self, command, arguments):
        job = self._create_job(command, arguments)
        job.run()
        job.wait()

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
        is_local_file = (output_file is not None
                         and self._is_local_file(output_file))
        if is_local_file:
            self._job_output_file = output_file
        else:
            self._job_output_file = self._get_tmp_output_file()
    
    def _prepare_input_file(self, input_file):
        if input_file is None or self._is_local_file(input_file):
            self._input_file = input_file
        else:
            self._copy_input_file(input_file)

    def _is_local_file(self, file_path):
        host_separator_index = file_path.find("://")
        return host_separator_index == -1

    def _copy_input_file(self, input_file):
        local_path = self._get_tmp_input_file()
        dst_path = self._saga_file_path(local_path)
        self._filesystem.copy_and_overwrite([input_file], dst_path)
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

    def _capture_job_output(self):
        path = self._connection_string + self._job_output_file
        self._job_output = self._filesystem.cat([path])

    def _get_tmp_output_file(self):
        return self._unique_path("/tmp/s210664-saga-tmp-output-file")

    def _get_tmp_input_file(self):
        return self._unique_path("/tmp/s210664-saga-tmp-input-file")

    def _unique_path(self, path):
        return "%s-%s" % (path, time.time())
