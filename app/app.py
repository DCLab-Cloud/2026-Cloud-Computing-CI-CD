import os
import socket
from html import escape
from pathlib import Path

from flask import Flask, jsonify

app = Flask(__name__)
VERSION_FILE = Path(__file__).with_name("version.txt")
MESSAGE = "Hello CI/CD!"


def version_info():
    return {
        "version": VERSION_FILE.read_text(encoding="utf-8").strip(),
        "source_commit": os.environ.get("APP_COMMIT", "local"),
        "hostname": socket.gethostname(),
    }


@app.get("/")
def index():
    info = version_info()
    return (
        '<!doctype html><html lang="ko"><meta charset="utf-8">'
        f"<h1>{escape(MESSAGE)}</h1>"
        f"<p>Version: {escape(info['version'])}</p>"
        f"<p>Commit: {escape(info['source_commit'])}</p>"
        f"<p>Pod: {escape(info['hostname'])}</p></html>"
    )


@app.get("/healthz")
def healthz():
    return jsonify(status="ok")


@app.get("/version")
def version():
    return jsonify(version_info())
