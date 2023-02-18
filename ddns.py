# websupport.sk DNS remote conf script

import hmac
import hashlib
import time
import requests
import base64
from datetime import date, datetime, timezone
import smtplib
from email.mime.text import MIMEText
from urllib.request import urlopen
import socket
import json
from collections import OrderedDict
import ast
import syslog
from dns import resolver
from ddns_conf import *

# prepare and make request for desired record_id
def update_request(record_id, name, new_ip, ttl):
    # Websupport REST API section
    method = 'PUT'
    path = f'/v1/user/{user_id}/zone/{domain}/record/{record_id}'
    
    # Prepare json object for sending    
    data = json.dumps(OrderedDict([("name", name), ("content", new_ip), ("ttl", ttl)]), separators=(',', ':'),)
    data = ast.literal_eval(data)

    # Compute signature
    timestamp = int(time.time())
    canonicalRequest = '%s %s %s' % (method, path, timestamp)
    signature = hmac.new(
        bytes(secret, 'UTF-8'), 
        bytes(canonicalRequest, 'UTF-8'), 
        hashlib.sha1
    ).hexdigest()

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Date': datetime.fromtimestamp(timestamp, timezone.utc).isoformat()
    }    

    # WS REST API change IP
    print("Sending update request...")
    print("Headers:", headers)
    print("Data:", data)
    result = requests.put(
        f'{api}{path}', 
        auth=(apiKey, signature),
        headers=headers, 
        json=data
    ).content.decode('utf-8')    
    print("Request result:", result)
    return result

def send_mail(public_ip, body_msg):
    if 'gmail_user' not in locals() or 'gmail_user' not in globals():
        print("Email not configured.")
        return

    # Setup mailserver.
    # Note that we actually want to create a new server every time,
    # because the original server will eventually disconnect.
    # Overall, we should not be sending enough mails to turn this into a
    # resource problem.
    smtpserver = smtplib.SMTP('smtp.gmail.com', 587) # Server to use.
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    smtpserver.login(gmail_user, gmail_password)

    # Mailing info
    # Account Information
    today = date.today()  # Get current time/date
    now = datetime.now() # Get current time

    # Creates the text, subject, 'from', and 'to' of the message.
    #msg = MIMEText('actual public IP: %s' %  public_ip)
    msg = MIMEText(body_msg)
    msg['Subject'] = 'IP Info: change of dynamic IP on %s %s' %(now.strftime('%H:%M'), today.strftime('%d-%b-%Y'))
    msg['From'] = gmail_user
    msg['To'] = to
    # Send the message
    smtpserver.sendmail(gmail_user, [to], msg.as_string())
    # Closes the smtp server.
    smtpserver.quit()

errors = 0
while True:    
    try:        
        # Fetch the current publicly visible IP.
        print("Check for current IP...")
        my_ip = urlopen(get_plain_IP).read().decode("utf-8")
        print("Current IP:", my_ip)

        print("Check for last known IP...")
        # Here, we have to use a fixed DNS server outside
        # of our own network, because on our network, we
        # have a local DNS server that will make it seem
        # like the address of our server is local.
        res = resolver.Resolver()
        res.nameservers = ['8.8.8.8']
        answers = res.resolve(check_domain)
        answers = [str(x) for x in answers]
        last_ip = answers[0]
        print("Last known IP:", last_ip)

        # If the two IPs are different, we try to update
        # all user specified records.
        result = ''
        if my_ip != last_ip:
            for i in record_ids:
                result += update_request(i, record_ids[i], my_ip, global_ttl) + "\n"
            send_mail(my_ip, result)
            syslog.syslog(syslog.LOG_INFO, result)    
        else:
            print("No change necessary.")    
        errors  = 0
    except Exception as e:        
        # Sometimes, the get IP service or WS API just fails,
        # in which case we want to keep trying, but get a notification
        # if the problems persist over a longer period of time.
        errors += 1
        print(f"Error during IP update: `{e}`.")
        if errors >= 10:
            errors = 0
            send_mail("NaN", "Repeated errors encountered during DDNS updates.")

    print("Sleeping for one hour...")
    time.sleep(3600)