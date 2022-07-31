# Websupport.sk DDNS Docker

This is a simple Python script based on https://github.com/kalikadze/dDNS that periodically updates selected DNS records to the current IP address. Consequently, it can be used as a basis for a dynamic DNS service for a domain managed by Websupport.

### Configuration

The necessary configuration is provided using environment variables. The list of necessary variables is given in `env.list.template`:

```
# Obtained from the admin console of Websupport.sk
WS_API_KEY=XXX
WS_API_SECRET=XXX
WS_USER_ID=123

# The base domain name for which we'll be updating records.
WS_DOMAIN=XXX
# The domain name who's IP should be compared to the current IP
# to determine whether records should be updated.
# E.g. if we are only updating test.example.com, not example.com,
# we have to reflect this here.
WS_CHECK_DOMAIN=XXX

# List of records. Records can be only updated, not created 
# (create them manually first). Record IDs can be found for example
# in the record URL in the admin console.
WS_RECORD_ID_1=123
WS_RECORD_NAME_1=XXX

# You can specify up to 9 records that should be updated to the current IP.
WS_RECORD_ID_2=123
WS_RECORD_NAME_2=XXX

# Finally, you can enter email address that should receive notifications
# about IP changes. Receiver can be anyone, but sender must be a Gmail
# address. Also, don't use your account password, use the "App passwords"
# functionality: https://support.google.com/accounts/answer/185833?hl=en
# If you omit these three variables, no emails will be sent.
GMAIL_RECEIVER=XXX
GMAIL_USER=XXX@gmail.com
GMAIL_APP_PASSWORD=XXX
```

You can copy `env.list.template` into `env.list` and fill in your credentials. Afterwards, you can start the service using:

```
docker run -d --env-file env.list daemontus/websupport-ddns:latest
```

Alternatively, you can just run `python ddns.py` to try it outside of Docker.