# Telegram bot framework
import requests
import datetime
import time
import re
import json
import threading
import signal
from collections import deque


# Telegram bot credentials
bot_token = ''



class Bot(object):

    def __init__(self, bot_token):
        self.bot_url = 'https://api.telegram.org/bot%s/' %(bot_token)
        self.msg_queue = deque([])

    # Long polling for message updates, this is how new messages are read by the bot
    def message_poll(self):
        self.offset = 0
        update_url = self.bot_url+'getUpdates'
        while True:
            payload = {'timeout':'30','offset':self.offset}
            # Get the message JSON object and decode the JSON
            try:
                r = requests.get(update_url,params=payload).json()
                if r['result']:
                    self.offset = r['result'][0]['update_id'] + 1
                    # print(r)
                    # Queueing for future expansion and multithreading
                    #self.msg_queue.append(r)
                    #received = self.msg_queue.popleft()
                    self.message_parsing(r)
            except:
                print('Error with message poll')


    # Send message function
    def send_message(self, response_text, chat_id):
        sendmessage_url = bot_url+'sendMessage'
        payload = {'chat_id':chat_id, 'text':response_text}
        r = requests.get(sendmessage_url, params=payload)


    def message_parsing(self, r):
        try:
            # Get each piece of information from the Updates
            #offset = r['result'][0]['update_id'] + 1
            self.key_list = r['result'][0]['message'].keys()
            self.message_userid = r['result'][0]['message']['chat']['id']
            self.sender_name = r['result'][0]['message']['from']['first_name']
            self.message_time = int(r['result'][0]['message']['date'])
            self.curr_time = int(time.time())

            # Response for text, and only respond if the message read was sent <10 sec ago
            if 'text' in self.key_list and (self.message_time + 10) > self.curr_time:
                self.message_text = r['result'][0]['message']['text']
                print(self.message_text)
                print(self.message_userid)
                #text_check(message_text, message_userid, sender_name)
        except:
            print("Error with parsing message")


    # Check text based message for keywords
    def text_check(self, message_text, message_userid, sender_name):
        # Make the whole message lower case so I can compare strings
        message_text = message_text.lower()
        if re.search('/ipadd', message_text):
            pi_ip = requests.get('http://httpbin.org/ip').json()['origin']
            send_message(pi_ip, message_userid)

        if re.search('teststring', message_text):
            send_message('hi there', message_userid)



Bot(bot_token).message_poll()
