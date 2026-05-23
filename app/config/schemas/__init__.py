from .packing_list import PACKING_LIST_SCHEMA
from .certificate_of_origin import CERTIFICATE_OF_ORIGIN_SCHEMA
from .invoice import INVOICE_SCHEMA
from .technical_details import TECHNICAL_DETAILS_SCHEMA

SCHEMAS = {
    "packing_list": PACKING_LIST_SCHEMA,
    "certificate_of_origin": CERTIFICATE_OF_ORIGIN_SCHEMA,
    "invoice": INVOICE_SCHEMA,
    "technical_details": TECHNICAL_DETAILS_SCHEMA,
}