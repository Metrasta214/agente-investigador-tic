"""Publica las ramas existentes usando Git Credential Manager, sin mostrar tokens.

python scripts/publicar_github.py --usuario USUARIO --publicar
La cuenta debe coincidir con la conexión GitHub comprobada por el propietario.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--usuario", required=True)
    parser.add_argument("--publicar", action="store_true")
    args = parser.parse_args()
    git = ["git", "-c", f"safe.directory={ROOT}", "-C", str(ROOT)]
    env = {**os.environ, "GCM_INTERACTIVE": "Never", "GIT_TERMINAL_PROMPT": "0"}
    credential = subprocess.run(git + ["credential", "fill"],
        input="protocol=https\nhost=github.com\n\n", text=True,
        capture_output=True, env=env, timeout=30)
    fields = dict(line.split("=", 1) for line in credential.stdout.splitlines() if "=" in line)
    token = fields.get("password")
    if not token:
        raise SystemExit("Git no tiene credenciales de GitHub. Inicia sesión en Git Credential Manager.")

    def api(path, body=None):
        request = urllib.request.Request("https://api.github.com" + path,
            data=None if body is None else json.dumps(body).encode(),
            headers={"Authorization": "Bearer " + token, "Accept": "application/vnd.github+json",
                     "X-GitHub-Api-Version": "2026-03-10", "User-Agent": "Radar-TIC-practica"})
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)

    user = api("/user")["login"]
    if user.casefold() != args.usuario.casefold():
        raise SystemExit("La cuenta de Git no coincide con la cuenta esperada. No se publicó nada.")
    name = "agente-investigador-tic"
    url = f"https://github.com/{user}/{name}.git"
    existing_remote = subprocess.run(git + ["remote", "get-url", "origin"], capture_output=True, text=True)
    if existing_remote.returncode == 0 and existing_remote.stdout.strip().removesuffix(".git").lower() != url.removesuffix(".git").lower():
        raise SystemExit("El remoto existente apunta a otro repositorio. Requiere revisión.")
    if not args.publicar:
        print(json.dumps({"cuenta": user, "destino": url, "publicado": False}))
        return
    try:
        repo = api(f"/repos/{user}/{name}")
        if repo["private"]:
            raise SystemExit("El repositorio existente es privado; no se modificó su visibilidad.")
        branches = api(f"/repos/{user}/{name}/branches")
        if branches and existing_remote.returncode != 0:
            raise SystemExit("El repositorio existente contiene ramas. Hay que revisar su contenido antes de conectarlo.")
    except urllib.error.HTTPError as error:
        if error.code != 404:
            raise SystemExit(f"GitHub rechazó la consulta: HTTP {error.code}.") from None
        repo = api("/user/repos", {"name": name, "private": False,
            "description": "Radar TIC: práctica 2.2, agente investigador con FastAPI, Responses API y Web Search"})
    if existing_remote.returncode != 0:
        subprocess.run(git + ["remote", "add", "origin", url], check=True)
    subprocess.run(git + ["push", "-u", "origin", "main", "feature/agente-investigador"], env=env, check=True)
    print(json.dumps({"cuenta": user, "repositorio": repo["html_url"], "publicado": True}))


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as error:
        raise SystemExit(f"GitHub rechazó la operación: HTTP {error.code}.") from None
    except urllib.error.URLError:
        raise SystemExit("No se pudo conectar con GitHub.") from None
