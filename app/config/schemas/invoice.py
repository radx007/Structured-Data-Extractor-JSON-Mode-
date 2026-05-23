INVOICE_SCHEMA = {
        "extracted_data": {
            "invoice_number": "string",
            "invoice_date": "date",
            "sc_number": "string",
            "consignee": {
                "name": "string",
                "passport": "string"
            },
            "transport": {
                "arrival_location": "string",
                "country_of_departure": "string",
                "country_of_arrival": "string"
            },

            "origin": {
                "country_of_origin": "string",
                "hs_code": "string"
            },
            "items": [
                {
                    "marks": "string",
                    "description": "string",
                    "vin": "string",
                    "quantity": "number",
                    "unit_price": "number",
                    "line_total": "number"
                }
            ],
            "charges": {
                "freight_cost": "number"
            },
            "totals": {
                "total_quantity": "number",
                "total_amount": "number",
                "currency": "string",
                "amount_in_words": "string"
            }
        }
    }