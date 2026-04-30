from typing import Dict, List, Any


class CrossCheckResult:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def add_error(self, msg: str):
        self.errors.append({"type": "error", "message": msg})

    def add_warning(self, msg: str):
        self.warnings.append({"type": "warning", "message": msg})

    def to_dict(self):
        return {
            "errors": self.errors,
            "warnings": self.warnings,
            "is_valid": len(self.errors) == 0
        }


def get_doc(docs: List[Dict], doc_type: str):
    return next((d["extracted_data"] for d in docs if d["document_type"] == doc_type), None)


def check_consignee(docs, result: CrossCheckResult):
    names = set()

    for d in docs:
        data = d["extracted_data"]

        if isinstance(data.get("consignee"), dict):
            name = data["consignee"].get("name")
        else:
            name = data.get("consignee")

        if name:
            names.add(name.strip().upper())

    if len(names) > 1:
        result.add_error(f"Consignee mismatch across documents: {list(names)}")


def check_invoice_number(docs, result: CrossCheckResult):
    invoice_numbers = set()

    invoice_doc = get_doc(docs, "invoice")
    coc_doc = get_doc(docs, "certificate_of_origin")

    if invoice_doc:
        invoice_numbers.add(invoice_doc.get("invoice_number"))

    if coc_doc:
        invoice_numbers.add(coc_doc.get("invoice", {}).get("invoice_number"))

    invoice_numbers = {i for i in invoice_numbers if i}

    if len(invoice_numbers) > 1:
        result.add_warning(
            f"Invoice number mismatch: {list(invoice_numbers)}"
        )

def check_weights(docs, result: CrossCheckResult):
    packing = get_doc(docs, "packing_list")
    tech = get_doc(docs, "technical_details")

    if not packing or not tech:
        return

    try:
        packing_weight = packing["totals"]["gross_weight_kg"]
        tech_weight = tech["curb_weight_kg"]

        if abs(packing_weight - tech_weight) > 50: 
            result.add_warning(
                f"Weight mismatch: packing={packing_weight}, technical={tech_weight}"
            )
    except:
        pass


def check_model(docs, result: CrossCheckResult):
    models = set()

    coc = get_doc(docs, "certificate_of_origin")
    tech = get_doc(docs, "technical_details")

    if coc:
        for g in coc.get("goods", []):
            if g.get("model"):
                models.add(g["model"].strip().upper())

    if tech and tech.get("model"):
        models.add(tech["model"].strip().upper())

    if len(models) > 1:
        result.add_error(f"Model mismatch across documents: {list(models)}")


def run_cross_document_checks(documents: List[Dict[str, Any]]) -> Dict[str, Any]:
    result = CrossCheckResult()

    check_consignee(documents, result)
    check_invoice_number(documents, result)
    check_weights(documents, result)
    check_model(documents, result)

    return result.to_dict()