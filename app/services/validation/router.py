from typing import Dict, Type

from app.services.validation.schemas.packing_list import PackingList
from app.services.validation.schemas.invoice import Invoice
from app.services.validation.schemas.certificate_of_origin import CertificateOfOrigin
from app.services.validation.schemas.technical_details import TechnicalDetails


DOCUMENT_MODELS: Dict[str, Type] = {
    "packing_list": PackingList,
    "invoice": Invoice,
    "certificate_of_origin": CertificateOfOrigin,
    "technical_details": TechnicalDetails,
}


def get_model(document_type: str):
    """
    Returns the correct Pydantic model based on document type.
    """

    if not document_type:
        raise ValueError("Missing document_type")

    model = DOCUMENT_MODELS.get(document_type)

    if not model:
        raise ValueError(f"Unsupported document type: {document_type}")

    return model