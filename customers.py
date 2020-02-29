# Learn more or give us feedback
import requests
import json
import random
import string

api_key = "5e069ae4f90746158075478b37e7d4b6"
url = "http://api.reimaginebanking.com/customers?key={}".format(api_key)

def get_customers():
    response = requests.get(url, headers={'content-type':'application/json'})
    if response.status_code == 201:
	    print('account created')

    customers = json.loads(response.text)
    for customer in customers:
        print(customer['first_name'])

def generate_customer_json():
    first_name = randomString(5)
    last_name = randomString(5)
    customer = {
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
    return json.dumps(customer)

def post_customers(num_customers):
    for i in range(num_customers):
        response = requests.post(
        	url,
        	data=generate_customer_json(),
        	headers={'content-type':'application/json'},
        	)

def randomString(stringLength):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
