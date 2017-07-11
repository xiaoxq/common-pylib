#!/usr/bin/env python

"""
Global config.
Usage:
    Init once with:
        config.init(conf_path)
    Then query with:
        config.get(key)
        config.get(key, default)
"""

import ConfigParser

import colored_glog as glog

_conf = {}


def init(conf_path):
    """Init global conf dict from conf_path."""
    global _conf
    cf = ConfigParser.SafeConfigParser()
    cf.read(conf_path)
    for line in file(conf_path):
        line = line.strip()
        if line.startswith('[') and line.endswith(']'):
            _conf.update(cf.items(line[1:-1]))
    glog.info('Get global config: {}'.format(_conf))


def put(key, val):
    """Put extra entry."""
    global _conf
    _conf[key] = val


def get(key, default=None):
    """Get key from global config."""
    global _conf
    if not _conf:
        glog.error('Config has not been initialized yet')
        return default
    return _conf.get(key, default)
