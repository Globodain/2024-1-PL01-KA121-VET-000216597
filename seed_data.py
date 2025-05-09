from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime

client = MongoClient('mongodb://localhost:27017')
db = client['blog_app']

db.users.delete_many({})
db.posts.delete_many({})
db.comments.delete_many({})

db.users.insert_many([
    {
        'username': 'admin',
        'password_hash': generate_password_hash('adminpass'),
        'role': 'admin',
        'avatar': None
    },
    {
        'username': 'user',
        'password_hash': generate_password_hash('userpass'),
        'role': 'user',
        'avatar': None
    }
])

# Optional: seed one sample post
db.posts.insert_one({
    'title': 'Welcome to Lukas Blog!',
    'body': 'This is the first post. Admin posts will show a ★.',
    'created_at': datetime.utcnow(),
    'likes': 0,
    'author_id': db.users.find_one({'username': 'admin'})['_id']
})

print("Seed complete.")
