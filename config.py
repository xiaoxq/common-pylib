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
import glog
import sys
import types

_conf = None


def init(conf_path):
    """Init the conf from conf_path."""
    global _conf
    _conf = {}

    cf = ConfigParser.SafeConfigParser()
    cf.read(conf_path)
    for line in file(conf_path):
        line = line.strip()
        if line.startswith('[') and line.endswith(']'):
            for k, v in cf.items(line[1:-1]):
                _conf[k] = v
    glog.info('Get config: {}'.format(_conf))


def put(key, val):
    """Put extra entry."""
    global _conf
    _conf = _conf or {}
    _conf[key] = val


def merge(other_dict):
    """Merge with other dict."""
    global _conf
    _conf = _conf or {}
    for k, v in other_dict.iteritems():
        _conf[k] = v


def get(key, default=None):
    """Get key from global config."""
    global _conf
    if _conf is None:
        glog.error('Config has not been initialized yet')
        return default
    return _conf.get(key, default)
