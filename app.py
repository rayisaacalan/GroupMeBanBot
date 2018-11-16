import os
import sys
import json
import groupy
from groupy.client import Client, attachments
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.getenv('GM_TOKEN')
GMClient = Client.from_token(TOKEN)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    if data['name'] != 'Testy McTestson':
        msg = '{}, you just said "{}". Your user id is {} and your membership id is {}.'.format(data['name'], data['text'], data['user_id'], data['id'])
        print(data, flush = True)
        send_message(msg)
    return "ok", 200

def send_message(msg):
    url = 'https://api.groupme.com/v3/bots/post'

    data = {
            'bot_id' : os.getenv('GROUPME_TESTBOT_ID'),
            'text'   : msg,
    }
    request = Request(url, urlencode(data).encode())
    json = urlopen(request).read().decode()
