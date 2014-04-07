# Introduction

This project consists of Unix-like utilities for performing file
operations on remote hosts using GRID infrastructure.

All utilities are based on a SAGA library, a "Simple API for Grid Applications".
SAGA provides a convenient abstractions over most common operations
performed in GRID environment. It supports operations like file transfer,
job submission, etc.

As SAGA is quite high level solution compared to other standard
GRID libraries, it allows for faster and easier development
of GRID based utilities.

Project has been developed in Python language, thus Python bindings
to the SAGA library have been used.

## Installation

In order to install the project to selected directory, run:

	$ git clone https://github.com/mdlugajczyk/computing-infrastructure-assignment.git directory_name

Create new python environment using virtualenv:

	$ cd directory_name
	$ virtualenv .virtualenv

Select newly created environment:

	$ . .virtualenv/bin/activate

Install all dependencies:

	$ pip install -r requirements.txt

Now project is ready to be used.

## Credentials setup

This project connects to remote hosts using SSH, therefore it is required that SSH keys
are correctly set up.

SSH keys can be generated using following command:

	$ ssh-keygen -t rsa -C "email@example.com"

Next you have to add your ssh keys to ssh-agent:

	$ ssh-add ~/.ssh/id_rsa

Replace id_rsa with name of your key.
All utilities will try to connect to remote hosts using default key/user name.
If you want to use different key, add appropriate configuration to
~/.ssh/config file.

# Description of utilities

Each file path passed as argument should have following form

ssh://host/path/to/file/or/directory

In future, connection types other than ssh may be supported.

If an error occurs during execution of the command,
it's printed to the screen and program exits.

Following utilities have been developed:

## copy

This utility is similar to Unix cp command.

It can be invoked as follows:

	$ ./cp.py [-f] src1 ... srcN dst

There can be arbitrary number of source files and one destination file.
`-f` flag will cause the destination file to be overwritten if it already exists.
If `-f` is not used, and destination already exists, error will be reported.
All `src` arguments have to be files. `dst` argument can be directory

Exemplary invocation:

	$ ./cp.py -f ssh://localhost/etc/passwd ssh://localhost/etc/hosts ssh://localhost/tmp/

It will copy /etc/passwd and /etc/hosts files to /tmp directory on local machine.

## cat

This utility is similar to Unix cat command. It concatenates files and prints the result
to stdout or specified destination

It can be invoked as follows:

	$ ./cat.py src1 ... srcN [-o dst]
`src1 ... srcN` is a sequence of at least one file path, content of all
specified files will be concatenated. By default, result is
printed to stdout. If `-o` flag is specified together with destination,
result will be written to given file.

Exemplary invocation:

	$ ./cat.py ssh://localhost/etc/passwd ssh://localhost/etc/hosts -o ssh://localhost/tmp/passwd_hosts

It will write content of /etc/passwd and /etc/hosts to /tmp/passwd_hosts file

## rm

This utility is similar to Unix rm command. It removes files from remote hosts.
Removing directories is not supported.

It can be invoked as follows:

	$ rm file1 ... fileN

Where `file1 ... fileN` is a list of files to be removed.

Exemplary invocation:

	$ ./rm.py ssh://localhost/tmp/path/to/file

## ls

This utility is similar to Unix ls command. It lists content of a remote
directory.

It can be invoked as follows:

	$ ./ls.py dir_name

Exemplary invocation:

	$ ./ls.py ssh://localhost/etc

It will print content of /etc directory.

## exec

This utility allows to run jobs on remote hosts.

It can be invoked as follows:

	$ ./exec.py [-stdin filein] [-stdout fileout] -r contact-string -- command arg1 ... argN

### Arguments

`-r` - Required argument, describes how to connect to remote host
`command` - Require argument, command to run on remote host
`-stdin` - Optional argument, command's input file. Can be either local or remote
`-stdout` - Optional argument, command's output file. Can be either local or remote

If no output file is specified, command's output will be printed to the screen (it is accomplished
by redirecting the output to temporary file and running `cat` on this file after job's finished).

If input/output file is a remote file, i.e, specified in the `ssh://host/file` format, it'll be copied to/from the host.
If it's a local file, e.g., `/tmp/file` it'll be just passed as job's argument.

Exemplary invocation:

	$ ./exec.py -stdin ssh://localhost/etc/passwd -stdout /tmp/passwd_grep -r ssh://localhost -- grep root

It will run the command on localhost. It will execute `grep root` on /etc/passwd file, and save
the result to /tmp/passwd_grep file.

# Tests

Tests have been developed for this project. To run unit tests, invoke:

	$ nosetests

from project's root directory.

To run functional/acceptance tests, enter the `test` directory and invoke `run_functional.sh` script.

	$ cd test
	$ ./run_functional.sh
