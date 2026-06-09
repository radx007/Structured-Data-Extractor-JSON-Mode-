from app.services import DocumentRouter, run_glm_ocr, run_llm_json_mapping
from app.services.reconciliation.report_builder import build_final_report
from app.services.validation.parser import validate_document
from app.utils.logging import logger
from app.utils.glm_server import get_ocr_server
from app.utils.llama_server import LlamaServer
from app.config import settings, SCHEMAS, PROMPTS


router = DocumentRouter()


async def process_documents(files):
    results = []
    final_output = []

    # ------------------------------------------------------------------ #
    # PHASE 1: OCR — start GLM-OCR server, run all images, then stop it  #
    # ------------------------------------------------------------------ #
    ocr_server = get_ocr_server()

    try:
        import asyncio
        await asyncio.to_thread(ocr_server.start)
        logger.info("GLM-OCR server started for OCR phase.")
    except Exception as e:
        logger.error(f"Failed to start GLM-OCR server: {e}")
        yield {"type": "error", "error": "OCR Server failed to initialize"}
        return

    try:
        for file in files:
            try:
                content_type = file.content_type or ""
                if not content_type.startswith("image/"):
                    yield {"type": "error", "filename": file.filename, "error": "Only images allowed"}
                    continue

                contents = await file.read()
                if len(contents) > settings.MAX_SIZE:
                    yield {"type": "error", "filename": file.filename, "error": "File too large"}
                    continue

                logger.info(f"[{file.filename}] OCR Stage - Image received")
                yield {"type": "ocr_started", "filename": file.filename, "status": "processing"}

                final_data = await run_glm_ocr(contents)

                if not final_data:
                    logger.error(f"[{file.filename}] OCR returned empty result")
                    yield {"type": "ocr_failed", "filename": file.filename, "error": "OCR returned empty result"}
                    results.append({"filename": file.filename, "status": "error", "error": "OCR failed"})
                    continue

                results.append({"filename": file.filename, "data": final_data, "status": "success"})
                yield {"type": "ocr_completed", "filename": file.filename, "status": "success"}

            except Exception as e:
                logger.error(f"[{file.filename}] OCR failed: {e}")
                yield {"type": "ocr_failed", "filename": file.filename, "error": str(e)}
                results.append({"filename": file.filename, "status": "error", "error": str(e)})

    finally:
        # Always stop OCR server after all images are done — frees VRAM for LLM
        await asyncio.to_thread(ocr_server.stop)
        logger.info("GLM-OCR server stopped. VRAM free for LLM.")

    # ------------------------------------------------------------------ #
    # PHASE 2 & 3: Classification + Extraction — LLM server starts here  #
    # ------------------------------------------------------------------ #
    ocr_results_dict = {
        res["filename"]: res["data"]
        for res in results
        if res.get("status") == "success"
    }

    if not ocr_results_dict:
        pass
    else:
        try:
            # LlamaServer starts here (VRAM now free from OCR server)
            with LlamaServer() as llama:
                yield {"type": "phase_started", "phase": "classification", "total_files": len(ocr_results_dict)}
                classifications = router.classify_documents(ocr_results_dict)

                for res in results:
                    if res.get("status") == "success":
                        doc_type = classifications.get(res["filename"], "unknown")
                        res["document_type"] = doc_type

                yield {"type": "classification_completed"}

                # --- PHASE 3: JSON mapping ---
                yield {"type": "phase_started", "phase": "extraction"}
                for res in results:
                    if res.get("status") != "success":
                        continue

                    doc_type = res.get("document_type", "unknown")
                    ocr_input = res.get("ocr_text") or str(res.get("data", ""))

                    yield {"type": "extraction_started", "filename": res["filename"], "document_type": doc_type}

                    try:
                        final_json = await run_llm_json_mapping(
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

                        yield {"type": "extraction_completed", "filename": res["filename"]}

                    except Exception as e:
                        logger.error(f"[{res['filename']}] LLM Extraction failed: {e}")
                        yield {"type": "extraction_failed", "filename": res["filename"], "error": str(e)}
                        res["status"] = "error"
                        res["error"] = str(e)

                    if "ocr_text" in res:
                        del res["ocr_text"]

        except Exception as e:
            logger.error(f"Llama server or classification/extraction failed: {e}")
            yield {"type": "error", "error": "Classification/Extraction phase failed"}
            return

    # ------------------------------------------------------------------ #
    # PHASE 4: Validation                                                #
    # ------------------------------------------------------------------ #
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

    yield {
        "type": "validation_phase_completed",
        "total_validated": len(validated_documents),
        "total_failed": len(failed_docs)
    }

    # ------------------------------------------------------------------ #
    # PHASE 5: Reconciliation                                            #
    # ------------------------------------------------------------------ #
    yield {"type": "phase_started", "phase": "reconciliation"}
    final_report = build_final_report(validated_documents)
    yield {"type": "reconciliation_completed"}

    yield {
        "type": "completed",
        "result": {
            "documents": validated_documents,
            "failed_documents": failed_docs,
            "decision": final_report
        }
    }