export PYTHONPATH=/home/Gamble/source/
service nginx restart

cd /home/Gamble/source/ 
chmod -R 777 /var/log/gamble
nohup  python /home/Gamble/source/app.py >> /var/log/gamble/flask_api.log &
python -m pydoc -p 5858