import pytest
from app.services.validation.common.validators import normalize_vin, parse_date, to_float


def test_normalize_vin_ok():
    assert normalize_vin("lsja36u31sn090069") == "LSJA36U31SN090069"


def test_normalize_vin_bad():
    with pytest.raises(ValueError):
        normalize_vin("BADVIN")


def test_parse_date_iso():
    assert str(parse_date("2025-09-23")) == "2025-09-23"


def test_parse_date_text():
    assert str(parse_date("September 23, 2025")) == "2025-09-23"


def test_to_float_commas():
    assert to_float("1,234.50") == 1234.5


def test_to_float_empty():
    assert to_float("") is None


def test_to_float_invalid():
    with pytest.raises(ValueError):
        to_float("abc")
