"""System command utils."""
import subprocess as sp
import sys

_NULL_FD = open('/dev/null', 'w')


def run(*args):
    """Get (returncode, stdout, stderr) of the command."""
    cmd = ' '.join(args)
    print 'INFO: Run system command:', cmd
    p = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE, close_fds=True)
    return (p.wait(),
            None if not p.stdout else p.stdout.read().strip().split('\n'),
            None if not p.stderr else p.stderr.read().strip())


def run_or_die(*args):
    """Run command and die if it dies."""
    cmd = ' '.join(args)
    print 'INFO: Run system command:', cmd
    p = sp.Popen(cmd, shell=True, stdout=_NULL_FD, stderr=sp.PIPE, close_fds=True)
    if p.wait():
        if p.stderr:
            sys.stderr.write(p.stderr.read())
        exit(p.returncode)


def run_in_background(*args):
    """Run command in background."""
    cmd = ' '.join(args)
    print 'INFO: Run system command in background:', cmd
    sp.Popen(cmd, shell=True, stdout=_NULL_FD, stderr=_NULL_FD, close_fds=True)
