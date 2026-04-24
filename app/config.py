class Settings:

    APP_NAME = "Vehicle Document AI"

    OCR_LANG = "en"

    MAX_UPLOAD_FILES = 4
    
    MAX_SIZE = 5 * 1024 * 1024  # 5MB

    _packing_list = {
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
                    
    _certificate_of_origin = {
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
    _invoice = {
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
    _technical_details ={
        "extracted_data": {
            "certificate_number": "string",
            "issue_date": "string",
            "manufacturer": "string",
            "brand": "string",
            "vehicle_name": "string",
            "model": "string",
            "chassis_number": "string",
            "engine_model": "string",
            "engine_number": "string",
            "fuel_type": "string",
            "displacement_ml": "number",
            "power_kw": "number",
            "emission_standard": "string",
            "fuel_consumption": "number",
            "dimensions_mm": {
            "length": "number",
            "width": "number",
            "height": "number"
            },
            "number_of_tires": "number",
            "tire_specifications": "string",
            "wheelbase_mm": "number",
            "axle_load_kg": "string",
            "number_of_axles": "number",
            "steering_type": "string",
            "gross_weight_kg": "number",
            "curb_weight_kg": "number",
            "rated_payload_kg": "number",
            "max_towing_capacity_kg": "number",
            "passenger_capacity": "number",
            "max_speed_kmh": "number",
            "manufacturing_date": "string",
            "abs_model": "string",
            "abs_manufacturer": "string",
            "edr_system": "boolean",
            "remarks": "string",
            "manufacturer_address": "string"
        }
    }

    schemas = {
        "packing_list": _packing_list,
        "certificate_of_origin": _certificate_of_origin,
        "invoice": _invoice,
        "technical_details": _technical_details
    }

    instructions = {
        "packing_list": (
            "TASK: Extract structured data from a packing list document.\n\n"

            "STRICT OUTPUT RULES:\n"
            "- Return ONLY valid JSON.\n"
            "- Do NOT add explanations.\n"
            "- Do NOT leave fields null if the value can be derived from the text.\n\n"

            "1. CONSIGNEE:\n"
            "- Extract 'consignee' name.\n"
            "- Extract 'passport' (or NIN).\n"
            "- Keep ONLY digits for passport.\n\n"

            "2. TRANSPORT:\n"
            "- 'departure_location' = origin port.\n"
            "- 'arrival_location' = destination port.\n\n"

            "3. DATE:\n"
            "- Convert to format YYYY-MM-DD.\n\n"

            "4. ITEMS ARRAY (VERY IMPORTANT):\n"
            "- Extract ALL rows.\n"
            "- 'vin' MUST be exactly 17 characters.\n"
            "- 'description' = vehicle model only (remove marketing words like 'Youth Fashion Edition').\n"
            "- 'marks' = 'N/M' if present, else null.\n"
            "- 'quantity' = integer.\n"
            "- 'net_weight_kg', 'gross_weight_kg', 'volume_m3' = numeric.\n\n"

            "5. TOTALS (CRITICAL LOGIC):\n"
            "- ALWAYS fill totals.\n"
            "- FIRST: try to extract totals from the document footer.\n"
            "- IF totals are missing OR null:\n"
            "  → compute totals by summing ALL items:\n"
            "     total_quantity = sum(quantity)\n"
            "     total_net_weight = sum(net_weight_kg)\n"
            "     total_gross_weight = sum(gross_weight_kg)\n"
            "     total_volume = sum(volume_m3)\n"
            "- NEVER leave totals null if items exist.\n\n"

            "6. SANITIZATION:\n"
            "- Remove units (KG, M3).\n"
            "- Keep only numbers.\n\n"

            "7. FINAL RULE:\n"
            "- Do NOT hallucinate new data.\n"
            "- BUT computed totals from items are VALID and REQUIRED.\n"
        ),
        "certificate_of_origin": (
            "PRIMARY TASK: Extract structured data from the certificate of origin. "

            "1. CERTIFICATE: "
            "   - Extract 'certificate_number'. "
            "   - Extract 'verification' (URL or authority). "

            "2. EXPORTER: "
            "   - Extract 'name', 'address', and 'country'. "
            "   - Clean obvious OCR errors in names (e.g., remove extra leading characters like 'ZSAIC' → 'SAIC'). "

            "3. CONSIGNEE: "
            "   From the identity block extract: "
            "   - 'name' "
            "   - 'passport' (digits only) "
            "   - 'nin' (exactly 18 digits) "
            "   - 'email' "
            "   - 'phone' "
            "   - 'address' "
            "   - 'country' "

            "4. TRANSPORT: "
            "   - 'port_of_departure' = text after 'FROM' "
            "   - 'port_of_arrival' = text after 'TO' "
            "   - 'mode' = SEA / AIR / ROAD (normalize to uppercase) "
            "   - Extract 'country_of_departure' and 'country_of_arrival' from ports if present "

            "5. GOODS ARRAY: "
            "   For each item: "
            "   - 'vin' MUST be exactly 17 characters. "
            "   - 'model' = alphanumeric vehicle model code. "
            "   - 'manufacturing_year' = numeric value. "
            "   - 'description' MUST be the FULL commercial name (e.g., 'MG5 180DVVT MANUAL YOUTH FASHION EDITION'). "
            "   - Do NOT truncate description to brand only. "
            "   - 'manufacturer' = company name (clean OCR noise if needed). "
            "   - 'unit_weight_kg' = numeric value only. "
            "   - 'quantity' = integer. "
            "   - 'marks' = 'N/M' if present. "

            "6. CLASSIFICATION: "
            "   - Extract 'hs_code'. "

            "7. INVOICE: "
            "   - Extract 'invoice_number'. "
            "   - Extract 'invoice_date' and normalize to 'YYYY-MM-DD'. "

            "8. DESTINATION: "
            "   - Extract 'destination_country'. "

            "9. SANITIZATION: "
            "   - Remove units like KG. "
            "   - Keep only numeric values where required. "

            "10. FINAL RULES: "
            "   - Do NOT hallucinate values. "
            "   - If a value exists → NEVER return null. "
            "   - If missing → return null (NOT empty string). "
        ),
        "commercial_invoice": (
            "Extract structured data from the document into the schema. Do not guess or invent missing values. "

            "HEADER:"
            "- Extract invoice_number, sc_number, invoice_date (normalize to YYYY-MM-DD). "

            "PARTIES:"
            "- Extract consignee name and passport (digits only). "

            "TRANSPORT:"
            "- Extract departure and arrival locations. "
            "- Extract country_of_departure and country_of_arrival (country names only). "

            "ORIGIN:"
            "- Extract country_of_origin and hs_code exactly as written. "

            "ITEMS (GENERAL RULE):"
            "- Identify each product line as a structured record. "
            "- Each item may contain: product identity, reference codes, quantity, price, and totals. "

            "FIELD EXTRACTION RULE:"
            "- marks = label or prefix information if present (e.g., N/M). "
            "- description = main product name BEFORE any technical identifier or code. "
            "  * Must represent the human-readable product name. "
            "  * Must NOT include serial numbers, VINs, or reference codes. "
            "- vin = any unique structured identifier if present (e.g., VIN, serial number). "
            "- quantity = integer value. "
            "- unit_price = numeric value. "
            "- line_total = numeric value. "

            "ITEM SEPARATION RULE:"
            "- If multiple fields are packed into one string, separate by role not position. "
            "- Identify product name first, then identifiers, then numeric values. "

            "CHARGES:"
            "- Extract any transport or freight-related costs if present. "

            "TOTALS:"
            "- total_quantity = sum of item quantities. "
            "- total_amount = sum of item totals + charges if applicable. "
            "- currency = detect from document. "
            "- amount_in_words = clean text only (remove filler words like SAY/ONLY). "

            "GENERAL RULES:"
            "- Never hallucinate missing fields. "
            "- Never return empty strings → use null only. "
            "- Do not merge unrelated fields. "
        ),
        "technical_details": (
            "TASK: Extract vehicle technical data into structured JSON.\n\n"

            "OUTPUT RULES:\n"
            "- Return ONLY valid JSON.\n"
            "- All fields must exist.\n"
            "- If missing → null.\n\n"

            "CRITICAL EXTRACTION RULES:\n"
            "- Copy values EXACTLY from text.\n"
            "- Do NOT correct spelling.\n"
            "- Do NOT infer or calculate.\n"
            "- Remove units (kg, km/h, mm, kW) from numbers.\n"
            "- Keep dates exactly as written.\n\n"

            "IDENTITY LOCKING (VERY IMPORTANT):\n"
            "- chassis_number MUST be exactly 17 characters.\n"
            "- engine_number MUST be copied exactly.\n"
            "- certificate_number MUST be copied exactly (no missing digits).\n\n"

            "FIELD MAPPING:\n"
            "- certificate_number → Certificate Number.\n"
            "- issue_date → Issuance Date.\n"
            "- manufacturer → Vehicle Manufacturer Name.\n\n"

            "BRAND / VEHICLE NAME RULE:\n"
            "- If format is 'Brand/Vehicle Name':\n"
            "  → brand = text BEFORE '/'\n"
            "  → vehicle_name = text AFTER '/'\n"
            "- If no '/', then:\n"
            "  → brand = first word\n"
            "  → vehicle_name = full remaining text\n\n"

            "- model → Vehicle Model.\n"
            "- chassis_number → Vehicle Identification Number.\n"
            "- engine_model → Engine Model.\n"
            "- engine_number → Engine Number.\n"
            "- fuel_type → Fuel Type.\n"
            "- displacement_ml → Displacement value.\n"
            "- power_kw → Power value.\n"
            "- emission_standard → Emission Standard.\n"
            "- fuel_consumption → Fuel Consumption.\n\n"

            "DIMENSIONS RULE:\n"
            "- Extract exactly 3 numbers from 'Overall Dimensions':\n"
            "  → length, width, height (in order).\n\n"

            "- number_of_tires → Number of Tires.\n"
            "- tire_specifications → Tire Specifications.\n"
            "- wheelbase_mm → Wheelbase.\n"
            "- axle_load_kg → Axle Load (KEEP as string, e.g. '826/818').\n"
            "- number_of_axles → Number of Axles.\n"
            "- steering_type → Steering Type.\n\n"

            "- gross_weight_kg → Gross Vehicle Weight.\n"
            "- curb_weight_kg → Curb Weight.\n"
            "- rated_payload_kg → Rated Payload.\n"
            "- max_towing_capacity_kg → Maximum Towing Capacity.\n"
            "- passenger_capacity → Rated Passenger Capacity.\n"
            "- max_speed_kmh → Maximum Design Speed.\n"
            "- manufacturing_date → Date of Vehicle Manufacture.\n\n"

            "ABS EXTRACTION (STRICT):\n"
            "- Find text pattern: 'ABS model and manufacturer:'\n"
            "- abs_model = first value after this text\n"
            "- abs_manufacturer = remaining text after comma\n"
            "- Do NOT duplicate into remarks\n\n"

            "EDR RULE:\n"
            "- edr_system = true ONLY if 'EDR' appears in text\n"
            "- otherwise false\n\n"

            "REMARKS RULE:\n"
            "- Extract ONLY optional equipment and descriptive text\n"
            "- EXCLUDE structured values (ABS, power, VIN, etc.)\n"
            "- Keep text clean (no repetition)\n\n"

            "ADDRESS:\n"
            "- manufacturer_address → Vehicle Manufacturing Unit Address\n\n"

            "FINAL RULE:\n"
            "- Do NOT hallucinate\n"
            "- Do NOT merge fields\n"
            "- Only extract explicitly present data\n"
        ),
        "unknown": "Perform a general extraction of all visible entities into a flat JSON structure."
    }


settings = Settings()