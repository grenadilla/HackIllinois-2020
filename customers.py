# Learn more or give us feedback
import requests
import json
import random
import string

def get_customers():
    url = "http://api.reimaginebanking.com/customers?key=5e069ae4f90746158075478b37e7d4b6"
    response = requests.get(url, headers={'content-type':'application/json'})
    if response.status_code == 201:
	    print('account created')

    customers = json.loads(response.text)
    for customer in customers:
        print(customer['first_name'])

def randomString(stringLength):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def generate_json():

    first_name = randomString(10)
    last_name = randomString(3)
    fake_customer = {
      "first_name": first_name,
      "last_name": last_name,
      "address": {
        "street_number": "",
        "street_name": "",
        "city": "",
        "state": "",
        "zip": ""
      }
    }
    return fake_customer

print(generate_json())
