#/bin/bash

cd ~/workspace/screen-message-delivery/
# comment out the following line if run in virtualenv
#source ~/.envs/flask/bin/activate
export FLASK_APP=main.py
export FLASK_DEBUG=False
flask run --host 0.0.0.0 &
sleep 5s # waiting flask

while [ true ]
do
    #-o /dev/null throws away the usual output
    #--silent throws away the progress meter
    #--head makes a HEAD HTTP request, instead of GET
    #--write-out '%{http_code}\n' prints the required status code
    status=$(curl -o /dev/null --silent --head --write-out '%{http_code}\n' http://127.0.0.1:5000/)
    if [ "$status" != 200 ]
    then
        echo "waiting..."
        sleep 5s # waiting flask
        status=$(curl -o /dev/null --silent --head --write-out '%{http_code}\n' http://127.0.0.1:5000/)
    else
        break
    fi
done

chromium --noerrdialogs --kiosk http://127.0.0.1:5000/detail/
