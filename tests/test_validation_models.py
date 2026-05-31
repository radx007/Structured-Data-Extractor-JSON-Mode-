from app.services.validation.parser import validate_document


def test_invoice_valid(invoice_doc):
    res = validate_document(invoice_doc)
    assert res["status"] == "success"


def test_invoice_total_mismatch(invoice_doc):
    invoice_doc["extracted_data"]["totals"]["total_amount"] = 1
    res = validate_document(invoice_doc)
    assert res["status"] == "error"


def test_invoice_bad_vin(invoice_doc):
    invoice_doc["extracted_data"]["items"][0]["vin"] = "BADVIN"
    res = validate_document(invoice_doc)
    assert res["status"] == "error"


def test_packing_list_valid(packing_list_doc):
    res = validate_document(packing_list_doc)
    assert res["status"] == "success"


def test_packing_list_totals_mismatch(packing_list_doc):
    packing_list_doc["extracted_data"]["totals"]["gross_weight_kg"] = 999
    res = validate_document(packing_list_doc)
    assert res["status"] == "error"


def test_certificate_valid(certificate_doc):
    res = validate_document(certificate_doc)
    assert res["status"] == "success"


def test_technical_valid(technical_doc):
    res = validate_document(technical_doc)
    assert res["status"] == "success"


def test_technical_missing_required(technical_doc):
    technical_doc["extracted_data"]["manufacturer"] = None
    res = validate_document(technical_doc)
    assert res["status"] == "error"
