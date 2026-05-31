import json
from app.services.classifier import DocumentRouter


class DummyResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


def test_classify_empty():
    router = DocumentRouter()
    assert router.classify_documents({}) == {}


def test_classify_ok(monkeypatch):
    def fake_post(*args, **kwargs):
        payload = {"response": json.dumps({"a.png": "invoice"})}
        return DummyResponse(payload)

    monkeypatch.setattr("app.services.classifier.requests.post", fake_post)
    router = DocumentRouter()
    res = router.classify_documents({"a.png": "text"})
    assert res["a.png"] == "invoice"


def test_classify_error(monkeypatch):
    def fake_post(*args, **kwargs):
        raise RuntimeError("fail")

    monkeypatch.setattr("app.services.classifier.requests.post", fake_post)
    router = DocumentRouter()
    res = router.classify_documents({"a.png": "text"})
    assert res["a.png"] == "unknown"
