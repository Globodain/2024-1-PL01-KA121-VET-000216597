import os
from flask import (
    Flask, render_template, redirect,
    url_for, flash, request, current_app
)
from flask_login import (
    LoginManager, UserMixin,
    login_user, login_required,
    logout_user, current_user
)
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
from datetime import datetime
from werkzeug.security import (
    generate_password_hash, check_password_hash
)
from forms import (
    LoginForm, RegisterForm,
    ProfileForm, PostForm, CommentForm
)

app = Flask(__name__)
app.config.update(
    SECRET_KEY='your_secret_key_here',
    MONGO_URI='mongodb://localhost:27017/blog_app',
    UPLOAD_FOLDER='static/avatars',
    MAX_CONTENT_LENGTH=2 * 1024 * 1024,
    ALLOWED_EXTENSIONS={'png', 'jpg', 'jpeg', 'gif'}
)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

mongo = PyMongo(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, data):
        self.id = str(data['_id'])
        self.username = data['username']
        self.role = data['role']
        self.avatar = data.get('avatar')


@login_manager.user_loader
def load_user(user_id):
    data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    return User(data) if data else None


def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
    )


@app.route('/')
def index():
    raw_posts = list(mongo.db.posts.find().sort('created_at', -1))
    posts = []
    for p in raw_posts:
        author = mongo.db.users.find_one({'_id': p['author_id']})
        posts.append({
            'id': str(p['_id']),
            'title': p['title'],
            'body': p['body'],
            'likes': p.get('likes', 0),
            'comments': mongo.db.comments.count_documents({'post_id': p['_id']}),
            'author_name': author['username'],
            'author_avatar': author.get('avatar'),
            'author_role': author['role']
        })
    return render_template('index.html', posts=posts)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    post = mongo.db.posts.find_one({'_id': ObjectId(post_id)})
    if not post:
        return "Post not found", 404

    # Handle "like"
    if request.method == 'POST' and request.form.get('action') == 'like':
        if not current_user.is_authenticated:
            flash('Please log in to like posts')
            return redirect(url_for('login'))
        mongo.db.posts.update_one(
            {'_id': ObjectId(post_id)},
            {'$inc': {'likes': 1}}
        )
        return redirect(url_for('post_detail', post_id=post_id))

    # Handle new comment
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('Please log in to comment')
            return redirect(url_for('login'))
        mongo.db.comments.insert_one({
            'post_id': post['_id'],
            'user_id': ObjectId(current_user.id),
            'content': comment_form.content.data,
            'created_at': datetime.utcnow()
        })
        return redirect(url_for('post_detail', post_id=post_id))

    # Fetch comments
    raw_comments = list(mongo.db.comments.find(
        {'post_id': post['_id']}
    ).sort('created_at', 1))
    comments = []
    for c in raw_comments:
        user = mongo.db.users.find_one({'_id': c['user_id']})
        comments.append({
            'username': user['username'],
            'avatar': user.get('avatar'),
            'content': c['content'],
            'created_at': c['created_at']
        })

    # Compose post data
    author = mongo.db.users.find_one({'_id': post['author_id']})
    post_data = {
        'id': str(post['_id']),
        'title': post['title'],
        'body': post['body'],
        'likes': post.get('likes', 0),
        'comments_count': len(comments),
        'author_name': author['username'],
        'author_avatar': author.get('avatar'),
        'author_role': author['role']
    }

    return render_template(
        'post.html',
        post=post_data,
        comments=comments,
        form=comment_form
    )


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        if mongo.db.users.find_one({'username': form.username.data}):
            flash('Username already taken')
        else:
            mongo.db.users.insert_one({
                'username': form.username.data,
                'password_hash': generate_password_hash(form.password.data),
                'role': 'user',
                'avatar': None
            })
            flash('Registration successful—please log in')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        data = mongo.db.users.find_one({'username': form.username.data})
        if data and check_password_hash(data['password_hash'], form.password.data):
            login_user(User(data))
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        update = {'username': form.username.data}
        file = form.avatar.data
        if file and allowed_file(file.filename):
            fn = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], fn))
            update['avatar'] = fn
        mongo.db.users.update_one(
            {'_id': ObjectId(current_user.id)},
            {'$set': update}
        )
        flash('Profile updated')
        return redirect(url_for('profile'))
    return render_template('profile.html', form=form)


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    # Both 'admin' and 'user' can create here
    form = PostForm()
    if form.validate_on_submit():
        mongo.db.posts.insert_one({
            'title': form.title.data,
            'body': form.body.data,
            'created_at': datetime.utcnow(),
            'likes': 0,
            'author_id': ObjectId(current_user.id)
        })
        flash('Your post has been published!')
        return redirect(url_for('index'))
    return render_template('create.html', form=form)


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_page():
    if current_user.role != 'admin':
        return "Access denied", 403
    # Admin panel still allows post creation if you wish
    form = PostForm()
    if form.validate_on_submit():
        mongo.db.posts.insert_one({
            'title': form.title.data,
            'body': form.body.data,
            'created_at': datetime.utcnow(),
            'likes': 0,
            'author_id': ObjectId(current_user.id)
        })
        flash('New post added')
        return redirect(url_for('admin_page'))
    posts = list(mongo.db.posts.find().sort('created_at', -1))
    return render_template('admin.html', form=form, posts=posts)

@app.route('/admin/delete/<post_id>', methods=['POST'])
@login_required
def admin_delete_post(post_id):
    if current_user.role != 'admin':
        return "Access denied", 403

    mongo.db.posts.delete_one({'_id': ObjectId(post_id)})
    mongo.db.comments.delete_many({'post_id': ObjectId(post_id)})
    flash('Post has been deleted')
    return redirect(url_for('admin_page'))





if __name__ == '__main__':
    app.run(debug=True)
