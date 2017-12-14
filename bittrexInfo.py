from bittrex import Bittrex
from pymarketcap import *
from twilio.rest import Client
import simplejson as json

apiKeys = json.loads(open("secrets.json").read())
myBittrex = Bittrex(apiKeys['key'], apiKeys['secret'])

cmc = Pymarketcap()

twilio = Client(apiKeys['SID'], apiKeys['AUTH'])

data = json.loads(json.dumps(myBittrex.get_balances()))

deposited = 1297.20

if data["success"]: 
    total = 0
    balances = {}
    changes = {}
    for curr in data['result']:
        balance  = curr['Balance']
        currency = curr['Currency']
        if balance > 0:
            balances[currency] = balance

    for curr, balance in balances.items(): # get balances
        print(curr, balance)
        cmcData = json.loads(json.dumps(cmc.ticker(curr)))
        usd = cmcData['price_usd']
        total += usd*balance

        # check what has changed more than 10% in 24 hrs
        if abs(cmcData['percent_change_24h']) > 10 and balance > .00001:
            changes[curr] = cmcData['percent_change_24h']

    returns = (-deposited)+total
    percentReturns = returns/deposited*100

    if abs(percentReturns - apiKeys['prev']) > 5:
        message = "There has been a greater than 5% change in your crypto profit. \nYour new balance is: ${0:.2f}, with a percent change of: {1:.2f}%. \nCurrencies with a 24 hour change greater than 10%:\n".format(total, percentReturns)
        for curr, change in changes.items():
            message += curr + ": {0:.2f}%".format(change) + ".\n"
        print(message)
        apiKeys['prev'] = percentReturns
        with open('secrets.json', 'w') as outfile: # write to json file
            json.dump(apiKeys, outfile)
        twilio.messages.create(to=apiKeys['toNumber'], from_=apiKeys['fromNumber'], body=message)
    else:
        print("Less than 5% change")

    print("Bittrex total: ${0:.2f}".format(total))
    print("Current return: ${0:.2f}".format(returns))
    print("Percent return: {0:.2f}%".format(percentReturns))



