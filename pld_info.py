import requests
import json
from datetime import datetime
from config import Config
from app.models import Account

def purchase_data(customer):
    accounts = Account.query.filter(Account.user == customer).all()
    payload = {'key': Config.API_KEY}

    months = generate_months()
    account_purchases = {}
    for account in accounts:
        purchase_amounts = ([0] * 12)
        purchaseUrl = '{}accounts/{}/purchases'.format(Config.API_URL, account.account_id)
        purchase_response = requests.get(purchaseUrl, headers={'content-type':'application/json'}, params=payload)

        if (purchase_response.status_code == 200):
            purchases = json.loads(purchase_response.text)

            for purchase in purchases:
                purchase_date = datetime.strptime(purchase['purchase_date'][:10], '%Y-%m-%d')
                for i in range(12):
                    if (purchase_date >= months[i]):
                        purchase_amounts[i] += purchase['amount']
                        break

            account_purchases[account.account_id] = purchase_amounts

    return account_purchases

def deposit_data(customer):
    accounts = Account.query.filter(Account.user == customer).all()
    payload = {'key': Config.API_KEY}

    months = generate_months()
    account_deposits = {}
    for account in accounts:
        deposit_amounts = ([0] * 12)
        depositUrl = '{}accounts/{}/deposits'.format(Config.API_URL, account.account_id)
        deposit_response = requests.get(depositUrl, headers={'content-type':'application/json'}, params=payload)

        if (deposit_response.status_code == 200):
            deposits = json.loads(deposit_response.text)

            for deposit in deposits:
                deposit_date = datetime.strptime(deposit['transaction_date'][:10], '%Y-%m-%d')
                for i in range(12):
                    if (deposit_date >= months[i]):
                        deposit_amounts[i] += deposit['amount']
                        break

            account_deposits[account.account_id] = deposit_amounts

    return account_deposits

def loan_data(customer):
    accounts = Account.query.filter(Account.user == customer).all()
    payload = {'key': Config.API_KEY}
    account_loans = {}

    for account in accounts:
        loanUrl = '{}accounts/{}/loans'.format(Config.API_URL, account.account_id)
        loan_response = requests.get(loanUrl, headers={'content-type':'application/json'}, params=payload)

        if (loan_response.status_code == 200):
            loans = json.loads(loan_response.text)
            loan_data = []
            for loan in loans:
                # monthly payment, amount
                loan_data.append((loan['monthly_payment'], loan['amount']))

            account_loans[account.account_id] = loan_data

    return account_loans

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