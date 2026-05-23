CERTIFICATE_OF_ORIGIN_PROMPT =  (
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
        )