#!/usr/bin/env python
"""
Update docs in mongodb.
Usage:
    # Please see mongodb_util for conf details. Generally you need at least:
    #     mongodb_host / mongodb_port / mongodb_user / mongodb_pass
    python mongodb_update_docs.py <conf_file> <db> <collection>
"""
import bson
import sys

import config
import mongodb_util


def ProcessDoc(doc):
    """Process single doc."""
    return None


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Format: python mongodb_update_docs.py <conf_file> <db> <collection>'
        exit(1)

    config.init(sys.argv[1])
    collections = mongodb_util.get_collection(sys.argv[2], sys.argv[3])

    i = 0
    for doc in collections.find(modifiers={"$snapshot": True}):
        i += 1; print '======================== Processing doc {} ======================='.format(i)
        find_query = {'_id': doc['_id']}
        new_doc = ProcessDoc(doc)
        if new_doc:
            print '********** DO UPDATING **********'
            collections.update(find_query, new_doc, w=1)
