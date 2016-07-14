import unirest
import uuid
import os.environ

# ~~~ TRANSACTION METHODS ~~~
def transaction_lookup(location_id=None, transaction_id=None):
    url = "https://connect.squareup.com/v2/locations/%s/transactions/%s" % (location_id, transaction_id)
    return execute("GET", url)

def transaction_charge(location_id, order_data, card_nonce=None, customer_id=None, delay=False, chargeback_protection=False):
    url = "https://connect.squareup.com/v2/locations/%s/transactions" % location_id
    body_data = {
        "idempotency_key": str(uuid.uuid4().int),
        "shipping_address": order_data["shipping_address"],
        "billing_address": order_data["billing_address"],
        "amount_money": order_data["amount"],
        "buyer_email_address": order_data["email"],
        "delay_capture": delay
    }
    if card_nonce and customer_id:
        print "Exception: Cannot "
        sys.exit(1)
    elif card_nonce:
        data["card_nonce"] = card_nonce
    elif customer_id:
        customer = customer_lookup(customer_id)
        card = card_lookup(customer_id)
        data["customer_id"] = customer_id
        data["customer_card_id"] = card["id"]
        data["shipping_address"] = customer["address"]
        data["billing_address"] = card["billing_address"]
    if chargeback_protection: 
        if data.buyer_email_address == "":
            return False
        if (data.shipping_address or data.billing_address):
            pass
        else: 
            return False
    return execute("POST", url, body_data)

def transaction_void(location_id=None, transaction_id=None):
    url = "https://connect.squareup.com/v2/locations/%s/transactions/%s/void" % (location_id, transaction_id)
    transaction = transaction_lookup(location_id, transaction_id)
    for tender in transaction.tenders:
        body_data = {
            "idempotency_key": str(uuid.uuid4().int),
            "tender_id": tender["id"],
            "reason": "Refund via API",
            "amount_money": {
                "amount": tender["amount_money"]["amount"],
                "currency": tender["amount_money"]["currency"]
            }
        }
    return execute("POST", url, body_data)

def transaction_refund(location_id=None, transaction_id=None):
    url = "https://connect.squareup.com/v2/locations/%s/transactions/%s/refund" % (location_id, transaction_id)
    return execute("POST", url, body_data)


# ~~~ CUSTOMER METHODS ~~~
def customer_lookup(customer_id):
    url = "https://connect.squareup.com/v2/customers/%s" % customer_id
    return execute("POST", url, body_data)

def customer_create(customer_data):
    url = "https://connect.squareup.com/v2/customers/"
    body_data = {
      "given_name": customer_data.name_first,
      "family_name": customer_data.name_last,
      "email_address": customer_data.email,
      "address": {
        "address_line_1": customer_data.address1,
        "address_line_2": customer_data.address2,
        "locality": customer_data.city,
        "administrative_district_level_1": customer_data.state,
        "postal_code": customer_data.zipcode,
        "country": customer_data.country
      },
      "phone_number": customer_data.phone,
      "reference_id": "YOUR_REFERENCE_ID",
      "note": ""
    }
    return execute("POST", url, body_data)

def customer_update(customer_id, customer_data={}):
    url = "https://connect.squareup.com/v2/customers/%s" % customer_id
    return execute("PUT", url, body_data)

def customer_delete(customer_id):
    url = "https://connect.squareup.com/v2/customers/%s" % customer_id
    return execute("DELETE", url)


# ~~~ CREDIT-CARD METHODS ~~~
def card_lookup(customer_id):
    url = "https://connect.squareup.com/v2/customers/%s/cards" % customer_id
    return execute("GET", url)
 
def card_create(customer_id, card_nonce):
    url = "https://connect.squareup.com/v2/customers/%s/cards" % customer_id
    customer = customer_lookup(customer_id)
    body_data = {
      "card_nonce": card_nonce,
      "billing_address": customer["address"],
      "cardholder_name": customer["given_name"] + " " + customer["family_name"]
    }
    return execute("POST", url, body_data) 

def card_delete(customer_id, card_id):
    url = "https://connect.squareup.com/v2/customers/%s/cards/%s" % (customer_id, card_id)
    return execute("DELETE", url)


# ~~~ REST API HANDLING METHODS ~~~
def execute(mthd, url, body_data):
    try:
        access_token = os.environ['SQUARE_ACCESS_TOKEN']
    except KeyError:
        print "Please set the server environment variable SQUARE_ACCESS_TOKEN to that of your Square account."
        sys.exit(1)
    if mthd == "GET":
        response = unirest.get(url, headers={ "Authorization": "Bearer "+access_token, "Accept": "application/json" })
    elif mthd == "POST":
        response = unirest.post(url, headers={ "Authorization": "Bearer "+access_token, "Accept": "application/json", "Content-Type": "application/json" }, params=body_data)
    elif mthd == "PUT":
        response = unirest.put(url, headers={ "Authorization": "Bearer "+access_token, "Accept": "application/json", "Content-Type": "application/json" }, params=body_data)
    elif mthd == "DELETE":
        response = unirest.delete(url, headers={ "Authorization": "Bearer "+access_token, "Accept": "application/json" })
    return response.body
