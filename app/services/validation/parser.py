from app.services.validation.router import get_model
from app.services.validation.errors import format_pydantic_error


def validate_document(raw_doc: dict):
    try:

        model = get_model(raw_doc["document_type"])

        validated = model.model_validate(raw_doc)

        return {
            "status": "success",
            "data": validated.model_dump(mode="json")
        }

    except Exception as e:
        return format_pydantic_error(e)