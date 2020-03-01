import requests
import json
from datetime import datetime
from collections import OrderedDict
from config import Config
from app.models import Account

def purchase_data(customer):
    accounts = Account.query.filter(Account.user == customer).all()
    payload = {'key': Config.API_KEY}

    months = generate_months()

    account_purchases = {}
    account_loans = {}
    for i, account in enumerate(accounts):
        purchase_amounts = ([0] * 12)
        purchaseUrl = '{}accounts/{}/purchases'.format(Config.API_URL, account.account_id)
        loanUrl = '{}accounts/{}/loans'.format(Config.API_URL, account.account_id)
        purchase_response = requests.get(purchaseUrl, headers={'content-type':'application/json'}, params=payload)
        loan_response = requests.get(loanUrl, headers={'content-type':'application/json'}, params=payload)

        if (loan_response.status_code == 200 and purchase_response.status_code == 200):
            loans = json.loads(loan_response.text)
            purchases = json.loads(purchase_response.text)

            for purchase in purchases:
                purchase_date = datetime.strptime(purchase['purchase_date'][:10], '%Y-%m-%d')
                for j in range(12):
                    if (purchase_date >= months[j]):
                        purchase_amounts[j] += purchase['amount']
                        break

            loan_amount_payments = []
            for loan in loans:
                loan_amount_payments.append(loan['monthly_payment'])

            account_purchases[account.account_id] = purchase_amounts
            account_loans[account.account_id] = loan_amount_payments

    return (account_purchases, account_loans)
            

def generate_months():
    midmonth = []
    date = datetime.today()
    date = date.replace(day = 15)
    for i in range(12):
        midmonth.append(date)
        if (date.month - 1 == 0):
            date = date.replace(year = date.year - 1, month = 12, day = 15)
        else:
            date = date.replace(month = date.month - 1, day = 15)
    return midmonth