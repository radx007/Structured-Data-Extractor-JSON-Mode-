PACKING_LIST_PROMPT = (
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
        )