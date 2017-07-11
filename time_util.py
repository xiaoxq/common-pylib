#!/usr/bin/env python
#  coding: utf-8

"""Time utils."""

import datetime
import pytz
import re

import gflags

import colored_glog as glog

gflags.DEFINE_string('timezone', 'America/Los_Angeles', 'Timezone.')

EPOCH = datetime.datetime(1970, 1, 1)


def datetime_to_timestamp(dt):
    """Seconds since epoch."""
    return int((dt - EPOCH).total_seconds())


def time_str_to_timestamp(datetime_str):
    """
    Convert any datetime string, such as '2010-10-10-00-00-00', '20101010000000' or
    '2010-10-10 00:00:00' to seconds since EPOCH.
    """
    packed_str = re.sub("[^0-9]", "", datetime_str)
    if len(packed_str) >= 14:
        dt = datetime.datetime.strptime(packed_str[:14], '%Y%m%d%H%M%S')
    elif len(packed_str) >= 12:
        dt = datetime.datetime.strptime(packed_str[:12], '%Y%m%d%H%M')
    elif len(packed_str) >= 8:
        dt = datetime.datetime.strptime(packed_str[:8], '%Y%m%d')
    else:
        glog.error('Unknown time str: {}'.format(datetime_str))
        return -1
    return datetime_to_timestamp(dt)


def timestamp_to_time_str(ts, format='%Y-%m-%d-%H-%M-%S'):
    """Convert seconds since epoch to '2010-10-10-00-00-00'."""
    dt = EPOCH + datetime.timedelta(seconds = int(ts))
    return dt.strftime(format)


def current_time_str(format='%Y-%m-%d-%H-%M-%S'):
    """Get current time string."""
    return datetime.datetime.now(pytz.timezone(gflags.FLAGS.timezone)).strftime(format)


def current_timestamp():
    """Get current timestamp."""
    return time_str_to_timestamp(current_time_str())

if __name__ == '__main__':
    if time_str_to_timestamp('19700101-010000') != 3600:
        glog.fatal('Wrong result: 19700101-010000 -> {}'.format(
                time_str_to_timestamp('19700101-010000')))
    elif timestamp_to_time_str(3600) != '1970-01-01-01-00-00':
        glog.fatal('Wrong answer: 3600 -> {}'.format(timestamp_to_time_str(3600)))
    else:
        glog.info('All passed!')
