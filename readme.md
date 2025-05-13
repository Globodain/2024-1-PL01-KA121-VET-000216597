Write here the final project report and how deploy your code


------------------------------------------------
Required Python packages
------------------------------------------------
Execute this to generate file with rquired Python packages:
pip freeze > requirements.txt

Execute this to install all Python listed in requirements.txt:
pip install -r requirements.txt



------------------------------------------------
Database migrations and updates
------------------------------------------------
Execute this to create a new migration:
flask db migrate -m "{optional name}"

Execute this to upgrade database through all migrations:
flask db upgrade



------------------------------------------------
Flask-Babel
------------------------------------------------

To add new language execute:
flask translate init <language-code>

To update languages execute:
flask translate update

To compile languages after updating execute:
flask translate compile



------------------------------------------------
translation service
------------------------------------------------
Execute this with your key to the Microsoft Translator API:
set MS_TRANSLATOR_KEY=<paste-your-key-here>