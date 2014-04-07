# Introduction

During this project, and utility for running scientific workflows has been developed.
It supports running workflows from file, which contains job definitions as well
as their ordering.

It is based on programs developed in previous part, and also makes use of the SAGA
library.

# Installation

After performing installation instructions from previous part, no additional steps are required.
Workflow utility is ready to be used.

# Workflow systems

Workflow systems are used for various reasons. They allow to automate tasks, reducing chances of error
and allowing humans to avoid mundane, repetitive tasks.

They have other advantages as tracking provenance of data used in the workflow.

# DAG

DAG stands for Directed Acyclic Graph. It's a graph which has directed edges (they have start vertex and end vertex),
and have no cycles. More formally, DAG is a pair (V, E) where V is a set of vertices. E is a set of ordered pairs (v1, v2), v1 v2
belong to V, such that edges in E do not form a cycle.

# File structure

Workflow file has following structure:

JOB job-name command arguments
JOB job2-name command arguments
.
.
.
PARENT parent1..parentN CHILD child1..childN
PARENT parent1..parentN CHILD child1..childN


JOB statements define job and give it a name, PARENT/CHILD statement sets relationship between jobs.
Parents have to be executed before their children.

Simple workflow file may look like this:

JOB A cat ssh://localhost/tmp/passwd-copy
JOB B copy ssh://localhost/etc/passwd ssh://localhost/tmp/passwd-copy
PARENT B CHILD A

# Usage

Workflow utility can be used as follows:

	$ ./run_workflow.py workflow_file

Directory test/functional/workflows contains exemplary workflow files.
