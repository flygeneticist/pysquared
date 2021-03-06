import unirest
import uuid
import json

# ~~~ LOCATION METHODS ~~~
def location_lookup():
    url = "https://connect.squareup.com/v2/locations"
    return execute("GET", url)

# ~~~ TRANSACTION METHODS ~~~
def transaction_lookup(location_id, transaction_id):
    url = "https://connect.squareup.com/v2/locations/%s/transactions/%s" % (location_id, transaction_id)
    return execute("GET", url)

def transaction_charge(location_id, order_data, card_nonce=None, customer_id=None, card_id= False, delay=False):
    url = "https://connect.squareup.com/v2/locations/%s/transactions" % location_id
    body_data = {"idempotency_key": str(uuid.uuid4().int), "delay_capture": delay}
    for i in ["shipping_address", "billing_address", "buyer_email_address", "amount_money"]:
        try:
            body_data[i] = order_data[i]
        except:
            pass
    if card_nonce and customer_id:
        raise Exception("Cannot process a transaction using both options. Choose one or the other.")
    elif card_nonce:
        body_data["card_nonce"] = card_nonce
    elif customer_id and card_id:
        body_data["customer_id"] = customer_id
        body_data["customer_card_id"] = card_id
    else:
        raise Exception("Cannot process the transaction with the arguments given.")
    return execute("POST", url, json.dumps(body_data))

def transaction_void(location_id, transaction_id):
    url = "https://connect.squareup.com/v2/locations/%s/transactions/%s/void" % (location_id, transaction_id)
    return execute("POST", url)

def transaction_refund(location_id, transaction_id, reason=False):
    url = "https://connect.squareup.com/v2/locations/%s/transactions/%s/refund" % (location_id, transaction_id)
    response = []
    transaction = transaction_lookup(location_id, transaction_id)
    for tender in transaction.tenders:
        body_data = {
            "idempotency_key": str(uuid.uuid4().int),
            "tender_id": tender["id"],
            "reason": "Refund via API" if reason == False else str(reason),
            "amount_money": {
                "amount": tender["amount_money"]["amount"],
                "currency": tender["amount_money"]["currency"]
            }
        }
        response += execute("POST", url, json.dumps(body_data))
    return response


# ~~~ CUSTOMER METHODS ~~~
def customer_lookup(customer_id):
    url = "https://connect.squareup.com/v2/customers/%s" % customer_id
    return execute("GET", url)

def customer_create(customer_data):
    url = "https://connect.squareup.com/v2/customers"
    return execute("POST", url, json.dumps(customer_data))

def customer_update(customer_id, customer_data):
    url = "https://connect.squareup.com/v2/customers/%s" % customer_id
    return execute("PUT", url, json.dumps(customer_data))

def customer_delete(customer_id):
    url = "https://connect.squareup.com/v2/customers/%s" % customer_id
    return execute("DELETE", url)


# ~~~ CREDIT-CARD METHODS ~~~
def card_get_all(customer_id):
    url = "https://connect.squareup.com/v2/customers/%s/cards" % customer_id
    return execute("GET", url)

def card_get_one(customer_id, card_id):
    url = "https://connect.squareup.com/v2/customers/%s/cards/%s" % (customer_id, card_id)
    return execute("GET", url)
 
def card_create(customer_id, card_nonce, billing_address):
    url = "https://connect.squareup.com/v2/customers/%s/cards" % customer_id
    customer = customer_lookup(customer_id)
    body_data = {
      "card_nonce": card_nonce,
      "billing_address": billing_address,
      "cardholder_name": customer["customer"]["given_name"] + " " + customer["customer"]["family_name"]
    }
    return execute("POST", url, json.dumps(body_data)) 

def card_delete(customer_id, card_id):
    url = "https://connect.squareup.com/v2/customers/%s/cards/%s" % (customer_id, card_id)
    return execute("DELETE", url)


# ~~~ REST API HANDLING METHODS ~~~
def execute(mthd, url, body_data=None):
    try:
        access_token = 'sq0atb-_ifJWXh-Jj15F004mRfJ6Q' #os.environ['SQUARE_ACCESS_TOKEN']
    except KeyError:
        raise Exception("Set the server environment variable SQUARE_ACCESS_TOKEN to that of your Square account.")
    if mthd == "GET":
        response = unirest.get(url, headers={ "Authorization": "Bearer "+access_token, "Accept": "application/json" })
    elif mthd == "POST":
        response = unirest.post(url, headers={ "Authorization": "Bearer "+access_token, "Accept": "application/json", "Content-Type": "application/json" }, params=body_data)
    elif mthd == "PUT":
        response = unirest.put(url, headers={ "Authorization": "Bearer "+access_token, "Accept": "application/json", "Content-Type": "application/json" }, params=body_data)
    elif mthd == "DELETE":
        response = unirest.delete(url, headers={ "Authorization": "Bearer "+access_token, "Accept": "application/json" })
    return response.body


# TESTING CODE
# square_nonce = "CBASEPnKQZGzmUfKCPhvMP5dqI8"
# square_id = "CBASELXkqLo7TogdWUk_c0D3S3M"
# location_id = "CBASEJwUwLaHK7XERiFJstxcAMU"
# square_card_id = "32f81324-6c12-5603-518c-bfb89572be71"
# customer_data = { 
#     "given_name": "Kelvin", 
#     "family_name": "Keller", 
#     "email_address": "flygeneticist@gmail.com", 
#     "address": {
#         "address_line_1": "1234 Street", 
#         "address_line_2": "", 
#         "locality": "Austin", 
#         "administrative_district_level_1": "TX", 
#         "postal_code": "78741",
#         "country": "US" 
#     },  
#     "phone_number": "6099492314", 
#     "reference_id": "6352735", 
#     "note": "Website generated customer" 
# }
# if square_id == "":
#     square_id = customer_create(customer_data)["customer"]["id"]
# print square_id
# square_card_id = card_create(square_id, square_nonce, customer_data["address"])["card"]["id"]
# print square_card_id
# order_data = {
# "shipping_address": {
#     "address_line_1": "123 Main St",
#     "locality": "San Francisco",
#     "administrative_district_level_1": "CA",
#     "postal_code": "94114",
#     "country": "US"
# },
#     "billing_address": {
#         "address_line_1": "1234 Street", 
#         "address_line_2": "", 
#         "locality": "Austin", 
#         "administrative_district_level_1": "TX", 
#         "postal_code": "78741",
#         "country": "US" 
#     },
#     "amount_money": {
#         "amount": 4200,
#         "currency": "USD"
#     }
# }
# square_transaction_id = transaction_charge(location_id, order_data, card_nonce=None, customer_id=square_id, card_id=square_card_id, delay=False)["transaction"]["id"]
# print square_transaction_id
