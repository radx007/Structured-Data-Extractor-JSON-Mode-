# services/validation/errors.py

from pydantic import ValidationError

def format_pydantic_error(e):
    if isinstance(e, ValidationError):
        return {
            "status": "error",
            "errors": [
                {
                    "field": ".".join(map(str, err["loc"])),
                    "message": err["msg"]
                }
                for err in e.errors()
            ]
        }

    return {
        "status": "error",
        "message": str(e)
    }