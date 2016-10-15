# Import packages
from flask import Flask, request
import requests
import sys
import os
import json
from Credentials import *

# Initialize app
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

                   # send_message(sender_id, message_text)
                    kitten(sender_id) 
                    main_menu(sender_id)

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
    log(r.text)


def main_menu(recipient_id):
    buttons = []
    button = {'title':"Upload a picture", 'type':'postback', 'payload':'upload'}
    buttons.append(button)
    button = {'title':'Browse recommendations', 'type':'postback', 'payload':'browse'}
    buttons.append(button)
    text = 'What would you like to do?'

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

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=payload)
    if r.status_code != 200:
        log(r.status_code)
    log(r.text)


def upload_menu(recipient_id):
    buttons = []
    button = {'title':"Womenswear", 'type':'postback', 'payload':'womens'}
    buttons.append(button)
    button = {'title':'Menswear', 'type':'postback', 'payload':'mens'}
    buttons.append(button)
    button = {'title':'Main menu', 'type':'postback', 'payload':'main'}
    buttons.append(button)
    text = 'Are you looking for Womenswear or Menswear?'

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

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=payload)
    if r.status_code != 200:
        log(r.status_code)
    log(r.text)


def womens(recipient_id): 

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
                            'template_type': 'generic',
                            'elements': [
                                {
                                    'title': 'Swipe left/right for more options',
                                    'buttons': [
                                        {
                                            'type': 'postback',
                                            'title': 'Tops',
                                            'payload': 'tops_women'
                                            },
                                        {
                                            'type': 'postback',
                                            'title': 'Bottoms',
                                            'payload': 'bottoms_women'
                                            },
                                        {
                                            'type': 'postback',
                                            'title': 'Main menu',
                                            'payload': 'main'
                                            }
                                        ]
                                    },
                                {
                                    'title': 'Swipe right/left for more options',
                                    'buttons': [
                                        {
                                            'type': 'postback',
                                            'title': 'Dresses',
                                            'payload': 'dresses'
                                            },
                                        {
                                            'type': 'postback',
                                            'title': 'Main menu',
                                            'payload': 'main'
                                            }
                                        ]
                            }
                        ]
                        }
                    }
                }
               )
            }

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=payload)
    if r.status_code != 200:
        log(r.status_code)
    log(r.text)



def mens_menu(recipient_id):
    buttons = []
    button = {'title':"Tops", 'type':'postback', 'payload':'tops_men'}
    buttons.append(button)
    button = {'title':'Bottoms', 'type':'postback', 'payload':'bottoms_men'}
    buttons.append(button)
    button = {'title': 'Main menu', 'type':'postback', 'payload':'main'}
    buttons.append(button)
    text = 'What type are you looking for?'

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

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=payload)
    if r.status_code != 200:
        log(r.status_code)
    log(r.text)


def receivedPostback(event):
    sender_id = event['sender']['id']
    recipient_id = event['recipient']['id']
    time = event['timestamp']

    payload = event['postback']['payload']

    if payload == 'upload':
        upload_menu(sender_id)
    if payload == 'browse':
        send_message(sender_id, 'Postback black')
    if payload == 'womens':
        womens(sender_id)
    if payload == 'mens':
        mens_menu(sender_id)
    if payload == 'main':
        main_menu(sender_id)
    if payload == 'tops_womens':
        send_message(sender_id, 'W Tops')
    if payload == 'bottoms_women':
        send_message(sender_id, 'W Bottoms')
    if payload == 'dresses':
        send_message(sender_id, 'Dresses')
    if payload == 'tops_mens':
        send_message(sender_id, 'Upload picture!')
    if payload == 'bottoms_men':
        send_message(sender_id, 'M Bottoms')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
