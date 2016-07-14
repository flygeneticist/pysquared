import unirest
import uuid


# ~~~ TRANSACTION METHODS ~~~
def transaction_lookup(location_id=None, transaction_id=None):
    url = "https://connect.squareup.com/v2/locations/%s/transactions/%s" % (location_id, transaction_id)
    return True

def transaction_charge(location_id, order_data, card_nonce=None, customer_id=None, delay=False, chargeback_protection=False):
    url = "https://connect.squareup.com/v2/locations/%s/transactions" % location_id
    data = {
        "idempotency_key": str(uuid.uuid4().int),
        "shipping_address": {
            "address_line_1": "123 Main St",
            "locality": "San Francisco",
            "administrative_district_level_1": "CA",
            "postal_code": "94114",
            "country": "US"
        },
        "billing_address": {
            "address_line_1": "500 Electric Ave",
            "address_line_2": "Suite 600",
            "administrative_district_level_1": "NY",
            "locality": "New York",
            "postal_code": "10003",
            "country": "US"
        },
        "amount_money": {
            "amount": 5000,
            "currency": "USD"
        },
        "buyer_email_address": "",
        "reference_id": "some optional reference id",
        "note": "some optional note",
        "delay_capture": delay
    }
    if card_nonce:
        # charge via nonce 
        data["card_nonce"] = card_nonce
    else if customer_id:
        # charge via stored customer & card data
        customer = customer_lookup(customer_id)
        card = card_lookup(customer_id)
        data["customer_id"] = customer_id
        data["customer_card_id"] = card.id
        data["shipping_address"] = customer.address
        data["billing_address"] = card.billing_address
    if chargeback_protection: 
        if data.buyer_email_address == "":
            return False
        if (data.shipping_address or data.billing_address):
            return True
        else: 
            return False
    return False

def transaction_void(location_id=None, transaction_id=None):
    url = "https://connect.squareup.com/v2/locations/%s/transactions/%s/void" % (location_id, transaction_id)
    transaction = transaction_lookup(location_id, transaction_id)
    for tender in transaction.tenders:
        data = {
            "idempotency_key": str(uuid.uuid4().int),
            "tender_id": tender.id,
            "reason": "Refund via API",
            "amount_money": {
                "amount": tender.amount_money.amount,
                "currency": tender.amount_money.currency
            }
        }
    return True

def transaction_refund(location_id=None, transaction_id=None):
    url = "https://connect.squareup.com/v2/locations/%s/transactions/%s/refund" % (location_id, transaction_id)
    return True


# ~~~ CUSTOMER METHODS ~~~
def customer_lookup(customer_id):
    url = "https://connect.squareup.com/v2/customers/%s" % customer_id
    return True

def customer_create(customer_data={}):
    data = {
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
    return True

def customer_update(customer_id, customer_data={}):
    url = "https://connect.squareup.com/v2/customers/%s" % customer_id
    return True

def customer_delete(customer_id):
    url = "https://connect.squareup.com/v2/customers/%s" % customer_id
    return True


# ~~~ CREDIT-CARD METHODS ~~~
def card_lookup(customer_id):
    url = "https://connect.squareup.com/v2/customers/%s/cards" % customer_id
    return True

def card_create(customer_id, card_nonce):
    url = "https://connect.squareup.com/v2/customers/%s/cards" % customer_id
    customer = customer_lookup(customer_id)
    data = {
      "card_nonce": card_nonce,
      "billing_address": customer.address,
      "cardholder_name": customer.given_name + " " + customer.family_name
    }
    # return card ID from Square server
    return True 

def card_delete(customer_id, card_id):
    url = "https://connect.squareup.com/v2/customers/%s/cards/%s" % (customer_id, card_id)
    return True
