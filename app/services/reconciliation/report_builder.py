from typing import List, Dict, Any

from app.services.reconciliation import reconcile_vins, run_cross_document_checks, run_algerian_rules


def build_final_report(documents: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Full reconciliation + compliance pipeline
    """

    # -------------------------
    # 1. VIN Reconciliation
    # -------------------------
    vin_result = reconcile_vins(documents)

    # -------------------------
    # 2. Cross-document checks
    # -------------------------
    cross_checks = run_cross_document_checks(documents)

    # -------------------------
    # 3. Algerian compliance rules
    # -------------------------
    rules_result = run_algerian_rules(documents, vin_result)

    # -------------------------
    # 4. Final decision logic
    # -------------------------
    final_valid = (
        vin_result["status"] == "ok"
        and cross_checks["is_valid"]
        and rules_result["valid"]
    )

    # -------------------------
    # 5. Collect all issues
    # -------------------------
    all_errors = []
    all_warnings = []

    # VIN errors
    if vin_result["status"] != "ok":
        all_errors.append({
            "type": "vin_mismatch",
            "message": "VIN mismatch across documents",
            "details": vin_result.get("details")
        })

    # Cross-doc
    all_errors.extend(cross_checks["errors"])
    all_warnings.extend(cross_checks["warnings"])

    # Rules
    all_errors.extend(rules_result["errors"])
    all_warnings.extend(rules_result["warnings"])

    # -------------------------
    # 6. Final structured output
    # -------------------------
    return {
        "status": "approved" if final_valid else "rejected",

        "vin": vin_result.get("vin"),

        "summary": {
            "valid": final_valid,
            "total_errors": len(all_errors),
            "total_warnings": len(all_warnings)
        },

        "errors": all_errors,
        "warnings": all_warnings,

        "debug": {
            "vin_details": vin_result.get("details"),
            "cross_checks": cross_checks,
            "rules": rules_result
        }
    }