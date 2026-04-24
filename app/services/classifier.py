import json
import requests
from typing import Dict, List

class DocumentRouter:
    def __init__(self):
        self.doc_types = [
            "certificate_of_origin",
            "packing_list",
            "invoice",
            "technical_details",
            "unknown"
        ]
        self.model = "llama3.2:3b"
        self.ollama_url = "http://localhost:11434/api/generate"

    def classify_documents(self, ocr_results: Dict[str, str]) -> Dict[str, str]:
        """
        Classifies OCR text using a local LLM with strict JSON enforcement.
        """
        if not ocr_results:
            return {}

        categories_str = ", ".join(self.doc_types)
        
        prompt = (
            f"Classify each document based on its OCR text.\n"
            f"Allowed Categories: {categories_str}\n\n"

            "DOCUMENT TYPE DEFINITIONS (VERY IMPORTANT):\n"

            "certificate_of_origin:\n"
            "- Contains: exporter, consignee, country of origin\n"
            "- Mentions: certificate number, customs, origin verification\n"
            "- Often includes: HS code, official stamps, export validation\n\n"

            "packing_list:\n"
            "- Contains: list of items, quantities, weights, volume\n"
            "- Mentions: net weight, gross weight, packaging details\n"
            "- NO prices or financial totals\n\n"

            "invoice:\n"
            "- Contains: prices, unit price, total amount, currency\n"
            "- Mentions: invoice number, payment, cost breakdown\n"
            "- Includes financial data (USD, total, amount in words)\n\n"

            "technical_details:\n"
            "- Contains: vehicle specifications\n"
            "- Mentions: VIN, engine number, weight, dimensions, power\n"
            "- Includes technical data (kg, mm, km/h)\n\n"

            "unknown:\n"
            "- Use if the document does not clearly match any category\n\n"

            "STRICT RULES:\n"
            "1. Return ONLY valid JSON.\n"
            "2. Keys = filenames.\n"
            "3. Values MUST be EXACTLY one of the Allowed Categories.\n"
            "4. If unsure → 'unknown'.\n"
            "5. Do NOT explain.\n\n"

            "CLASSIFICATION LOGIC:\n"
            "- Use keywords and structure, not guessing.\n"
            "- If prices exist → invoice.\n"
            "- If only weights/quantities → packing_list.\n"
            "- If vehicle specs → technical_details.\n"
            "- If export/certification/origin → certificate_of_origin.\n\n"

            "VALIDATION STEP:\n"
            f"Ensure every value is one of: {categories_str}.\n"
            "Otherwise replace with 'unknown'.\n\n"

            f"DATA:\n{json.dumps(ocr_results)}\n\n"

            "JSON Response:"
        )

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,  
            "format": "json",
            "options": {
                "temperature": 0,
                "stop": ["\n\n"]
            },
            "keep_alive": "5m"
        }

        try:
            response = requests.post(
                self.ollama_url,
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            
            raw_response = response.json()
            llm_content = raw_response.get("response", "{}")
            
            return json.loads(llm_content)
            
        except Exception as e:
            print(f"Criticial Error in Classification: {e}")
            return {filename: "unknown" for filename in ocr_results.keys()}
