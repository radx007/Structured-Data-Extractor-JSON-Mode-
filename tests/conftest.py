from copy import deepcopy
import os
import sys
import pytest


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


@pytest.fixture()
def invoice_doc():
    return {
        "document_type": "invoice",
        "extracted_data": {
            "invoice_number": "INV-1",
            "invoice_date": "2025-09-23",
            "sc_number": "SC-1",
            "consignee": {"name": "JANE DOE", "passport": "874562193"},
            "transport": {
                "arrival_location": "SKIKDA",
                "country_of_departure": "China",
                "country_of_arrival": "Algeria",
            },
            "origin": {"country_of_origin": "China", "hs_code": "8703223010"},
            "items": [
                {
                    "marks": "N/M",
                    "description": "MG5 180DVVT",
                    "vin": "1HGCM82633A004352",
                    "quantity": 1,
                    "unit_price": 6200,
                    "line_total": 6200,
                }
            ],
            "charges": {"freight_cost": 1300},
            "totals": {
                "total_quantity": 1,
                "total_amount": 7500,
                "currency": "USD",
                "amount_in_words": "SEVEN THOUSAND FIVE HUNDRED",
            },
        },
    }


@pytest.fixture()
def packing_list_doc():
    return {
        "document_type": "packing_list",
        "extracted_data": {
            "consignee": "JANE DOE",
            "passport": "874562193",
            "sc_number": "SC-1",
            "invoice_number": "INV-1",
            "packing_list_number": "PL-1",
            "date": "2025-09-23",
            "departure_location": "NANSHA",
            "arrival_location": "SKIKDA",
            "items": [
                {
                    "marks": "N/M",
                    "description": "MG5",
                    "vin": "1HGCM82633A004352",
                    "quantity": 1,
                    "net_weight_kg": 1200,
                    "gross_weight_kg": 1300,
                    "volume_m3": 4.5,
                }
            ],
            "totals": {
                "quantity": 1,
                "net_weight_kg": 1200,
                "gross_weight_kg": 1300,
                "volume_m3": 4.5,
            },
        },
    }


@pytest.fixture()
def certificate_doc():
    return {
        "document_type": "certificate_of_origin",
        "extracted_data": {
            "certificate_number": "CO-1",
            "verification": "https://example.com",
            "exporter": {
                "name": "ORION AUTO EXPORTS",
                "address": "PORT ZONE 12",
                "country": "China",
            },
            "consignee": {
                "name": "JANE DOE",
                "passport": "874562193",
                "nin": "987654321098765432",
                "email": "jane.doe@example.com",
                "phone": "555123987",
                "address": "SKIKDA",
                "country": "Algeria",
            },
            "transport": {
                "mode": "SEA",
                "port_of_departure": "NANSHA",
                "port_of_arrival": "SKIKDA",
                "country_of_departure": "China",
                "country_of_arrival": "Algeria",
            },
            "destination_country": "Algeria",
            "goods": [
                {
                    "marks": "N/M",
                    "description": "MG5 180DVVT MANUAL YOUTH FASHION EDITION",
                    "vin": "1HGCM82633A004352",
                    "model": "MG5",
                    "manufacturing_year": 2024,
                    "manufacturer": "ORION MOTORS",
                    "unit_weight_kg": 1200,
                    "quantity": 1,
                }
            ],
            "classification": {"hs_code": "8703223010"},
            "invoice": {"invoice_number": "INV-1", "invoice_date": "2025-09-23"},
        },
    }


@pytest.fixture()
def technical_doc():
    return {
        "document_type": "technical_details",
        "extracted_data": {
            "certificate_number": "TD-1",
            "issue_date": "2025-09-23",
            "manufacturer": "ORION MOTORS",
            "brand": "MG",
            "vehicle_name": "MG5",
            "model": "MG5",
            "chassis_number": "1HGCM82633A004352",
            "engine_model": "E1",
            "engine_number": "EN123",
            "fuel_type": "gasoline",
            "displacement_ml": 1800,
            "power_kw": 110,
            "emission_standard": "EURO 6",
            "fuel_consumption": 6.5,
            "dimensions_mm": {"length": 4600, "width": 1800, "height": 1500},
            "number_of_tires": 4,
            "tire_specifications": "205/55R16",
            "wheelbase_mm": 2650,
            "axle_load_kg": "826/818",
            "number_of_axles": 2,
            "steering_type": "LHD",
            "gross_weight_kg": 1600,
            "curb_weight_kg": 1300,
            "rated_payload_kg": 300,
            "max_towing_capacity_kg": 500,
            "passenger_capacity": 5,
            "max_speed_kmh": 180,
            "manufacturing_date": "2025-01-10",
            "abs_model": "ABS-1",
            "abs_manufacturer": "Bosch",
            "edr_system": True,
            "remarks": "Standard",
            "manufacturer_address": "Shanghai",
        },
    }


@pytest.fixture()
def documents_valid(invoice_doc, packing_list_doc, certificate_doc, technical_doc):
    return [
        {"document_type": "invoice", "extracted_data": deepcopy(invoice_doc["extracted_data"])},
        {"document_type": "packing_list", "extracted_data": deepcopy(packing_list_doc["extracted_data"])},
        {"document_type": "certificate_of_origin", "extracted_data": deepcopy(certificate_doc["extracted_data"])},
        {"document_type": "technical_details", "extracted_data": deepcopy(technical_doc["extracted_data"])},
    ]
