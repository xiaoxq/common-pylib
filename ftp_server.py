#!/usr/bin/env python
"""
FTP Server. Usage:
echo "
$user1 $passws1 $user_dir1
$user2 $passws2 $user_dir2
...
" | python ftp_server.py
"""
import gflags
import pyftpdlib.authorizers
import pyftpdlib.handlers
import pyftpdlib.servers
import sys

import colored_glog as glog
import gflag_util

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


def serve():
    """Server entry."""
    G = gflags.FLAGS
    handler = pyftpdlib.handlers.FTPHandler
    handler.authorizer = build_authorizer()

    glog.info('Starting FTP server at {}:{}'.format(G.ftp_host, G.ftp_port))
    server = pyftpdlib.servers.FTPServer((G.ftp_host, G.ftp_port), handler)
    server.serve_forever()

if __name__ == '__main__':
    gflag_util.init()
    serve()
