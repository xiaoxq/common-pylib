"""
MongoDB util.
Requirements: pip install glog pymongo (>=3.4)

Usages:
users = get_collection('mydb', 'users')         # Get collection.

################################################# Insert
users.insert(user_doc)                          # Async insert.
users.insert(user_doc, w=2)                     # At least insert to 2 nodes.

################################################# Lookup
find_query = {
    "firstname": "jane",
    "score": {"$gt": 0},
    # Other selectors: gt, lt, gte, lte, ne; exists, in, nin, or, nor, all, mode, size
}
fields_selector = {
    "email": 1
}
sort_query = ("dateofbirth", pymongo.DESCENDING)

users.find()
users.find(find_query)
users.find(find_query, fields_selector)
users.find(find_query, snapshot=True)
users.find_one(...)

# Cascade operations
...find().count()
...find().sort(sort_query).limit(10).skip(20)

################################################# Update
update_query = {
    "$set": {
        "email": "janedoe74@example2.com"
    },
    "$unset": {
        "phone": 1
    },
    # Other updaters: inc, push, pushAll, pop, pull, pullAll, addToSet, rename
}

users.update(find_query, new_user_doc)          # Async full update.
users.update(find_query, update_query)          # Async partial update.
users.find_and_modify(find_query, update_query) # Also return the doc.
users.update(..., w=2)                          # Sync update.
users.update(..., multi=True)                   # Update multiple.
users.update(..., upsert=True)                  # Update or insert.

################################################# Delete
users.remove(find_query)                        # Async remove.
users.remove(find_query, safe=True)             # Sync remove.
users.remove(None, safe=True)                   # Remove all.
################################################# Index
users.create_index('username')                  # Create single index.
users.create_index('username', name='name_idx') # Create named index.
users.create_index([("first_name", pymongo.ASCENDING), ...] # Create multi indexes.
users.drop_index('username')                    # Drop single index.
users.drop_index('name_idx')                    # Drop named index.
users.drop_indexes()                            # Drop all indexes.
"""
import gflags
import pymongo

gflags.DEFINE_string('mongo_host', '0.0.0.0', 'MongoDB host ip.')
gflags.DEFINE_integer('mongo_port', 27017, 'MongoDB port.')
gflags.DEFINE_string('mongo_db_name', None, 'MongoDB db name.')
gflags.DEFINE_string('mongo_user', None, 'MongoDB user.')
gflags.DEFINE_string('mongo_pass', None, 'MongoDB password.')


def _get_db():
    G = gflags.FLAGS
    client = pymongo.MongoClient(G.mongo_host, G.mongo_port)
    db = client[G.mongo_db_name]
    db.authenticate(gflags.FLAGS.mongo_host, config.get('mongodb_pass'))
    return db


def get_collection(collection_name):
    """Get DB handler."""
    return _get_db()[collection_name]

if __name__ == "__main__":
    print _get_db().collection_names()
