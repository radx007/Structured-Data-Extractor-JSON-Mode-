from app.services.classifier import DocumentRouter
from app.services.glm_ocr import run_glm_ocr
from app.services.llm_extractor import run_llm_extraction
from app.services.reconciliation.report_builder import build_final_report
from app.services.validation.parser import validate_document
from app.utils.logging import logger
from app.config import settings, SCHEMAS, PROMPTS



router = DocumentRouter()

async def process_documents(files):
    results = []
    final_output = []

    try:
        # --- PHASE 1: OCR & EXTRACTION (streaming events) ---
        for file in files:
            if not file.content_type.startswith("image/"):
                yield {"type": "error", "filename": file.filename, "error": "Only images allowed"}
                continue

            try:
                contents = await file.read()
                if len(contents) > settings.MAX_SIZE:
                    yield {"type": "error", "filename": file.filename, "error": "File too large"}
                    continue

                logger.info(f"[{file.filename}] OCR Stage - Image received")

                # notify frontend OCR started
                yield {"type": "ocr_started", "filename": file.filename, "status": "processing"}

                # call existing OCR (keeps return semantics)
                final_data = await run_glm_ocr(contents)

                if not final_data:
                    logger.error(f"[{file.filename}] OCR returned empty result")
                    yield {"type": "ocr_failed", "filename": file.filename, "error": "OCR returned empty result"}
                    results.append({"filename": file.filename, "status": "error", "error": "OCR failed"})
                    continue

                # store and notify OCR completed
                results.append({
                    "filename": file.filename,
                    "data": final_data,
                    "status": "success"
                })

                yield {"type": "ocr_completed", "filename": file.filename, "status": "success",}
                logger.info(f"[{file.filename}] OCR Success.")

            except Exception as e:
                logger.error(f"[{file.filename}] OCR failed: {e}")
                yield {"type": "ocr_failed", "filename": file.filename, "error": str(e)}
                results.append({"filename": file.filename, "status": "error", "error": str(e)})

    except Exception as startup_error:
        logger.error(f"Failed to start OCR server: {startup_error}")
        yield {"type": "error", "error": "OCR Server failed to initialize"}
        return

    # --- PHASE 2: Classification ---
    ocr_results_dict = {res["filename"]: res["data"] for res in results if res.get("status") == "success"}

    if ocr_results_dict:
        yield {"type": "phase_started", "phase": "classification", "total_files": len(ocr_results_dict)}
        classifications = router.classify_documents(ocr_results_dict)

        for res in results:
            if res.get("status") == "success":
                doc_type = classifications.get(res["filename"], "unknown")
                res["document_type"] = doc_type
                logger.info(f"[{res['filename']}] Classification Stage - Classified as: {doc_type}")

        yield {"type": "classification_completed", }

    # --- PHASE 3: LLM Extraction (batch notifications) ---
    yield {"type": "phase_started", "phase": "extraction"}
    for res in results:
        if res.get("status") != "success":
            continue

        doc_type = res.get("document_type", "unknown")
        ocr_input = res.get("ocr_text") or str(res.get("data", ""))

        yield {"type": "extraction_started", "filename": res["filename"], "document_type": doc_type}

        try:
            final_json = await run_llm_extraction(
                ocr_input,
                SCHEMAS.get(doc_type, {}),
                PROMPTS.get(doc_type, "")
            )

            extracted = final_json.get("extracted_data", final_json)
            final_output.append({
                "filename": res["filename"],
                "document_type": doc_type,
                "extracted_data": extracted
            })

            yield {"type": "extraction_completed", "filename": res["filename"],}

        except Exception as e:
            logger.error(f"[{res['filename']}] LLM Extraction failed: {e}")
            yield {"type": "extraction_failed", "filename": res["filename"], "error": str(e)}
            res["status"] = "error"
            res["error"] = str(e)

        if "ocr_text" in res:
            del res["ocr_text"]

    # --- PHASE 4: Validation ---
    validated_documents = []
    failed_docs = []

    yield {"type": "phase_started", "phase": "validation", "total": len(final_output)}
    for item in final_output:
        vres = validate_document(item)
        if vres["status"] != "success":
            failed_docs.append({"filename": item["filename"], "errors": vres.get("errors")})
            yield {"type": "validation_failed", "filename": item["filename"], "errors": vres.get("errors")}
            continue

        validated_documents.append({"filename": item["filename"], **vres["data"]})
        yield {"type": "validation_completed", "filename": item["filename"], "data": vres["data"]}

    yield {"type": "validation_phase_completed", "total_validated": len(validated_documents), "total_failed": len(failed_docs)}

    # --- PHASE 5: Reconciliation ---
    yield {"type": "phase_started", "phase": "reconciliation"}
    final_report = build_final_report(validated_documents)

    yield {"type": "reconciliation_completed", }

    completed = {
        "documents": validated_documents,
        "failed_documents": failed_docs,
        "decision": final_report
    }

    yield {"type": "completed", "result": completed}