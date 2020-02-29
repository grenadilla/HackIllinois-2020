import requests
import json
import random
import names

api_key = "5e069ae4f90746158075478b37e7d4b6"
url = "http://api.reimaginebanking.com/customers?key={}".format(api_key)

def get_customers():
    response = requests.get(url, headers={'content-type':'application/json'})
    if response.status_code == 201:
	    print('account created')

    customers = json.loads(response.text)
    return customers

def generate_customer_json():
    customer = {
      "first_name": names.get_first_name(),
      "last_name": names.get_last_name(),
      "address": {
        "street_number": "500",
        "street_name": "Disney",
        "city": "Champaign",
        "state": "IL",
        "zip": "61801"
      }
    }
    return json.dumps(customer)

def post_customers(num_customers):
    for i in range(num_customers):
        response = requests.post(url, data=generate_customer_json(), headers={'content-type':'application/json'})
        if response.status_code == 201 or response.status_code == 201:
            print('account created')
