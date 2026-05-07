"""
Lokální development server.

Vercel deployuje každý soubor v `api/` jako samostatnou serverless funkci
podle názvu souboru (např. `/api/auth` -> `api/auth.py`). Lokálně tu
strukturu emulujeme jediným Flask serverem, který:

- servíruje `index.html` na `/`,
- registruje routy z `api/process.py` (PDF -> XLSX, auth-gated),
- registruje routy z `api/auth.py` (login endpoint),
- sdílí port (default 3000), takže frontend volá `/api/...` stejně jako v produkci.

Spuštění:

    python dev_server.py

Volitelně lze nastavit env vars:

- APP_PASSWORD : sdílené heslo pro login (prázdné = open mode)
- DEBUG_MODE   : "true" zapne podrobné error traces v JSON odpovědi
- PORT         : port (default 3000)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from flask import Flask, send_from_directory

from api.auth import app as auth_app
from api.process import _enforce_auth, app as process_app

dev_app = Flask(__name__)


@dev_app.route("/")
def index():
    return send_from_directory(PROJECT_ROOT, "index.html")


def _copy_routes(src: Flask, dst: Flask) -> None:
    """Přeregistruje URL pravidla zdrojové Flask app na cílovou app."""
    for rule in src.url_map.iter_rules():
        if rule.endpoint == "static":
            continue
        view_func = src.view_functions[rule.endpoint]
        methods = list(rule.methods - {"HEAD", "OPTIONS"}) if rule.methods else None
        dst.add_url_rule(
            rule.rule,
            f"{src.name}__{rule.endpoint}",
            view_func,
            methods=methods,
        )


_copy_routes(process_app, dev_app)
_copy_routes(auth_app, dev_app)

# Auth gate z process.py musí běžet i v dev serveru — ale pouze pro /api/process
# (auth endpoint si validaci řeší sám interně).
@dev_app.before_request
def _dev_enforce_auth():
    from flask import request
    if request.path == "/api/process":
        return _enforce_auth()
    return None


if __name__ == "__main__":
    port = int(os.getenv("PORT", "3000"))
    print(f"\n  Darvis PDF Objednávky (local dev) → http://localhost:{port}\n")
    dev_app.run(host="127.0.0.1", port=port, debug=True)
