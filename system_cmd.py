#!/usr/bin/env python
#  coding: utf-8

"""System command utils."""

import subprocess as sp
import sys

import colored_glog as glog

_NULL_FD = open('/dev/null', 'w')


def run(*args):
    """Get (ret_code, stdout, stderr) of the command."""
    cmd = ' '.join(args)
    glog.info('SYSTEM> {}'.format(cmd))
    p = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE, close_fds=True)
    return (p.wait(),
            None if not p.stdout else p.stdout.read(),
            None if not p.stderr else p.stderr.read())


def run_or_die(*args):
    """Run command and die if it dies."""
    ret, output, error = run(*args)
    if ret:
        if error:
            glog.fatal(error)
        sys.exit(ret)
    return output


def run_and_alert(*args):
    """Run command and alert errors."""
    ret, output, error = run(*args)
    if error:
        glog.error(error)
    return output


def run_in_background(*args):
    """Run command in background."""
    cmd = ' '.join(args)
    glog.info('SYSTEM> {}'.format(cmd))
    sp.Popen(cmd, shell=True, stdout=_NULL_FD, stderr=_NULL_FD, close_fds=True)
