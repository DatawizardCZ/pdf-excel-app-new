"""
Vercel Python Serverless Function: PDF -> Excel converter

Wraps the existing pdf_processor.py module and returns an XLSX file
generated from an uploaded PDF (multipart/form-data, field name "file").

Endpoint: POST /api/process
"""
from __future__ import annotations

import hmac
import io
import os
import sys
import tempfile
import traceback
from pathlib import Path

from flask import Flask, jsonify, request, send_file, send_from_directory

# Ensure project root is importable so we can reuse pdf_processor.py 1:1
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
from pdf_processor import extract_data_from_pdf, get_processor_version

app = Flask(__name__)

XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

# Sdílené heslo pro celou aplikaci. V produkci se nastavuje v Vercel dashboardu
# (Project Settings -> Environment Variables -> APP_PASSWORD). Pokud není
# nastaveno, aplikace běží v "open" režimu (žádné heslo) — užitečné pro lokální
# vývoj. Pro produkci VŽDY nastavte silné heslo.
APP_PASSWORD = os.getenv("APP_PASSWORD", "")


def _has_valid_auth() -> bool:
    """Constant-time porovnání hesla z Authorization: Bearer <heslo> headeru."""
    if not APP_PASSWORD:
        return True  # open mode (no password configured)
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return False
    token = auth[len("Bearer "):]
    return hmac.compare_digest(token, APP_PASSWORD)


@app.before_request
def _enforce_auth():
    """Vyžaduje platné heslo na všech /api/* endpointech kromě /api/auth.
    Statický `/` a další non-API routy projdou bez kontroly (Vercel je beztoho
    servíruje mimo Python funkci)."""
    path = request.path
    if path == "/api/auth":
        return None  # endpoint validates itself
    if not path.startswith("/api/"):
        return None  # only /api/* is gated
    if not _has_valid_auth():
        return jsonify({"error": "Unauthorized", "detail": "Chybí nebo neplatné heslo"}), 401
    return None


@app.route("/api/auth", methods=["GET", "POST"])
def auth():
    """Auth endpoint.

    GET  -> ověří aktuální Authorization header. 200 = ok, 401 = invalid/missing.
            Vrací i `auth_required` aby frontend věděl, jestli má kreslit login.
    POST -> přijme {"password": "..."} v JSON, validuje, vrátí 200/401.
    """
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


@app.route("/api/process", methods=["POST"])
def process_pdf():
    if "file" not in request.files:
        return jsonify({"error": "Žádný soubor v requestu (očekáváno pole 'file')"}), 400

    upload = request.files["file"]
    if not upload or not upload.filename:
        return jsonify({"error": "Soubor bez názvu"}), 400

    if not upload.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Pouze PDF soubory jsou podporovány"}), 400

    tmp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            upload.save(tmp.name)
            tmp_path = Path(tmp.name)

        df = extract_data_from_pdf(tmp_path)

        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Objednávka")
        excel_buffer.seek(0)

        excel_filename = f"{Path(upload.filename).stem}_processed.xlsx"

        return send_file(
            excel_buffer,
            mimetype=XLSX_MIME,
            as_attachment=True,
            download_name=excel_filename,
            max_age=0,
        )
    except Exception as exc:
        return (
            jsonify(
                {
                    "error": "Chyba při zpracování PDF",
                    "detail": str(exc),
                    "trace": traceback.format_exc() if os.getenv("DEBUG_MODE") == "true" else None,
                }
            ),
            500,
        )
    finally:
        if tmp_path is not None:
            try:
                tmp_path.unlink(missing_ok=True)
            except Exception:
                pass


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "ok",
            "processor": get_processor_version(),
        }
    )


# Local development: `python api/process.py` spustí Flask dev server,
# který servíruje i index.html z rootu projektu (Vercel produkčně řeší statický
# obsah jinak — tato větev se v produkci nikdy nespustí).
if __name__ == "__main__":
    @app.route("/")
    def _local_index():
        return send_from_directory(PROJECT_ROOT, "index.html")

    port = int(os.getenv("PORT", "3000"))
    print(f"\n  Darvis PDF Objednávky (local dev) running at: http://localhost:{port}\n")
    app.run(host="127.0.0.1", port=port, debug=True)
