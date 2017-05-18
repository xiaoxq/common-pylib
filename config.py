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


def init_conf_dict(conf_path):
    """Init a conf dict from conf_path."""
    conf_dict = {}
    cf = ConfigParser.SafeConfigParser()
    cf.read(conf_path)
    for line in file(conf_path):
        line = line.strip()
        if line.startswith('[') and line.endswith(']'):
            conf_dict.update(cf.items(line[1:-1]))
    return conf_dict

_conf = {}


def init(conf_path):
    """Init global conf dict from conf_path."""
    global _conf
    _conf.update(init_conf_dict(conf_path))
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
