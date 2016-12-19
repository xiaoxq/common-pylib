"""
MongoDB util.

Usages:
users = get_collection('mydb', 'users') # Get collection.

######################################### Insert
users.insert(user_doc)                  # Async insert.
users.insert(user_doc, safe=True)       # Sync insert.
users.insert(user_doc, w=2)             # At least insert to 2 nodes.

######################################### Lookup
find_query = {
    "firstname": "jane",
    "score": {"$gt": 0},
    # Other selectors: gt, lt, gte, lte, ne; exists, in, nin, or, nor, all, mode, size
}
sort_query = ("dateofbirth", pymongo.DESCENDING)

users.find()
users.find(query_dict)
users.find(query_dict, snapshot=True)
users.find_one(...)

# Cascade operations
...find().count()
...find().sort(sort_query).limit(10).skip(20)

######################################### Update
update_query = {
    "$set": {
        "email": "janedoe74@example2.com"
    },
    "$unset": {
        "phone": 1
    },
    # Other updaters: inc, push, pushAll, pop, pull, pullAll, addToSet, rename
}

users.update(find_query, new_user_doc)  # Async full update.
users.update(find_query, update_query)  # Async partial update.
users.update(..., safe=True)            # Sync update.
users.update(..., multi=True)           # Update multiple.

######################################### Delete
users.remove(find_query)                # Async remove.
users.remove(find_query, safe=True)     # Sync remove.
users.remove(None, safe=True)           # Remove all.
"""
import pymongo
import sys

import config

_conn = None
def _conn_singleton():
    global _conn
    if _conn:
        return _conn

    try:
        _conn = pymongo.Connection(host=config.get('mongodb_host', 'localhost'),
                                   port=int(config.get('mongodb_port', 27017)))
        print 'INFO: Connect to MongoDB successfully'
    except pymongo.errors.ConnectionFailure, e:
        sys.stderr.write('ERROR: Could not connect to MongoDB: %s' % e)
        sys.exit(1)
    return _conn

def get_collection(db_name, collection_name):
    """Get DB handler."""
    return _conn_singleton()[db_name].__getattr__(collection_name)


if __name__ == "__main__":
    config.put('mongodb_host', 'localhost')
    config.put('mongodb_port', 27017)
    print _conn_singleton().database_names()
