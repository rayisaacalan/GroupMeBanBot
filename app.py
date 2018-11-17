import os
import sys
import json
import groupy
import random
from groupy.client import Client, attachments
from groupy.api import memberships
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request
#import requests

app = Flask(__name__)

TOKEN = os.getenv('GM_TOKEN')
GMClient = Client.from_token(TOKEN) #Returns a "session"
BANNABLE_USER = os.getenv('BAN_USER_ID') #user_id
GROUP_ID = os.getenv('GROUP_ID')
BOT_ID = os.getenv('GROUPME_TESTBOT_ID')

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print(data, flush = True)
    if data['user_id'] == BANNABLE_USER:
        print('Bannable User posted message!')
        if not random.randint(0,1):
            print('Bannable user got unlucky!')
            remove_user(data['id'])
    return "ok", 200

def send_message(msg):
    url = 'https://api.groupme.com/v3/bots/post'

    data = {
            'bot_id' : BOT_ID,
            'text'   : msg,
    }
    request = Request(url, urlencode(data).encode())
    json = urlopen(request).read().decode()
    #print("RESPONSE:")
    #print(json, flush = True)

def remove_user(memID):
    print('Made it to remove_user() with memID = '+ memID)
    send_message('That was not very cash money of you.')
    GMManager = groupy.api.base.Manager
    GMManager.session = GMClient
    GMManager.url = ('https://api.groupme.com/v3/'+'/groups/'+GROUP_ID+'/members/'+memID+'/remove')
    MemManager = groupy.api.memberships.Memberships(GMManager)
    MemManager.__init__(GMClient, GROUP_ID)
    MemManager.remove(memID)


    #groupy.api.memberships.remove(memID)
