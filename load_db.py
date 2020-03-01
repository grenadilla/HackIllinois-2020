from app import db, models
import requests
import json
from app.models import User, Account, AccountType
from config import Config

def create_account_types():
    if AccountType.query.filter(AccountType.name == "Credit Card").first() is None:
        a_type = AccountType(name="Credit Card")
        db.session.add(a_type)
    if AccountType.query.filter(AccountType.name == "Savings").first() is None:
        a_type = AccountType(name="Savings")
        db.session.add(a_type)
    if AccountType.query.filter(AccountType.name == "Checking").first() is None:
        a_type = AccountType(name="Checking")
        db.session.add(a_type)

def create_users():
    payload = {'key': Config.API_KEY}
    response = requests.get(('{}customers').format(Config.API_URL), 
        params=payload, headers={'content-type':'application/json'})

    if response.status_code == 200 or response.status_code == 201:
        customers = json.loads(response.text)
        for customer in customers:
            if User.query.filter(User.customer_id == customer["_id"]).first() is None:
                # user names are format firstname.lastname, with number appended to end if duplicate
                username = customer["first_name"].lower() + '.' + customer["last_name"].lower()
                user = User(username=username, customer_id=customer["_id"])
                db.session.add(user)
        db.session.commit()

def create_accounts():
    payload = {'key': Config.API_KEY}

    for user in User.query.all():
        response = requests.get(('{}customers/{}/accounts').format(Config.API_URL, user.customer_id), 
            params=payload, headers={'content-type':'application/json'})

        if response.status_code == 200 or response.status_code == 201:
            accounts = json.loads(response.text)
            for account in accounts:
                if Account.query.filter(Account.account_id == account["_id"]).first() is None:
                    a_type = AccountType.query.filter(AccountType.name == account["type"]).first()
                    if "account_number" in account:
                        a_num = account["account_number"]
                    else:
                        a_num = ""
                    new_account = Account(account_id=account["_id"], nickname=account["nickname"], 
                        rewards=account["rewards"], balance=account["balance"], account_number=a_num, user=user,
                        account_type=a_type)
                    db.session.add(new_account)
            db.session.commit()

if __name__ == '__main__':
    create_account_types()
    create_users()
    create_accounts()
