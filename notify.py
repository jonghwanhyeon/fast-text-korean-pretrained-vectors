# This script is for sending a notification via Pushover (https://pushover.net)
# To use this, you must configure `authentication.json` first

import os
import sys
import json
import time

import requests

number_of_attempts = 5
authentication_filename = 'authentication.json'

base_path = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists(os.path.join(base_path, authentication_filename)):
    sys.exit('{} does not exist'.format(authentication_filename))

if len(sys.argv) == 1:
    sys.exit('Usage: python3 {} <message>'.format(sys.argv[0]))

with open(os.path.join(base_path, authentication_filename), 'r', encoding='utf-8') as input_file:
    authentication = json.load(input_file)

parameters = {
    'user': authentication['user_key'],
    'token': authentication['api_token'],
    'message': ' '.join(sys.argv[1:])
}

success = False
for attempt in range(0, number_of_attempts):
    try:
        response = requests.post('https://api.pushover.net/1/messages.json', data=parameters)
        if response.status_code == 200:
            success = True
            break
    except:
        pass

    if not success:
        time.sleep(1)

if success:
    print('Notification sent')
else:
    sys.exit('An error occurred during sending notification')
