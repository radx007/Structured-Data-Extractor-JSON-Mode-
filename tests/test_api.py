from fastapi.testclient import TestClient
from pytest import MonkeyPatch
from app.main import app


def test_process_documents_stream(monkeypatch: MonkeyPatch):
    async def fake_process_documents(_):
        yield {"type": "completed", "result": {"ok": True}}

    monkeypatch.setattr("app.api.routes.process_documents", fake_process_documents)

    client = TestClient(app)
    files = [
        ("files", ("test1.png", b"img1", "image/png")),
        ("files", ("test2.png", b"img2", "image/png")),
        ("files", ("test3.png", b"img3", "image/png")),
        ("files", ("test4.png", b"img4", "image/png")),
    ]
    with client.stream("POST", "/process-documents", files=files) as response:
        assert response.status_code == 200
        lines = list(response.iter_lines())
        assert len(lines) == 1
