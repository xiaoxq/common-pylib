"""
Global config.
Usage:
    Init once with:
        config.init(conf_path, 'section')
        config.init(conf_path, ('section1', 'section2', ...))
    Then query with:
        config.get(key)
        config.get(key, default)
"""

import ConfigParser
import sys
import types

_conf = None


def init(conf_path, section):
    """Init the conf from conf_path."""
    global _conf
    _conf = {}

    cf = ConfigParser.SafeConfigParser()
    cf.read(conf_path)
    def _read_section(sec):
        for k, v in cf.items(sec):
            _conf[k] = v
    if type(section) == types.StringType:
        _read_section(section)
    else:
        for sec in section:
            _read_section(sec)
    print 'INFO: Get config:', _conf


def init_or_die(conf_path, section='base'):
    """Init the conf from conf_path, or die on failures."""
    try:
        init(conf_path, section)
    except Exception as e:
        sys.stderr.write(str(e))
        sys.exit(1)

    global _conf
    if len(_conf) == 0:
        sys.stderr.write('ERROR: Config is empty after reading {}'.format(conf_path))
        sys.exit(1)


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
    if not _conf:
        sys.stderr.write('ERROR: Config has not been initialized yet\n')
        return default
    return _conf.get(key, default)
