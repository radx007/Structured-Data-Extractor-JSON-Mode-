import re
from datetime import datetime

VIN_REGEX = r"^[A-HJ-NPR-Z0-9]{17}$"

def normalize_vin(v):
    if v is None:
        return None
    v = v.strip().upper()
    if not re.match(VIN_REGEX, v):
        raise ValueError("Invalid VIN")
    return v

def parse_date(v):
    if v is None:
        return None
    for fmt in ("%Y-%m-%d", "%B %d, %Y"):
        try:
            return datetime.strptime(v, fmt).date()
        except:
            continue
    raise ValueError(f"Invalid date: {v}")

def to_float(v):
    if v in (None, "", "N/A"):
        return None
    try:
        if isinstance(v, str):
            v = v.replace(",", "").strip()
        return float(v)
    except:
        raise ValueError(f"Invalid number: {v}")