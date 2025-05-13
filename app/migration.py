from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017')
db = client['blog_app']

# Migrate existing posts: set author_id from old author_name, remove old fields
for p in db.posts.find():
    if 'author_id' not in p:
        author = db.users.find_one({'username': p.get('author_name')})
        if author:
            db.posts.update_one(
                {'_id': p['_id']},
                {
                    '$set': {'author_id': author['_id']},
                    '$unset': {
                        'author_name': "", 'author_avatar': "", 'author_role': ""
                    }
                }
            )
print("Migration done.")
