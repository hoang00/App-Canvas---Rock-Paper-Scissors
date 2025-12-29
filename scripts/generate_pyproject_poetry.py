"""Generate a pyproject.toml for Poetry from requirements.in

- Puts small runtime set in [tool.poetry.dependencies]
- Puts the rest into [tool.poetry.dev-dependencies]

Adjust the RUNTIME_DEPS set below if you'd like a different split.
"""
import tomllib
from pathlib import Path

RUNTIME_DEPS = {"fastapi","uvicorn","httpx","pydantic","python-dotenv","requests"}

req_in = Path('requirements.in')
if not req_in.exists():
    raise SystemExit('requirements.in not found')

pkgs = [line.strip() for line in req_in.read_text().splitlines() if line.strip() and not line.strip().startswith('#')]

runtime = sorted([p for p in pkgs if p in RUNTIME_DEPS])
dev = sorted([p for p in pkgs if p not in RUNTIME_DEPS])

pyproject = []
pyproject.append('[tool.poetry]')
pyproject.append('name = "app-canvas-rock-paper-scissors"')
pyproject.append('version = "0.1.0"')
pyproject.append('description = "Benchling App Canvas: Rock-Paper-Scissors (FastAPI)"')
pyproject.append('authors = ["Your Name <you@example.com>"]')
pyproject.append('readme = "README.md"')
pyproject.append('license = "MIT"')
pyproject.append('')
pyproject.append('[tool.poetry.dependencies]')
pyproject.append('python = "^3.11"')
for p in runtime:
    pyproject.append(f'"{p}" = "*"')
pyproject.append('')
pyproject.append('[tool.poetry.dev-dependencies]')
pyproject.append('# All other top-level packages from requirements.in are listed here as dev deps')
for p in dev:
    pyproject.append(f'"{p}" = "*"')
pyproject.append('')
pyproject.append('[build-system]')
pyproject.append('requires = ["poetry-core>=1.0.0"]')
pyproject.append('build-backend = "poetry.core.masonry.api"')

Path('pyproject.toml').write_text('\n'.join(pyproject))
print('wrote pyproject.toml with', len(runtime), 'runtime deps and', len(dev), 'dev deps')
