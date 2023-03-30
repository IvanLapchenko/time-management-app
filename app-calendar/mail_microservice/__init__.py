import time
import json
import requests
from flask import Flask
from credintials import *
from flask_mail import Mail, Message


app = Flask(__name__)


app.config['MAIL_SERVER'] = 'smtp.ukr.net'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = email
app.config['MAIL_PASSWORD'] = password
app.config['MAIL_DEFAULT_SENDER'] = email
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
app.app_context().push()


def send_email(recipient, header, body):
    msg = Message('Event reminder', recipients=[recipient])
    msg.body = header
    msg.html = body
    mail.send(msg)
    print('Email sent')


def check_for_events():
    while True:
        events = requests.get("http://127.0.0.1:5000/check_for_near_events")
        events = events.json()

        #перевіряємо чи були отримані події на цю хвилину
        if len(events) > 0:
            for event in events:
                event = json.loads(event)

                id = event["user"]
                header = event["header"]
                body = f"{event['time']} \n {event['describe']}"
                # робимо звернення до бд щоб отримати емейл, на який потрібно відправити лист
                recipient = requests.get(f"http://127.0.0.1:5000/get_user_email_by_id/{id}").json()
                recipient = recipient["user_mail"]

                send_email(recipient, header, body)
        time.sleep(60)


check_for_events()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)