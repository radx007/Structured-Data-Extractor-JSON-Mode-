# services/validation/schemas/technical_details.py

from pydantic import BaseModel, field_validator
from typing import Optional, Literal
from datetime import date
from app.services.validation.common.validators import normalize_vin, parse_date, to_float


class Dimensions(BaseModel):
    length: float
    width: float
    height: float

    @field_validator("*", mode="before")
    def clean(cls, v):
        return to_float(v)


class TechnicalDetailsData(BaseModel):
    certificate_number: str
    issue_date: date
    manufacturer: str
    brand: str
    vehicle_name: str
    model: str
    chassis_number: str
    engine_model: str
    engine_number: str
    fuel_type: str

    displacement_ml: float
    power_kw: float
    emission_standard: str
    fuel_consumption: float

    dimensions_mm: Dimensions

    number_of_tires: int
    tire_specifications: str
    wheelbase_mm: float

    axle_load_kg: Optional[str] 

    number_of_axles: int
    steering_type: str

    gross_weight_kg: float
    curb_weight_kg: float

    rated_payload_kg: Optional[float]
    max_towing_capacity_kg: Optional[float]

    passenger_capacity: int
    max_speed_kmh: float

    manufacturing_date: date

    abs_model: Optional[str]
    abs_manufacturer: Optional[str]

    edr_system: Optional[bool]
    remarks: Optional[str]
    manufacturer_address: Optional[str]

    _issue_date = field_validator("issue_date", mode="before")(parse_date)
    _mfg_date = field_validator("manufacturing_date", mode="before")(parse_date)

    @field_validator(
        "displacement_ml", "power_kw", "fuel_consumption",
        "wheelbase_mm", "gross_weight_kg", "curb_weight_kg",
        "rated_payload_kg", "max_towing_capacity_kg",
        "max_speed_kmh",
        mode="before"
    )
    def clean_numbers(cls, v):
        return to_float(v)

    _vin = field_validator("chassis_number", mode="before")(normalize_vin)


class TechnicalDetails(BaseModel):
    document_type: Literal["technical_details"]
    extracted_data: TechnicalDetailsData