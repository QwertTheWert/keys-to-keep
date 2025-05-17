# Keys 2 Keep 
## Installation Guide

1. Pastikan [Python 3.13.2](https://www.python.org/) terinstall dan dimasukan ke path
2. Pastikan [DB Browswer for SQLite](https://sqlitebrowser.org/dl/) terinstall dan dimasukan ke path
3. Di directory applikasi ini, buatlah virtual environment python (nama bebas, tapi aku pake flask) `python -m venv flask`
4. Activate environment `flask/Scripts/activate.bat`
5. Jalankan code ini untuk download library `python -m pip install -r requirements.txt`
6. Jika belum ada database, lalukan perintah ini di console
```
py
from app import db, create_app, create_dummy_data
db.create_all()
new_app.app_context().push()
create_dummy_data()
exit()
```

That should be it.
