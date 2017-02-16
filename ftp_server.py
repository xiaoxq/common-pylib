"""FTP Server."""
#!/usr/bin/env python
import pyftpdlib.authorizers
import pyftpdlib.handlers
import pyftpdlib.servers
import sys

import config


def serve():
    """Server entry."""
    authorizer = pyftpdlib.authorizers.DummyAuthorizer()
    authorizer.add_user(config.get('ftp_user'),
                        config.get('ftp_pass'),
                        config.get('ftp_root'),
                        perm="elradfmw")

    handler = pyftpdlib.handlers.FTPHandler
    handler.authorizer = authorizer

    server = pyftpdlib.servers.FTPServer((config.get('ftp_host'), int(config.get('ftp_port'))),
                                         handler)
    server.serve_forever()

if __name__ == '__main__':
    config.init(sys.argv[1])
    serve()
