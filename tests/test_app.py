import asyncio
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from app import main
from app.core.config import Settings
from app.models.investigacion import InvestigacionRequest
from app.services import investigador_service as module
from app.services.investigador_service import InvestigadorService

client = TestClient(main.app)
BODY = {"pregunta": "¿Qué es una red de sensores?", "modo": "rapido", "usar_web": True}

def response_data():
    return {"status": "completed", "output": [
        {"type": "web_search_call", "status": "completed"},
        {"type": "message", "content": [{"type": "output_text", "text": "Resumen\nDatos [1]",
          "annotations": [{"type": "url_citation", "start_index": 14, "end_index": 17,
                           "title": "Fuente", "url": "https://example.org"}]}]}]}

def test_frontend_and_private_files():
    assert client.get("/").status_code == 200
    for path in ("/assets/js/app.js", "/assets/css/styles.css", "/favicon.ico"):
        assert client.get(path).status_code == 200
    for path in ("/.env", "/app/core/config.py", "/requirements.txt"):
        assert client.get(path).status_code == 404
    assert "api_key" not in client.get("/api/health").json()

def test_validation():
    for body in ({**BODY, "pregunta": "   "}, {**BODY, "modo": "otro"}, {**BODY, "pregunta": "a"*2001}):
        assert client.post("/api/investigar", json=body).status_code == 422

def test_missing_key(monkeypatch):
    monkeypatch.setattr(main, "settings", Settings(api_key="", access_token=""))
    monkeypatch.setattr(main, "service", InvestigadorService(Settings(api_key="")))
    result = client.post("/api/investigar", json=BODY)
    assert result.status_code == 503
    assert "OPENAI_API_KEY" in result.json()["detail"]

def test_access_and_success(monkeypatch):
    service = InvestigadorService(Settings(api_key="fake"))
    expected = service.procesar(response_data(), InvestigacionRequest(**BODY), "2026-10-12T00:00:00Z")
    monkeypatch.setattr(main, "settings", Settings(api_key="fake", access_token="secret-test"))
    monkeypatch.setattr(main.service, "investigar", AsyncMock(return_value=expected))
    assert client.post("/api/investigar", json=BODY).status_code == 401
    result = client.post("/api/investigar", json=BODY, headers={"X-Access-Token":"secret-test"})
    assert result.status_code == 200
    assert result.json()["fuentes"][0]["url"] == "https://example.org"

def test_safe_sources_and_incomplete():
    data = response_data()
    data["status"] = "incomplete"
    data["output"][1]["content"][0]["annotations"][0]["url"] = "javascript:alert(1)"
    result = InvestigadorService(Settings()).procesar(data, InvestigacionRequest(**BODY), "now")
    assert result.fuentes == []
    assert result.avisos

def test_web_toggle_provider_contract(monkeypatch):
    calls = []
    class Response:
        def model_dump(self): return response_data()
    class FakeClient:
        def __init__(self, **kwargs): self.responses = self
        async def __aenter__(self): return self
        async def __aexit__(self, *args): pass
        async def create(self, **kwargs):
            calls.append(kwargs)
            return Response()
    monkeypatch.setattr(module, "AsyncOpenAI", FakeClient)
    service = InvestigadorService(Settings(api_key="fake"))
    for web in (False, True):
        asyncio.run(service.investigar(InvestigacionRequest(**{**BODY, "usar_web": web})))
    assert "tools" not in calls[0]
    assert calls[1]["tools"] == [{"type": "web_search"}]
    assert calls[1]["tool_choice"] == "required"
    assert calls[1]["max_tool_calls"] == 3
    assert calls[0]["input"] == calls[1]["input"]

def test_docs_policy_and_nonce():
    import re
    page = client.get("/docs")
    nonce = re.search(r'<script nonce="([^"]+)"', page.text).group(1)
    assert f"'nonce-{nonce}'" in page.headers["Content-Security-Policy"]
    assert "https://cdn.jsdelivr.net" in page.headers["Content-Security-Policy"]
    assert "https://cdn.jsdelivr.net" not in client.get("/").headers["Content-Security-Policy"]
    assert client.get("/openapi.json").status_code == 200

def test_provider_failure_does_not_expose_secret(monkeypatch):
    monkeypatch.setattr(main, "settings", Settings(api_key="private-test", access_token=""))
    monkeypatch.setattr(main.service, "investigar", AsyncMock(side_effect=RuntimeError("private-test")))
    result = client.post("/api/investigar", json=BODY)
    assert result.status_code == 500
    assert "private-test" not in result.text

def test_usage_and_tool_confirmation():
    data = response_data()
    data["output"][0]["status"] = "failed"
    data["usage"] = {"input_tokens": 120, "output_tokens": 30, "total_tokens": 150,
                     "output_tokens_details": {"reasoning_tokens": 10}}
    result = InvestigadorService(Settings()).procesar(data, InvestigacionRequest(**BODY), "now")
    assert result.web_utilizada is False
    assert result.web_llamadas == 1
    assert result.tokens == {"input_tokens": 120, "output_tokens": 30, "total_tokens": 150}

def test_vercel_requires_separate_access_code(monkeypatch):
    provider = AsyncMock()
    monkeypatch.setattr(main.service, "investigar", provider)
    for settings in (Settings(api_key="private-test", access_token="", vercel=True),
                     Settings(api_key="private-test", access_token="private-test", vercel=True)):
        monkeypatch.setattr(main, "settings", settings)
        assert client.post("/api/investigar", json=BODY).status_code == 503
        assert client.get("/api/health").json()["acceso_requerido"] is True
    provider.assert_not_called()
