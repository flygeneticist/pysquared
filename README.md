# pysquared
Square eCommerce API wrapper for Python Web Applications.

## Transaction Charge Method:
###Order Data Object:
Pass a python dictionary, build from order form and/or database data to complete a transaction:
- Required Fields:
    -- 
- Optional Fields:
    -- Shipping Address:
        --- "shipping_address": {
        "address_line_1": "123 Main St",
        "locality": "San Francisco",
        "administrative_district_level_1": "CA",
        "postal_code": "94114",
        "country": "US"
        }
- Complete Example:
{
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
    "amount": {
        
    },