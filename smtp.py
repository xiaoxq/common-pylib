"""
SMTP library.
Make sure you have a config file with these settings:
smtp_server =
smtp_port =
smtp_user =
smtp_pass =
smtp_sender =

Library usage:
    # Make sure you have called config.init().
    smtp.send(subject, content, 'a@x.com,b@x.com,...')
    ...
    smtp.quit()
Binary usage:
    echo "CONTENT" | python smtp.py <conf_file> <subject> <receiver>
"""
#!/usr/bin/env python
#coding: utf-8
import email.header
import email.mime.text
import smtplib
import sys

import config

_smtp = None

def _init_smtp():
    client = smtplib.SMTP(config.get('smtp_server'), config.get('smtp_port'))
    client.ehlo()
    client.starttls()
    client.login(config.get('smtp_user'), config.get('smtp_pass'))
    return client


def send(subject, content, receiver, cc=None):
    """Send email."""
    msg = email.mime.text.MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = email.header.Header(subject, 'utf-8')
    msg['From'] = config.get('smtp_sender')
    msg['To'] = receiver
    print 'INFO: Sent mail <{}> with {} bytes to [{}]'.format(subject, len(content), receiver)

    global _smtp
    _smtp = _smtp or _init_smtp()
    _smtp.sendmail(config.get('smtp_sender'), receiver, msg.as_string())


def quit():
    """Quit from smtp connection."""
    _smtp.quit()
    _smtp = None

if __name__ == '__main__':
    conf_file, subject, receiver = sys.argv[1:]
    config.init(conf_file, 'smtp')
    send(subject, sys.stdin.read(), receiver)
