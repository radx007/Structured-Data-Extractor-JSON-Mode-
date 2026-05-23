PACKING_LIST_SCHEMA = {
        "extracted_data": {
            "consignee": "string",
            "passport": "string",
            "sc_number": "string",
            "invoice_number": "string",
            "packing_list_number": "string",
            "date": "date",
            "departure_location": "string",
            "arrival_location": "string",
            "items": [
                {
                    "marks": "string",
                    "description": "string",
                    "vin": "string",
                    "quantity": "number",
                    "net_weight_kg": "number",
                    "gross_weight_kg": "number",
                    "volume_m3": "number"
                }
            ],
            "totals": {
                "quantity": "number",
                "net_weight_kg": "number",
                "gross_weight_kg": "number",
                "volume_m3": "number"
            }
        }
    }