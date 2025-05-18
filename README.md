# Keys 2 Keep 
## Installation Guide

1. Pastikan [Python 3.13.2](https://www.python.org/) terinstall dan dimasukan ke path
2. Pastikan [DB Browswer for SQLite](https://sqlitebrowser.org/dl/) terinstall 
3. Di directory applikasi ini, buatlah virtual environment python (nama bebas, tapi aku pake flask) `python -m venv flask`
4. Activate environment `flask/Scripts/activate.bat`
5. Jalankan code ini untuk download library `python -m pip install -r requirements.txt`
6. Jika belum ada database, ketik `py` di console untuk buka Python lalu lalukan perintah ini:
```
from app import db, create_app, create_dummy_data
new_app = create_app()
new_app.app_context().push()
db.create_all()
create_dummy_data()
exit()

```

That should be it.
