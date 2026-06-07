INVOICE_PROMPT = (
            "Extract structured data from the document into the schema. Do not guess or invent missing values. "

            "HEADER:"
            "- Extract invoice_number, sc_number, invoice_date (normalize to YYYY-MM-DD). "

            "PARTIES:"
            "- Extract consignee name and passport (digits only) ONLY from the (To:) / consignee section. Never use names from the company header, issuer, seller, exporter, or (From:) section."

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
            "- vin MUST be exactly 17 characters"
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
            "- total_amount = Extract the final total amount (numeric only). general rule: look for the largest numeric value in the document. "
            "- currency = Extract the currency (e.g., USD, EUR). "
            "- amount_in_words = clean text only (remove filler words like SAY/ONLY). "

            "GENERAL RULES:"
            "- Never hallucinate missing fields. "
            "- Never return empty strings → use null only. "
            "- Do not merge unrelated fields. "
        )