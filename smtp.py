"""
SMTP library.
Make sure you have a config file with these settings:
[smtp]
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
import glog
import smtplib
import sys

import config


def send(subject, content, receiver, cc=None):
    """Send email."""
    msg = email.mime.text.MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = email.header.Header(subject, 'utf-8')
    msg['From'] = config.get('smtp_sender')
    msg['To'] = receiver
    if cc:
        msg['Cc'] = cc
        receiver += ',' + cc

    glog.info('Sent mail <{}> with {} bytes to [{}]'.format(subject, len(content), receiver))
    s = smtplib.SMTP(config.get('smtp_server'), config.get('smtp_port'))
    s.ehlo()
    s.starttls()
    s.login(config.get('smtp_user'), config.get('smtp_pass'))
    s.sendmail(msg['From'], receiver, msg.as_string())
    s.quit()


def send_from_local(subject, content, sender, receiver, cc=None):
    """Send email."""
    msg = email.mime.text.MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = email.header.Header(subject, 'utf-8')
    msg['From'] = sender
    msg['To'] = receiver
    if cc:
        msg['Cc'] = cc
        receiver += ',' + cc

    glog.info('Sent mail <{}> with {} bytes to [{}]'.format(subject, len(content), receiver))
    s = smtplib.SMTP('localhost')
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()


if __name__ == '__main__':
    conf_file, subject, receiver = sys.argv[1:]
    config.init(conf_file, 'smtp')
    send(subject, sys.stdin.read(), receiver)
