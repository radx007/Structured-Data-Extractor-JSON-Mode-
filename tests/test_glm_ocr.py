import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock
from app.services.glm_ocr import run_glm_ocr


@pytest.mark.asyncio
async def test_glm_ocr_ok(monkeypatch):
    # Mock httpx response
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "ocr text"}}]
    }

    # Mock the httpx AsyncClient.post
    async def fake_post(*args, **kwargs):
        return mock_response

    monkeypatch.setattr("httpx.AsyncClient.post", fake_post)
    res = await run_glm_ocr(b"img")
    assert res == "ocr text"


@pytest.mark.asyncio
async def test_glm_ocr_fail(monkeypatch):
    # Simulate connection error
    async def fake_post(*args, **kwargs):
        raise httpx.ConnectError("connection refused")

    monkeypatch.setattr("httpx.AsyncClient.post", fake_post)
    res = await run_glm_ocr(b"img")
    assert res == ""