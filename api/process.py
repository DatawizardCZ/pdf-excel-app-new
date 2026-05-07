"""
Vercel Python Serverless Function: PDF -> Excel converter

Wraps the existing pdf_processor.py module and returns an XLSX file
generated from an uploaded PDF (multipart/form-data, field name "file").

Endpoint: POST /api/process
"""
from __future__ import annotations

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
