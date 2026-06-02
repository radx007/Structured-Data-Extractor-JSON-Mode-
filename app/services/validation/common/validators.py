import re
from datetime import datetime

VIN_REGEX = r"^[A-HJ-NPR-Z0-9]{17}$"

# Common values produced by OCR/LLMs when data is missing
NULL_VALUES = {
    "",
    "-",
    "--",
    "---",
    "N/A",
    "NA",
    "NULL",
    "NONE",
    "UNKNOWN",
}


def _normalize_text(v):
    """
    Normalize common OCR/LLM placeholders.

    Examples:
        ""       -> None
        "-"      -> None
        "N/A"    -> None
        " null " -> None
    """
    if v is None:
        return None

    if isinstance(v, str):
        v = v.strip()

        if v.upper() in NULL_VALUES:
            return None

    return v


def normalize_vin(v):
    """
    Validate and normalize a VIN.

    Returns:
        Uppercase VIN string

    Raises:
        ValueError if VIN is invalid.
    """
    v = _normalize_text(v)

    if v is None:
        return None

    if not isinstance(v, str):
        raise ValueError("VIN must be a string")

    v = v.upper()

    if not re.fullmatch(VIN_REGEX, v):
        raise ValueError(f"Invalid VIN: {v}")

    return v


def parse_date(v):
    """
    Parse dates from common OCR/LLM formats.

    Supported:
        2025-09-23
        September 23, 2025
        Sep 23, 2025
        23/09/2025
        23-09-2025
        2025/09/23

    Returns:
        datetime.date or None
    """
    v = _normalize_text(v)

    if v is None:
        return None

    if hasattr(v, "year") and hasattr(v, "month") and hasattr(v, "day"):
        try:
            return v.date()
        except AttributeError:
            return v

    formats = (
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%B %d, %Y",
        "%b %d, %Y",
    )

    for fmt in formats:
        try:
            return datetime.strptime(str(v).strip(), fmt).date()
        except ValueError:
            continue

    raise ValueError(f"Invalid date: {v}")


def to_float(v):
    """
    Convert numeric strings to float.

    Handles:
        "1,234.50"
        "1234"
        1234
        "-"
        ""
        "N/A"

    Returns:
        float or None
    """
    v = _normalize_text(v)

    if v is None:
        return None

    try:
        if isinstance(v, str):
            v = v.replace(",", "").strip()

        return float(v)

    except (TypeError, ValueError):
        raise ValueError(f"Invalid number: {v}")


def to_int(v):
    """
    Convert values to integer.

    Handles:
        "4"
        "4.0"
        4
        "-"
        ""
        "N/A"

    Returns:
        int or None
    """
    v = _normalize_text(v)

    if v is None:
        return None

    try:
        if isinstance(v, str):
            v = v.replace(",", "").strip()

        return int(float(v))

    except (TypeError, ValueError):
        raise ValueError(f"Invalid integer: {v}")


def clean_optional_string(v):
    """
    Normalize optional text fields.

    Examples:
        "-"      -> None
        "N/A"    -> None
        " Bosch " -> "Bosch"
    """
    v = _normalize_text(v)

    if v is None:
        return None

    return str(v).strip()