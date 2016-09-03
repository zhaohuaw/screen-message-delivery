#/bin/bash

cd ~/workspace/screen-message-delivery/
source ~/.envs/flask/bin/activate
export FLASK_APP=main.py
export FLASK_DEBUG=False
flask run &
sleep 5s # waiting flask

#-o /dev/null throws away the usual output
#--silent throws away the progress meter
#--head makes a HEAD HTTP request, instead of GET
#--write-out '%{http_code}\n' prints the required status code
status = $(curl -o /dev/null --silent --head --write-out '%{http_code}\n' http://127.0.0.1:5000/)

while [$status != 200]
do
sleep 5s # waiting flask
status = $(curl -o /dev/null --silent --head --write-out '%{http_code}\n' http://127.0.0.1:5000/)
done

google-chrome --kiosk http://127.0.0.1:5000/detail/
