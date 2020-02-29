import requests
import json

api_key = "5e069ae4f90746158075478b37e7d4b6"

def get_customers():
    url = "http://api.reimaginebanking.com/customers?key={}".format(api_key)
    response = requests.get(url, headers={'content-type':'application/json'})
    if response.status_code == 201:
	    print('account created')
    
    customers = json.loads(response.text)
    for customer in customers:
        print(customer['_id'])