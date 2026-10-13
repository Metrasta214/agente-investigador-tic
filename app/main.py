import secrets
import logging
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from openai import AuthenticationError, RateLimitError, APITimeoutError, APIConnectionError, APIStatusError
from app.core.config import ROOT, Settings
from app.models.investigacion import InvestigacionRequest, InvestigacionResponse
from app.services.investigador_service import InvestigadorService

settings = Settings()
service = InvestigadorService(settings)
app = FastAPI(title="Radar TIC", version="1.0.0")
if settings.cors_origins:
    app.add_middleware(CORSMiddleware, allow_origins=list(settings.cors_origins),
                       allow_methods=["GET", "POST"], allow_headers=["Content-Type", "X-Access-Token"])

@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'"
    if request.url.path.startswith("/api"):
        response.headers["Cache-Control"] = "no-store"
    return response

@app.get("/", include_in_schema=False)
def index():
    return FileResponse(ROOT / "index.html")

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse(ROOT / "assets/favicon.svg", media_type="image/svg+xml")

@app.get("/api/health")
def health():
    return {"ok": True, "configurada": bool(settings.api_key), "modelo": settings.model,
            "acceso_requerido": bool(settings.access_token)}

@app.post("/api/investigar", response_model=InvestigacionResponse)
async def investigar(body: InvestigacionRequest, x_access_token: str = Header(default="")):
    if settings.access_token and not secrets.compare_digest(x_access_token.encode(), settings.access_token.encode()):
        raise HTTPException(401, "Código de acceso incorrecto.")
    try:
        return await service.investigar(body)
    except ValueError as exc:
        raise HTTPException(503, str(exc)) from None
    except AuthenticationError:
        raise HTTPException(502, "OpenAI rechazó la API Key. Revisa la configuración del servidor.") from None
    except RateLimitError:
        raise HTTPException(429, "Límite o saldo de OpenAI insuficiente. Revisa tu proyecto y vuelve a intentar.") from None
    except APITimeoutError:
        raise HTTPException(504, "La investigación tardó demasiado. Prueba el modo rápido.") from None
    except APIConnectionError:
        raise HTTPException(502, "No se pudo conectar con OpenAI. Revisa la conexión del servidor.") from None
    except APIStatusError:
        raise HTTPException(502, "OpenAI rechazó la solicitud. Verifica acceso al modelo y compatibilidad con Web Search.") from None
    except Exception as exc:
        logging.error("Error de investigación: %s", type(exc).__name__)
        raise HTTPException(500, "Ocurrió un error interno. Revisa el servidor.") from None

app.mount("/assets", StaticFiles(directory=ROOT / "assets"), name="assets")

