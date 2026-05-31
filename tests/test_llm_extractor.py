import pytest
from app.services.llm_extractor import run_llm_extraction


@pytest.mark.asyncio
async def test_llm_extraction_ok(monkeypatch):
    def fake_generate(*args, **kwargs):
        return {"response": '{"extracted_data": {"x": 1}}'}

    monkeypatch.setattr("app.services.llm_extractor.ollama.generate", fake_generate)
    res = await run_llm_extraction("text", {"x": "number"})
    assert res["extracted_data"]["x"] == 1


@pytest.mark.asyncio
async def test_llm_extraction_invalid_json(monkeypatch):
    def fake_generate(*args, **kwargs):
        return {"response": "not-json"}

    monkeypatch.setattr("app.services.llm_extractor.ollama.generate", fake_generate)
    res = await run_llm_extraction("text", {"x": "number"})
    assert res["status"] == "error"


@pytest.mark.asyncio
async def test_llm_extraction_unreachable(monkeypatch):
    def fake_generate(*args, **kwargs):
        raise RuntimeError("down")

    monkeypatch.setattr("app.services.llm_extractor.ollama.generate", fake_generate)
    res = await run_llm_extraction("text", {"x": "number"})
    assert res["status"] == "error"
