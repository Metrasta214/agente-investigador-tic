"""Comprobaciones HTTP y de secretos sin llamar a OpenAI.

Ejecutar desde la raíz: python scripts/verificar_local.py --url http://127.0.0.1:5001
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import httpx
from app.core.config import Settings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:5000")
    args = parser.parse_args()
    settings = Settings()
    sensitive = [value.encode() for value in (settings.api_key, settings.access_token) if value]
    git = ["git", "-c", f"safe.directory={ROOT}", "-C", str(ROOT)]
    tracked = subprocess.check_output(git + ["ls-files", "-z"]).decode().split("\0")
    leaks = [name for name in tracked if name and any(value in (ROOT / name).read_bytes() for value in sensitive)]
    assert not leaks, f"Secretos en archivos versionados: {leaks}"
    assert ".env" not in tracked
    subprocess.run(git + ["check-ignore", "-q", ".env"], check=True)
    # Revisa los blobs de todos los commits sin imprimir su contenido.
    objects = subprocess.check_output(git + ["rev-list", "--objects", "--all"]).decode().splitlines()
    for item in objects:
        oid = item.split(" ", 1)[0]
        kind = subprocess.check_output(git + ["cat-file", "-t", oid]).strip()
        if kind == b"blob":
            data = subprocess.check_output(git + ["cat-file", "blob", oid])
            assert not any(value in data for value in sensitive), "Secreto en historial Git"
    checks = []
    with httpx.Client(base_url=args.url, timeout=15, trust_env=False) as client:
        for path in ("/", "/api/health", "/assets/js/app.js", "/assets/js/api.js",
                     "/assets/js/config.js", "/assets/css/styles.css", "/favicon.ico", "/docs", "/openapi.json"):
            response = client.get(path)
            assert response.status_code == 200, (path, response.status_code)
            assert not any(value in response.content for value in sensitive), f"Secreto en {path}"
            checks.append({"ruta": path, "estado": response.status_code, "sin_secretos": True})
        for path in ("/.env", "/.git/config", "/app/core/config.py", "/requirements.txt",
                     "/assets/../.env", "/assets/%2e%2e/.env"):
            response = client.get(path)
            assert response.status_code == 404, (path, response.status_code)
            checks.append({"ruta": path, "estado": response.status_code})
        health = client.get("/api/health").json()
        response = client.post("/api/investigar", json={"pregunta": "   ", "modo": "otro"})
        assert response.status_code == 422
        if health["acceso_requerido"]:
            response = client.post("/api/investigar", json={"pregunta": "Pregunta de control", "modo": "rapido"})
            assert response.status_code == 401
        checks.append({"validacion": 422, "acceso_requerido": health["acceso_requerido"]})
    report = {"fecha_utc": datetime.now(timezone.utc).isoformat(),
              "url": args.url, "modelo": settings.model,
              "archivos_git_revisados": len([p for p in tracked if p]),
              "historial_sin_secretos": True, "consultas_openai": 0,
              "comprobaciones": checks, "navegador": "No disponible: revisión visual y capturas pendientes"}
    directory = ROOT / "docs/evidencias"
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "verificacion-local.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"ok": True, "rutas_revisadas": len(checks), "consultas_openai": 0}))


if __name__ == "__main__":
    main()
