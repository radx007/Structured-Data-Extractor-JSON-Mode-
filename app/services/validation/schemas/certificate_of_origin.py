from pydantic import BaseModel, field_validator
from typing import List, Optional, Literal
from datetime import date
from app.services.validation.common.validators import normalize_vin, parse_date, to_float


class GoodsItem(BaseModel):
    marks: Optional[str]
    description: str
    vin: str
    model: str
    manufacturing_year: int
    manufacturer: str
    unit_weight_kg: float
    quantity: float

    _vin = field_validator("vin", mode="before")(normalize_vin)

    @field_validator("unit_weight_kg", "quantity", mode="before")
    def clean_numbers(cls, v):
        return to_float(v)


class InvoiceRef(BaseModel):
    invoice_number: Optional[str] 
    invoice_date: date

    _date = field_validator("invoice_date", mode="before")(parse_date)


class CertificateData(BaseModel):
    certificate_number: Optional[str]
    verification: Optional[str]

    exporter: dict
    consignee: dict
    transport: dict

    destination_country: str
    goods: List[GoodsItem]

    classification: dict
    invoice: InvoiceRef


class CertificateOfOrigin(BaseModel):
    document_type: Literal["certificate_of_origin"]
    extracted_data: CertificateData