# cara import psql dari sql dump file:
# buat database yg namanya sama
# jika sudah ada DB ny, maka
# cek dulu nama schema yg sudah ada denga perintah \dn 
# drop dulu semua table ny dengan menggunakan nama schema ny,  kemudian buat schema barunya:
# drop schema nama_schema;
# create schema nama_schema;
# setelah itu baru import dengan perintah
# psql -h nama_host(bisa pakai localhost) -U namaa_username -d nama_database -f nama_file_dump

sudo apt install python3.10
pip install pyinstaller

pip install escpos
pip install configparser

pip install PyQt5

pip install opencv-python

pip install postgres

pip install fpdf
pip install keyboard
pip install pynput 

sudo apt install postgresql postgresql-contrib
sudo apt install python3-pip
pip install fpdf keyboard pynput PyQt5 configparser opencv-python python-escpos-win psycopg2
