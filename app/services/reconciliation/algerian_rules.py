from typing import Dict, Any, List
from datetime import date


class RulesResult:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def add_error(self, msg: str):
        self.errors.append({"type": "error", "message": msg})

    def add_warning(self, msg: str):
        self.warnings.append({"type": "warning", "message": msg})

    def to_dict(self):
        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings
        }

def get_doc(docs: List[Dict], doc_type: str):
    return next((d["extracted_data"] for d in docs if d["document_type"] == doc_type), None)


def check_vehicle_age(tech: Dict, result: RulesResult):
    mfg_date = tech.get("manufacturing_date")

    if not mfg_date:
        result.add_warning("Missing manufacturing date")
        return

    year = int(str(mfg_date)[:4])
    current_year = date.today().year

    age = current_year - year

    if age > 3:
        result.add_error(f"Vehicle too old ({age} years > 3 years limit)")


def check_engine_displacement(tech: Dict, result: RulesResult):
    displacement = tech.get("displacement_ml")

    if displacement is None:
        return

    if displacement > 2000:
        result.add_error(f"Engine too large ({displacement} cc > 2000 cc limit)")


def check_fuel_type(tech: Dict, result: RulesResult):
    fuel = tech.get("fuel_type")

    if not fuel:
        result.add_warning("Missing fuel type")
        return

    fuel = fuel.lower()

    if fuel not in ["gasoline", "petrol"]:
        result.add_warning(f"Uncommon or restricted fuel type: {fuel}")


def check_emission_standard(tech: Dict, result: RulesResult):
    emission = tech.get("emission_standard")

    if not emission:
        result.add_warning("Missing emission standard")
        return

    emission = emission.upper()

    # crude normalization
    if "EURO" in emission:
        return

    if "CHINA" in emission:
        result.add_warning("Non-European emission standard (China standard)")


def check_required_fields(tech: Dict, result: RulesResult):
    required_fields = [
        "manufacturer",
        "model",
        "chassis_number",
        "engine_number"
    ]

    for field in required_fields:
        if not tech.get(field):
            result.add_error(f"Missing required field: {field}")


def run_algerian_rules(documents: List[Dict[str, Any]], vin_result: Dict[str, Any]) -> Dict[str, Any]:
    result = RulesResult()

    # -------------------------
    # 0. VIN must be valid
    # -------------------------
    if vin_result["status"] != "ok":
        result.add_error("VIN mismatch across documents")

    # -------------------------
    # 1. Get technical doc
    # -------------------------
    tech = get_doc(documents, "technical_details")

    if not tech:
        result.add_error("Missing technical details document")
        return result.to_dict()

    # -------------------------
    # 2. Apply rules
    # -------------------------
    check_vehicle_age(tech, result)
    check_engine_displacement(tech, result)
    check_fuel_type(tech, result)
    check_emission_standard(tech, result)
    check_required_fields(tech, result)

    return result.to_dict()