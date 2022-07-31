# ddns_conf.py
# websupport.sk DNS remote conf script

import smtplib
import os

# api info
api = 'https://rest.websupport.sk'
# place you API key 
apiKey = os.environ['WS_API_KEY']
# place you API secret code 
secret = os.environ['WS_API_SECRET']

# domain related info
user_id = os.environ['WS_USER_ID']
domain = os.environ['WS_DOMAIN']
check_domain = os.environ['WS_CHECK_DOMAIN'] if 'WS_CHECK_DOMAIN' in os.environ else domain

#desired TTL for all records
global_ttl = 666

# particular DNS records
# you may change them as you need - records must exist before (IDs)
record_ids = {}

if 'WS_RECORD_ID_1' in os.environ:
	record_ids[os.environ['WS_RECORD_ID_1']] = os.environ['WS_RECORD_NAME_1']
if 'WS_RECORD_ID_2' in os.environ:
	record_ids[os.environ['WS_RECORD_ID_2']] = os.environ['WS_RECORD_NAME_2']
if 'WS_RECORD_ID_3' in os.environ:
	record_ids[os.environ['WS_RECORD_ID_3']] = os.environ['WS_RECORD_NAME_3']
if 'WS_RECORD_ID_4' in os.environ:
	record_ids[os.environ['WS_RECORD_ID_4']] = os.environ['WS_RECORD_NAME_4']
if 'WS_RECORD_ID_5' in os.environ:
	record_ids[os.environ['WS_RECORD_ID_5']] = os.environ['WS_RECORD_NAME_5']
if 'WS_RECORD_ID_6' in os.environ:
	record_ids[os.environ['WS_RECORD_ID_6']] = os.environ['WS_RECORD_NAME_6']
if 'WS_RECORD_ID_7' in os.environ:
	record_ids[os.environ['WS_RECORD_ID_7']] = os.environ['WS_RECORD_NAME_7']
if 'WS_RECORD_ID_8' in os.environ:
	record_ids[os.environ['WS_RECORD_ID_8']] = os.environ['WS_RECORD_NAME_8']
if 'WS_RECORD_ID_9' in os.environ:
	record_ids[os.environ['WS_RECORD_ID_9']] = os.environ['WS_RECORD_NAME_9']

# get your plain public IP - specify service URL
get_plain_IP = 'https://api.ipify.org'

if 'GMAIL_RECEIVER' in os.environ:
	# mail sending info - from gmail; if you want it
	to = os.environ['GMAIL_RECEIVER'] # Email to send to.
	gmail_user = os.environ['GMAIL_USER'] # Email to send from. (MUST BE GMAIL)
	gmail_password = os.environ['GMAIL_APP_PASSWORD'] # Gmail password.