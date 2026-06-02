import pytest
from app.services.llm_json_mapping import run_llm_json_mapping


class DummyResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


@pytest.mark.asyncio
async def test_llm_json_mapping_ok(monkeypatch):
    def fake_generate(*args, **kwargs):
        payload = {
            "choices": [
                {
                    "message": {
                        "content": '{"extracted_data": {"x": 1}}'
                    }
                }
            ]
        }
        return DummyResponse(payload)

    monkeypatch.setattr("app.services.llm_json_mapping.requests.post", fake_generate)
    res = await run_llm_json_mapping("text", {"x": "number"})
    assert res["extracted_data"]["x"] == 1


@pytest.mark.asyncio
async def test_llm_json_mapping_invalid_json(monkeypatch):
    def fake_generate(*args, **kwargs):
        payload = {
            "choices": [
                {
                    "message": {
                        "content": "not-json"
                    }
                }
            ]
        }
        return DummyResponse(payload)

    monkeypatch.setattr("app.services.llm_json_mapping.requests.post", fake_generate)
    res = await run_llm_json_mapping("text", {"x": "number"})
    assert res["status"] == "error"


@pytest.mark.asyncio
async def test_llm_json_mapping_unreachable(monkeypatch):
    def fake_generate(*args, **kwargs):
        raise RuntimeError("down")

    monkeypatch.setattr("app.services.llm_json_mapping.requests.post", fake_generate)
    res = await run_llm_json_mapping("text", {"x": "number"})
    assert res["status"] == "error"
