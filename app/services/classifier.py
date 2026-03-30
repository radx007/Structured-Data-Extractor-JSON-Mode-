class DocumentRouter:
    def __init__(self):
        # Anchor keywords normalized to UPPERCASE for easier matching
        self.rules = {
            "certificate_of_origin": [
                "CERTIFICATE OF ORIGIN", 
                "PEOPLE'S REPUBLIC OF CHINA", 
                "ORIGIN.CUSTOMS.GOV.CN"
            ],
            "packing_list": [
                "PACKING LIST NO.", 
                "MEASUREMENT (M³)", 
                "NET WEIGHT (KG)",
                "GROSS WEIGHT (KG)"
            ],
            "invoice": [
                "COMMERCIAL INVOICE", 
                "UNIT PRICE", 
                "OCEAN FREIGHT FEE", 
                "SAY US DOLLARS"
            ],
            "technical_details": [
                "VEHICLE IDENTIFICATION NUMBER", 
                "EMISSION STANDARD", 
                "MAXIMUM DESIGN SPEED", 
                "CURB WEIGHT (KG)",
                "CHASSIS NO:",
                "VEHICLE MANUFACTURING ENTERPRISE INFORMATION"
            ]
        }

    def classify(self, text_content: str) -> str:
        """
        Core logic: Score the text against keyword rules.
        """
        if not text_content:
            return "unknown"

        content_upper = text_content.upper()
        scores = {doc_type: 0 for doc_type in self.rules}
        
        for doc_type, keywords in self.rules.items():
            for word in keywords:
                if word in content_upper:
                    scores[doc_type] += 1
        
        # Find the best match
        best_match = max(scores, key=scores.get)
        
        
        return best_match if scores[best_match] > 0 else "unknown"

    def process_ocr_results(self, markdown_text: str) -> str:
        """
        Returns the single document type for the current file.
        """
        doc_type = self.classify(markdown_text)
        
        return doc_type