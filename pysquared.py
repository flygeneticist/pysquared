import unirest


# ~~~ TRANSACTION METHODS ~~~
def transaction_lookup(location_id=None, transaction_id=None):
    url = "https://connect.squareup.com/v2/locations/%s/transactions/%s" % (location_id, transaction_id)
    return True

def transaction_charge(location_id, card_nonce=None, customer_id=None, delay=False, chargeback_protection=False):
    url = "https://connect.squareup.com/v2/locations/%s/transactions" % location_id
    if card_nonce:
        # charge via nonce 
        return True
    else if customer_id:
        # charge via stored customer / card data
        customer = customer_lookup(customer_id)
        return True
    return False

def transaction_void(location_id=None, transaction_id=None):
    url = "https://connect.squareup.com/v2/locations/%s/transactions/%s/void" % (location_id, transaction_id)
    transaction = transaction_lookup(location_id, transaction_id)
    for tender in transaction.tenders:
        data = {
            "idempotency_key": "YOUR_IDEMPOTENCY_KEY",
            "tender_id": tender.id,
            "reason": "customer refund",
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
      "billing_address": {
        "address_line_1": customer.address_line_1,
        "address_line_2": customer.address_line_1,
        "locality": customer.city,
        "administrative_district_level_1": customer.administrative_district_level_1,
        "postal_code": customer.postal_code,
        "country": customer.country
      },
      "cardholder_name": customer.given_name + " " + customer.family_name
    }
    # return card ID from Square server
    return True 

def card_delete(customer_id, card_id):
    url = "https://connect.squareup.com/v2/customers/%s/cards/%s" % (customer_id, card_id)
    return True
