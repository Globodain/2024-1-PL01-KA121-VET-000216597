from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client['blog_app']

# dodaj liked_by = [] tam gdzie brak
db.posts.update_many(
    {'liked_by': {'$exists': False}},
    {'$set': {'liked_by': []}}
)
print("Migration done")
