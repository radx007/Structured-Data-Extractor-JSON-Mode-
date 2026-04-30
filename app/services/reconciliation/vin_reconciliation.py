from typing import Dict, List, Set, Any


# -------------------------
# Extract VINs from one document
# -------------------------
def extract_vins_from_document(doc: Dict[str, Any]) -> Set[str]:
    vins = set()

    data = doc.get("extracted_data", {})

    # Case 1: packing / invoice items
    for item in data.get("items", []):
        vin = item.get("vin")
        if vin:
            vins.add(vin)

    # Case 2: certificate goods
    for g in data.get("goods", []):
        vin = g.get("vin")
        if vin:
            vins.add(vin)

    # Case 3: technical details (single source of truth)
    chassis = data.get("chassis_number")
    if chassis:
        vins.add(chassis)

    return vins


# -------------------------
# Main reconciliation logic
# -------------------------
def reconcile_vins(documents: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Returns:
        {
            "status": "ok" | "mismatch",
            "vin": str | None,
            "details": {...}
        }
    """

    vin_map = {}

    for doc in documents:
        doc_type = doc.get("document_type")
        vins = extract_vins_from_document(doc)

        vin_map[doc_type] = list(vins)

    # Flatten all VINs across documents
    all_vins = set()
    for vins in vin_map.values():
        all_vins.update(vins)

    # -------------------------
    # CASE 1: everything matches
    # -------------------------
    if len(all_vins) == 1:
        return {
            "status": "ok",
            "vin": list(all_vins)[0],
            "details": vin_map
        }

    # -------------------------
    # CASE 2: mismatch detected
    # -------------------------
    return {
        "status": "mismatch",
        "vin": None,
        "details": vin_map,
        "conflict": list(all_vins)
    }