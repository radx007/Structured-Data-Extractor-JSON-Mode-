
from pydantic import BaseModel, field_validator, model_validator
from typing import List, Optional, Literal
from datetime import datetime
import re
from app.services.validation.common.validators import normalize_vin, parse_date, to_float

class PackingItem(BaseModel):
    marks: Optional[str]
    description: str
    vin: str
    quantity: float
    net_weight_kg: float
    gross_weight_kg: float
    volume_m3: float

    # VIN validation
    _vin = field_validator("vin", mode="before")(normalize_vin)

    # Number normalization
    @field_validator("*", mode="before")
    def clean_numbers(cls, v, info):
        if info.field_name in [
            "quantity", "net_weight_kg",
            "gross_weight_kg", "volume_m3"
        ]:
            return to_float(v)
        return v


class PackingTotals(BaseModel):
    quantity: float
    net_weight_kg: float
    gross_weight_kg: float
    volume_m3: float

    @field_validator("*", mode="before")
    def clean_numbers(cls, v):
        return to_float(v)


class PackingListData(BaseModel):
    consignee: str
    passport: str
    sc_number: str
    invoice_number: str
    packing_list_number: str
    date: datetime
    departure_location: str
    arrival_location: str
    items: List[PackingItem]
    totals: PackingTotals

    # Date normalization
    _date = field_validator("date", mode="before")(parse_date)

    @model_validator(mode="after")
    def check_totals(self):
        total_qty = sum(item.quantity for item in self.items)
        total_net = sum(item.net_weight_kg for item in self.items)
        total_gross = sum(item.gross_weight_kg for item in self.items)
        total_volume = sum(item.volume_m3 for item in self.items)

        # tolerance for float rounding
        tol = 0.01

        if abs(total_qty - self.totals.quantity) > tol:
            raise ValueError(f"Quantity mismatch: items={total_qty}, totals={self.totals.quantity}")

        if abs(total_net - self.totals.net_weight_kg) > tol:
            raise ValueError("Net weight mismatch")

        if abs(total_gross - self.totals.gross_weight_kg) > tol:
            raise ValueError("Gross weight mismatch")

        if abs(total_volume - self.totals.volume_m3) > tol:
            raise ValueError("Volume mismatch")

        return self


class PackingList(BaseModel):
    document_type: Literal["packing_list"]
    extracted_data: PackingListData