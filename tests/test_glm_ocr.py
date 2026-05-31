import pytest
from app.services.glm_ocr import run_glm_ocr


class DummyProc:
    def __init__(self, code, out="", err=""):
        self.returncode = code
        self.stdout = out
        self.stderr = err


@pytest.mark.asyncio
async def test_glm_ocr_ok(monkeypatch):
    def fake_run(*args, **kwargs):
        return DummyProc(0, out="ocr text")

    monkeypatch.setattr("app.services.glm_ocr.subprocess.run", fake_run)
    res = await run_glm_ocr(b"img")
    assert res == "ocr text"


@pytest.mark.asyncio
async def test_glm_ocr_fail(monkeypatch):
    def fake_run(*args, **kwargs):
        return DummyProc(1, out="", err="fail")

    monkeypatch.setattr("app.services.glm_ocr.subprocess.run", fake_run)
    res = await run_glm_ocr(b"img")
    assert res == ""
