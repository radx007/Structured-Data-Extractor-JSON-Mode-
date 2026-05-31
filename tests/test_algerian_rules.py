from app.services.reconciliation.algerian_rules import run_algerian_rules


def test_algerian_rules_ok(documents_valid):
    vin_result = {"status": "ok"}
    res = run_algerian_rules(documents_valid, vin_result)
    assert res["valid"] is True


def test_algerian_rules_missing_tech(documents_valid):
    docs = [d for d in documents_valid if d["document_type"] != "technical_details"]
    vin_result = {"status": "ok"}
    res = run_algerian_rules(docs, vin_result)
    assert res["valid"] is False


def test_algerian_rules_vehicle_age(documents_valid):
    tech = next(d for d in documents_valid if d["document_type"] == "technical_details")
    tech["extracted_data"]["manufacturing_date"] = "2018-01-01"
    vin_result = {"status": "ok"}
    res = run_algerian_rules(documents_valid, vin_result)
    assert res["valid"] is False


def test_algerian_rules_engine_size(documents_valid):
    tech = next(d for d in documents_valid if d["document_type"] == "technical_details")
    tech["extracted_data"]["displacement_ml"] = 2500
    vin_result = {"status": "ok"}
    res = run_algerian_rules(documents_valid, vin_result)
    assert res["valid"] is False
