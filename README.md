# pysquared
Square eCommerce API wrapper for Python Web Applications.

## Customer Creation Method:
###Customer Data Object:
Pass a python dictionary, built from order form and/or database data, to complete a customer creation:

- Only one of the following fields are required for a customer:
    - given_name
    - family_name
    - company_name
    - email_address
    - phone_number

- Example of a complete Customer object (from Square Documentation):
{
  "given_name": "Amelia",
  "family_name": "Earhart",
  "email_address": "Amelia.Earhart@example.com",
  "address": {
    "address_line_1": "500 Electric Ave",
    "address_line_2": "Suite 600",
    "locality": "New York",
    "administrative_district_level_1": "NY",
    "postal_code": "10003",
    "country": "US"
  },
  "phone_number": "1-212-555-4240",
  "reference_id": "YOUR_REFERENCE_ID",
  "note": "a customer"
}

## Transaction Charge Method:
###Order Data Object:
Pass a python dictionary, built from order form and/or database data, to complete a transaction:

- Required Fields:
    - 

- Optional Fields:
    - Shipping Address:
        - "shipping_address": {
        "address_line_1": "",
        "locality": "San Francisco",
        "administrative_district_level_1": "CA",
        "postal_code": "94114",
        "country": "US"
        }
- Complete Example:
    - { "shipping_address": {
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
    "amount": {

    },