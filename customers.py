import requests
import json

def get_customers():
    url = "http://api.reimaginebanking.com/customers?key={}"
    response = requests.get(url, headers={'content-type':'application/json'})
    if response.status_code == 201:
	    print('account created')
    
    customers = json.loads(response.text)
    for customer in customers:
        print(customer['first_name'])
    