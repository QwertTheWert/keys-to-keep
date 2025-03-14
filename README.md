# Keys 2 Keep 
## Installation Guide

1. Pastikan [Python 3.13.2](https://www.python.org/) terinstall
2. Pastikan [SQLite 3.49.1](https://www.sqlite.org/download.html) terinstall dan dimasukan ke path
3. Di directory applikasi ini, buatlah virtual environment python (nama bebas, tapi aku pake flask) `python -m venv flask`
4. Activate environment `flask/Scripts/activate.bat`
5. Jalankan code ini untuk download library `python -m pip install -r requirements.txt`
6. Initialisasi database dengan menjalankan code berikut di terminal, un-comment line 7-9 di file `main.py`, lalu jalankan kode, kemudian comment-kan lagi ketiga line tersebut.\n
	**Special:** Jika sudah pernah install, coba migrate database ke versi terbaru dan tidak perlu create databsae lagi.
	```flask db migrate
	flask db upgrade``` 
	* Jika error, hapusa `database.db` di folder instance lalu jalankan perintah no. 6

That should be it.