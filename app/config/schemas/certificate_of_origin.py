CERTIFICATE_OF_ORIGIN_SCHEMA = {
        "extracted_data": {
            "certificate_number": "string",
            "verification": "string",
            "exporter": {
                "name": "string",
                "address": "string",
                "country": "string"
            },
            "consignee": {
                "name": "string",
                "passport": "string",
                "nin": "string",
                "email": "string",
                "phone": "string",
                "address": "string",
                "country": "string"
            },
            "transport": {
                "mode": "string",
                "port_of_departure": "string",
                "port_of_arrival": "string",
                "country_of_departure": "string",
                "country_of_arrival": "string"
            },
            "destination_country": "string",
            "goods": [
                {
                    "marks": "string",
                    "description": "string",
                    "vin": "string",
                    "model": "string",
                    "manufacturing_year": "number",
                    "manufacturer": "string",
                    "unit_weight_kg": "number",
                    "quantity": "number"
                }
            ],
            "classification": {
                "hs_code": "string"
            },
            "invoice": {
                "invoice_number": "string",
                "invoice_date": "date"
            }
        }
    }