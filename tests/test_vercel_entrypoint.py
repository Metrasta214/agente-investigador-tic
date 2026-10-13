"""Exercise the deployment import in a fresh process without provider access."""
import os
from pathlib import Path
import subprocess
import sys


def test_vercel_entrypoint_starts_without_provider_access():
    root = Path(__file__).resolve().parents[1]
    code = """
import importlib
import socket
import tomllib
from unittest.mock import patch

def forbidden(*args, **kwargs):
    raise AssertionError('External network access is forbidden in this test')

with patch.object(socket.socket, 'connect', forbidden), patch.object(socket.socket, 'connect_ex', forbidden):
    import openai
    from fastapi.testclient import TestClient
    with patch.object(openai, 'AsyncOpenAI', forbidden), patch.object(openai, 'OpenAI', forbidden):
        with open('pyproject.toml', 'rb') as config:
            entrypoint = tomllib.load(config)['tool']['vercel']['entrypoint']
        module, name = entrypoint.split(':')
        application = getattr(importlib.import_module(module), name)
        with TestClient(application) as client:
            response = client.get('/api/health')
            assert response.status_code == 200
            assert response.json()['ok'] is True
            assert response.json()['acceso_requerido'] is True
            for path in ('/', '/assets/css/styles.css', '/assets/js/app.js', '/docs'):
                assert client.get(path).status_code == 200, path
"""
    env = {**os.environ, "VERCEL": "1", "OPENAI_API_KEY": "", "APP_ACCESS_TOKEN": "",
           "PYTHON_DOTENV_DISABLED": "1"}
    result = subprocess.run([sys.executable, "-c", code], cwd=root, env=env,
                            capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr
