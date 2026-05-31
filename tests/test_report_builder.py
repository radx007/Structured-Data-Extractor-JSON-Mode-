from app.services.reconciliation.report_builder import build_final_report


def test_report_approved(documents_valid):
    report = build_final_report(documents_valid)
    assert report["status"] == "approved"


def test_report_rejected(documents_valid):
    documents_valid[0]["extracted_data"]["items"][0]["vin"] = "LSJA36U31SN090070"
    report = build_final_report(documents_valid)
    assert report["status"] == "rejected"
