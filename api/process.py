"""
Vercel Python Serverless Function: PDF -> Excel converter.

Wraps `pdf_processor.py` 1:1 a vrací XLSX vytvořený z nahraného PDF
(multipart/form-data, pole `file`).

Endpoint: POST /api/process

Auth: vyžaduje `Authorization: Bearer <APP_PASSWORD>` pokud je APP_PASSWORD
nastaveno. Login flow řeší samostatná funkce v `api/auth.py`.
"""
from __future__ import annotations

import hmac
import io
import os
import sys
import tempfile
import traceback
from pathlib import Path

from flask import Flask, jsonify, request, send_file

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
from pdf_processor import extract_data_from_pdf

app = Flask(__name__)

XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

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


@app.before_request
def _enforce_auth():
    if not _has_valid_auth():
        return jsonify({"error": "Unauthorized", "detail": "Chybí nebo neplatné heslo"}), 401
    return None


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
