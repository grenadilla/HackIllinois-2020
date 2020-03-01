import requests
import json
from datetime import datetime
from collections import OrderedDict
from config import Config

customerId = Config.API_CUSTOMER_ID
apiKey = Config.API_KEY

def purchase_data():
    customerIdUrl = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerId, apiKey)
    customer_response = requests.get(customerIdUrl, headers={'content-type':'application/json'})
    accounts = json.loads(customer_response.text)

    months = generate_months()

    nicknames = []
    account_ids = []
    for account in accounts:
        nicknames.append(account['nickname'])
        account_ids.append(account['_id'])

    return_string = ""
    loan_amount_payments = [0] * len(account_ids)
    for i in range(len(account_ids)):
        purchase_amounts = ([0] * 12)
        purchaseUrl = 'http://api.reimaginebanking.com/accounts/{}/purchases?key={}'.format(account_ids[i],apiKey)
        loanUrl = 'http://api.reimaginebanking.com/accounts/{}/loans?key={}'.format(account_ids[i], apiKey)
        purchase_response = requests.get(purchaseUrl, headers={'content-type':'application/json'})

        loan_response = requests.get(loanUrl, headers={'content-type':'application/json'})
        loans = json.loads(loan_response.text)
        purchases = json.loads(purchase_response.text)

        for purchase in purchases:
            purchase_date = datetime.strptime(purchase['purchase_date'][:10], '%Y-%m-%d')
            for j in range(12):
                if (purchase_date >= months[j]):
                    purchase_amounts[j] += purchase['amount']
                    break

        for loan in loans:
            loan_amount_payments[i] += loan['monthly_payment']
        return_string += nicknames[i] + ": "+ str(purchase_amounts) + " : " + str(loan_amount_payments[i]) + "\n"

    if (purchase_response.status_code == 200):
            return return_string


    '''for i in range(len(purchase_amounts)):
        return_string += nicknames[i] + ": $" + str(purchase_amounts[i])
    if response.status_code == 200:
    	return return_string'''

def generate_months():
    #days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    list = []
    date = datetime.today()
    date = date.replace(day = 15)
    for i in range(12):
        list.append(date)
        if (date.month - 1 == 0):
            date = date.replace(year = date.year - 1, month = 12, day = 15)
        else:
            date = date.replace(month = date.month - 1, day = 15)
    return list
