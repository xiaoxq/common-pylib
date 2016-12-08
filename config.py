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


def get(key, default=None):
    """Get key from global config."""
    global _conf
    if not _conf:
        print 'ERROR: Config has not been initialized yet'
        return default
    return _conf.get(key, default)
