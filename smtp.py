#!/usr/bin/env python
# coding: utf-8

"""
SMTP library. Usage:
    smtp.send(subject, content, 'a@x.com,b@x.com,...')
    ...
    smtp.quit()
Binary usage:
    echo "<receiver> <subject> <content>" | python smtp.py [gflags]
"""

import email.header
import email.mime.text
import smtplib
import sys

import gflags
import google.apputils.app

import colored_glog as glog


gflags.DEFINE_string('smtp_server', None, 'SMTP server.')
gflags.DEFINE_integer('smtp_port', 25, 'SMTP server port.')
gflags.DEFINE_string('smtp_user', None, 'SMTP server user.')
gflags.DEFINE_string('smtp_pass', None, 'SMTP server password.')
gflags.DEFINE_string('smtp_sender', None, 'SMTP mail sender.')


def send(subject, content, receiver, cc=None):
    """Send email."""
    G = gflags.FLAGS
    msg = email.mime.text.MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = email.header.Header(subject, 'utf-8')
    msg['From'] = G.smtp_sender
    msg['To'] = receiver
    if cc:
        msg['Cc'] = cc
        receiver += ',' + cc

    glog.info('Sent mail <{}> with {} bytes to [{}]'.format(subject, len(content), receiver))
    s = smtplib.SMTP(G.smtp_server, G.smtp_port)
    s.ehlo()
    s.starttls()
    s.login(G.smtp_user, G.smtp_pass)
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


def main(argv):
    """As an executable to send emails."""
    receiver, subject, content = sys.stdin.read().split(' ', 2)
    send(subject, content, receiver)

if __name__ == '__main__':
    google.apputils.app.run()
