from fastapi.testclient import TestClient
from app.main import app


def test_process_documents_stream(monkeypatch):
    async def fake_process_documents(_):
        yield {"type": "completed", "result": {"ok": True}}

    monkeypatch.setattr("app.api.routes.process_documents", fake_process_documents)

    client = TestClient(app)
    files = {"files": ("test.png", b"img", "image/png")}
    with client.stream("POST", "/process-documents", files=files) as response:
        assert response.status_code == 200
        lines = list(response.iter_lines())
        assert len(lines) == 1
