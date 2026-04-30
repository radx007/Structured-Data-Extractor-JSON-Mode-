from pydantic import BaseModel, field_validator, model_validator
from typing import List, Optional, Literal
from datetime import date
from app.services.validation.common.validators import normalize_vin, parse_date, to_float


class InvoiceItem(BaseModel):
    marks: Optional[str]
    description: str
    vin: str
    quantity: float
    unit_price: float
    line_total: float

    _vin = field_validator("vin", mode="before")(normalize_vin)

    @field_validator("quantity", "unit_price", "line_total", mode="before")
    def clean_numbers(cls, v):
        return to_float(v)

    @model_validator(mode="after")
    def check_line_total(self):
        expected = (self.quantity or 0) * (self.unit_price or 0)

        if abs(expected - self.line_total) > 0.01:
            raise ValueError(
                f"Line total mismatch: expected={expected}, got={self.line_total}"
            )
        return self


class Charges(BaseModel):
    freight_cost: Optional[float]

    @field_validator("freight_cost", mode="before")
    def clean(cls, v):
        return to_float(v)

class Totals(BaseModel):
    total_quantity: float
    total_amount: float
    currency: str
    amount_in_words: Optional[str]

    @field_validator("total_quantity", "total_amount", mode="before")
    def clean(cls, v):
        return to_float(v)

class InvoiceData(BaseModel):
    invoice_number: str
    invoice_date: date
    sc_number: str

    consignee: dict
    transport: dict
    origin: dict

    items: List[InvoiceItem]
    charges: Charges
    totals: Totals

    _date = field_validator("invoice_date", mode="before")(parse_date)

    @model_validator(mode="after")
    def check_totals(self):
        items_total = sum(i.line_total or 0 for i in self.items)
        freight = self.charges.freight_cost or 0
        expected = items_total + freight

        if abs(expected - self.totals.total_amount) > 0.01:
            raise ValueError(
                f"Invoice total mismatch: expected={expected}, got={self.totals.total_amount}"
            )
        return self


class Invoice(BaseModel):
    document_type: Literal["invoice"]
    extracted_data: InvoiceData