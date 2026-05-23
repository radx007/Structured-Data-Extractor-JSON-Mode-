from .packing_list_prompt import PACKING_LIST_PROMPT
from .certificate_prompt import CERTIFICATE_OF_ORIGIN_PROMPT
from .invoice_prompt import INVOICE_PROMPT
from .technical_details_prompt import TECHNICAL_DETAILS_PROMPT

PROMPTS = {
    "packing_list": PACKING_LIST_PROMPT,
    "certificate_of_origin": CERTIFICATE_OF_ORIGIN_PROMPT,
    "commercial_invoice": INVOICE_PROMPT,
    "technical_details": TECHNICAL_DETAILS_PROMPT,
    "unknown": (
        "Perform a general extraction "
        "of all visible entities into a flat JSON structure."
    ),
}