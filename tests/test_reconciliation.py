from app.services.reconciliation.vin_reconciliation import reconcile_vins
from app.services.reconciliation.cross_document_checks import run_cross_document_checks


def test_reconcile_vins_ok(documents_valid):
    res = reconcile_vins(documents_valid)
    assert res["status"] == "ok"


def test_reconcile_vins_mismatch(documents_valid):
    documents_valid[0]["extracted_data"]["items"][0]["vin"] = "LSJA36U31SN090070"
    res = reconcile_vins(documents_valid)
    assert res["status"] == "mismatch"


def test_cross_checks_ok(documents_valid):
    res = run_cross_document_checks(documents_valid)
    assert res["is_valid"] is True
    assert res["errors"] == []


def test_cross_checks_consignee_mismatch(documents_valid):
    documents_valid[0]["extracted_data"]["consignee"]["name"] = "OTHER"
    res = run_cross_document_checks(documents_valid)
    assert res["is_valid"] is False


def test_cross_checks_invoice_number_warning(documents_valid):
    documents_valid[2]["extracted_data"]["invoice"]["invoice_number"] = "INV-2"
    res = run_cross_document_checks(documents_valid)
    assert len(res["warnings"]) > 0


def test_cross_checks_weight_warning(documents_valid):
    documents_valid[1]["extracted_data"]["totals"]["gross_weight_kg"] = 2000
    res = run_cross_document_checks(documents_valid)
    assert len(res["warnings"]) > 0


def test_cross_checks_model_mismatch(documents_valid):
    documents_valid[2]["extracted_data"]["goods"][0]["model"] = "DIFF"
    res = run_cross_document_checks(documents_valid)
    assert res["is_valid"] is False
