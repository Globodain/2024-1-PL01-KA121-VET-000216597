# Microblog

Author: Oliwier Adamczyk


### How to run

1. Download [Docker](https://www.docker.com/)
2. Run docker
3. Run command in terminal
    - development:
    
        ``docker-compose up --build``
    - production:

        ``docker build -t microblog .``

        ``docker run -p 5000:5000 -e FLASK_ENV=production microblog``


3. Then go to http://127.0.0.1:5000/

### Screenshots

![home](/screenshots/home.png)

![create_account](/screenshots/create_account.png)

![profile](/screenshots/profile.png)

![sign_in](/screenshots/sign_in.png)