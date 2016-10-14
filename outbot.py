from flask import Flask, request
import requests
import sys
import os
import json
from Credentials import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def handle_verification():
    if request.args.get('hub.verify_token', '') == VERIFY_TOKEN:
        return request.args.get('hub.challenge', 200)
    else:
        return 'Error, wrong validation token'


@app.route('/', methods=['POST'])
def handle_messages():
    data = request.get_json()
    log(data)

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
           
                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    recipient_id = messaging_event["recipient"]["id"]
                    message_text = messaging_event["message"]["seq"]

                    send_message(sender_id, message_text)
                    kitten(sender_id) 
                    menu(sender_id)

                if messaging_event.get("delivery"):
                    pass

                if messaging_event.get("optin"):
                    pass

                if messaging_event.get("postback"):
                    receivedPostback(messaging_event)

    return "ok", 200


def send_message(recipient_id, message_text):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
     })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
    log(r.text)


def log(message):  # Wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


def kitten(recipient_id):
    log("sending message to {recipient}: ".format(recipient=recipient_id))

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "recipient": json.dumps({
            "id": recipient_id
        }),
        "message": json.dumps({
            "attachment": {
                "type": "image",
                "payload": {
                    'url': "http://placekitten.com/g/200/300/"
                           }
                           }
                })
            }

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=payload)
    if r.status_code != 200:
        log(r.status_code)
#    log(r.text)


def menu(recipient_id):
    buttons = []
    button = {'title':"Arsenal", 'type':'web_url', 'url':'http://arsenal.com'}
    buttons.append(button)
    button = {'title':'Other', 'type':'postback', 'payload':'other'}
    buttons.append(button)
    text = 'Select'
    result = button_message(recipient_id, text, buttons)


def button_message(recipient_id, text, buttons):
    log("sending message to {recipient}: ".format(recipient=recipient_id))

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
            'recipient': json.dumps(
                {
                    'id': recipient_id
                    }
                ),
            'message': json.dumps(
                {
                    'attachment': {
                        'type' : 'template',
                        'payload': {
                            'template_type': 'button',
                            'text': text,
                            'buttons': buttons
                            }
                        }
                    }
               )
            }


def receivedPostback(event):
    sender_id = event['sender']['id']
    recipient_id = event['recipient']['id']
    time = event['timestamp']

    payload = event['postback']['payload']

    send_message(sender_id, 'Postback called')


    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=payload)
    if r.status_code != 200:
        log(r.status_code)
    log(r.text)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
