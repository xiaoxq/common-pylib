"""GFlags utils."""
import gflags
import glog
import sys


def init():
    """Init gflags from argv."""
    try:
        sys.argv = gflags.FLAGS(sys.argv)
    except gflags.FlagsError, e:
        glog.fatal('\n{}\nUsage: {} ARGS\n{}'.format(e, sys.argv[0], gflags.FLAGS))
        sys.exit(1)

    for k, v in gflags.FLAGS.FlagValuesDict().iteritems():
        glog.info('FLAG: {} = {}'.format(k, v))
    glog.info('NON-FLAG arguments: {}'.format(sys.argv))
