"""
Vercel Python Serverless Function: jednoduchý auth endpoint.

Endpointy:
- GET  /api/auth  -> ověří hlavičku `Authorization: Bearer <heslo>`
                     (200 = platné, 401 = chybí/neplatné, vrací `auth_required`)
- POST /api/auth  -> přijme {"password": "..."} v JSON, ověří, vrátí 200/401

Sdílené heslo se nastavuje v env variable `APP_PASSWORD` (Vercel dashboard
-> Project Settings -> Environment Variables). Pokud není nastaveno, app
běží v "open" módu — hodí se jen pro lokální dev.

Tato funkce se na Vercelu deployuje jako samostatná lambda — důvod je čistě
provozní: Vercel mapuje URL podle souborů v /api, takže /api/auth musí
existovat jako svůj vlastní soubor (jinak vrátí 404 ještě před tím, než
se k Flasku dostane).
"""
from __future__ import annotations

import hmac
import os

from flask import Flask, jsonify, request

app = Flask(__name__)

APP_PASSWORD = os.getenv("APP_PASSWORD", "")


def _has_valid_auth() -> bool:
    """Constant-time porovnání hesla z `Authorization: Bearer <heslo>` headeru."""
    if not APP_PASSWORD:
        return True
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return False
    token = auth[len("Bearer "):]
    return hmac.compare_digest(token, APP_PASSWORD)


@app.route("/api/auth", methods=["GET", "POST"])
def auth():
    if request.method == "GET":
        if not APP_PASSWORD:
            return jsonify({"ok": True, "auth_required": False}), 200
        if _has_valid_auth():
            return jsonify({"ok": True, "auth_required": True}), 200
        return jsonify({"ok": False, "auth_required": True}), 401

    body = request.get_json(silent=True) or {}
    password = body.get("password", "") or ""
    if not APP_PASSWORD:
        return jsonify({"ok": True, "auth_required": False}), 200
    if not isinstance(password, str) or not password:
        return jsonify({"ok": False}), 401
    if hmac.compare_digest(password, APP_PASSWORD):
        return jsonify({"ok": True, "auth_required": True}), 200
    return jsonify({"ok": False}), 401
