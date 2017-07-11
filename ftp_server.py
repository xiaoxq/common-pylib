#!/usr/bin/env python

"""
FTP Server. Usage:
echo "
$user1 $passws1 $user_dir1
$user2 $passws2 $user_dir2
...
" | python ftp_server.py

Use "anonymous" as username and password for anonymous access.
"""

import sys

import gflags
import google.apputils.app
import pyftpdlib.authorizers
import pyftpdlib.handlers
import pyftpdlib.servers

import colored_glog as glog

gflags.DEFINE_string('ftp_host', '0.0.0.0', 'FTP host.')
gflags.DEFINE_integer('ftp_port', 21, 'FTP port.')


def build_authorizer():
    """Add users from stdin."""
    authorizer = pyftpdlib.authorizers.DummyAuthorizer()
    for line in sys.stdin:
        parts = line.strip().split(' ', 2)
        if len(parts) != 3:
            continue
        user, passwd, user_dir = parts
        glog.info('Add user {} for dir {}'.format(user, user_dir))
        if user == 'anonymous':
            authorizer.add_anonymous(user_dir)
        else:
            authorizer.add_user(user, passwd, user_dir, perm="elradfmw")
    return authorizer


def main(argv):
    """Server entry."""
    handler = pyftpdlib.handlers.FTPHandler
    handler.authorizer = build_authorizer()

    G = gflags.FLAGS
    glog.info('Starting FTP server at {}:{}'.format(G.ftp_host, G.ftp_port))
    server = pyftpdlib.servers.FTPServer((G.ftp_host, G.ftp_port), handler)
    server.serve_forever()

if __name__ == '__main__':
    google.apputils.app.run()
