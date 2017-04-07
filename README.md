# Simple financial system
---
This system is made to help the cashier (me) at
[Østervold Kollegiet](osetervold.dk).

### Setup
First you have to install `Python 3.x` and `pip`.
Then the following commands should be run:
```bash
pip install virtualenv
virtualenv -p /usr/bin/python3.4 virtualenv # Maybe the path should be changed
source virtualenv/bin/activate
pip install -r requirements.txt
./manage.py migrate
./manage.py loaddata fixtures/templates.json
./manage.py loaddata fixtures/unions.json
./manage.py loaddata fixtures/departments.json
./manage.py runserver
source virtualenv/bin/activate
./manage.py runserver
```

After each pull you should run.
```bash
./manage.py migrate
```
