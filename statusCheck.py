from twilio.rest import Client

apiKeys = json.loads(open("secrets.json").read())
twilio = Client(apiKeys['SID'], apiKeys['AUTH'])

message = "Crypto Notifier running smoothly."
twilio.messages.create(to=apiKeys['toNumber'], from_=apiKeys['fromNumber'], body=message)


