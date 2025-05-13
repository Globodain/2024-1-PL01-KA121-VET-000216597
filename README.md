# Lukas Blog

A simple Flask + MongoDB blog application in Python 3.11


## 📝 Base Project Report

**Technologies & Libraries**  
- **Flask** - web framework  
- **Flask-Login** - session & authentication  
- **Flask-WTF** - forms & CSRF protection  
- **Flask-PyMongo** - MongoDB integration  
- **Werkzeug** - password hashing  
- **Bootstrap 5** - responsive UI 
- **FontAwesome** - Icons  
- **MongoDB** - document database  


## 🚀 Deployment Instructions

**1. Clone & Set Up**
```git clone https://github.com/
cd lukas-blog
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt```

**2. Configuration**
```export FLASK_APP=app.py
export FLASK_ENV=development       
export SECRET_KEY='your_secret_key'
export MONGO_URI='mongodb://localhost:27017/blog_app'```

**3. Seed Database**
```python seed_data.py```

**4. Run Development Server**
```flask run```

**5. Visit: http://127.0.0.1:5000/**
