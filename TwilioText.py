# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure
account_sid = "ACa6f456c11f606140be77170d7d4222b2"
auth_token = "6540ee350ee8163e71b559f9316b7e31"
client = Client(account_sid, auth_token)

message = client.messages.create(
  body="Stop loooking at my phone all of the time",
  from_="+18138514198",
  to="+19176849256"
)

print(message.sid)