import pytest
from types import SimpleNamespace
from app.pipeline import document_pipeline as dp


class DummyUploadFile:
    def __init__(self, filename, content_type, content):
        self.filename = filename
        self.content_type = content_type
        self._content = content

    async def read(self):
        return self._content


@pytest.mark.asyncio
async def test_process_documents_non_image(monkeypatch):
    monkeypatch.setattr(dp, "build_final_report", lambda docs: {"status": "approved"})

    f = DummyUploadFile("a.txt", "text/plain", b"x")
    events = [e async for e in dp.process_documents([f])]
    assert events[0]["type"] == "error"


@pytest.mark.asyncio
async def test_process_documents_success(monkeypatch, invoice_doc):
    async def fake_ocr(_):
        return "ocr text"

    async def fake_llm(*args, **kwargs):
        return {"extracted_data": invoice_doc["extracted_data"]}

    def fake_validate(doc):
        return {"status": "success", "data": doc}

    monkeypatch.setattr("app.services.llama_server.LlamaServer.start", lambda self: None)
    monkeypatch.setattr("app.services.llama_server.LlamaServer.wait_until_ready", lambda self: True)
    monkeypatch.setattr("app.services.llama_server.LlamaServer.stop", lambda self: None)

    monkeypatch.setattr(dp, "run_glm_ocr", fake_ocr)
    monkeypatch.setattr(dp, "run_llm_json_mapping", fake_llm)
    monkeypatch.setattr(dp, "validate_document", fake_validate)
    monkeypatch.setattr(dp, "build_final_report", lambda docs: {"status": "approved"})
    monkeypatch.setattr(dp, "router", SimpleNamespace(classify_documents=lambda x: {"a.png": "invoice"}))

    f = DummyUploadFile("a.png", "image/png", b"x")
    events = [e async for e in dp.process_documents([f])]
    types = [e["type"] for e in events]
    assert "completed" in types
    assert "error" not in types
