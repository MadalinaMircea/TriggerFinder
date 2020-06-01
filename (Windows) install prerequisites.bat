python -m venv venv
venv\Scripts\activate
pip install --update pip
pip install --update tensorflow==2.2.0
pip install --update nltk==3.5
pip install --update numpy==1.18.4
pip install flask
cd backend
cd TriggerFinder
set FLASK_APP=main.py