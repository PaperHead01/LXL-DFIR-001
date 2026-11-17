#!/usr/bin/env python3
"""
LXL-DFIR-001 — E-008 source: simulated cloud file-sharing service
"NimbusShare" — a fictional provider-side file sharing service.

--------------------------------------------------------------------------
WHAT THIS IS, AND WHY IT IS NOT A FAKE
--------------------------------------------------------------------------
This is NOT part of the examined machine. It stands in for the records a
cloud provider would hold — the kind of material you obtain from a third
party by legal process. Because it actually runs, the records it produces
are genuine: real HTTP requests, real timestamps, real bytes received,
real hashes of real uploaded files.

That distinction is the whole point of E-008. A generated CSV of "cloud
logs" proves nothing. This proves the transaction happened.

--------------------------------------------------------------------------
WHAT IT PRODUCES  (acquired as E-008)
--------------------------------------------------------------------------
  logs/access.jsonl   one JSON object per HTTP request
  uploads/            the files actually received, named <utc-stamp>_<name>

Log fields, and why each one earns its place:

  ts_utc / ts_ist   Two time bases. Every timestamp in this case carries both,
                    because the authorities you are reporting to count in IST
                    and the artefacts record in UTC.
  remote_addr       Which host made the request — the examined VM's address.
  method, path      What was asked for. The path shows the navigation flow.
  status            The server's own response. 200 means it succeeded.
  bytes_in          Size of the request body. Corroborates the packet capture
                    independently: the PCAP says how many bytes crossed the
                    wire, this says how many arrived.
  referer           What page the request came from. Proves the upload followed
                    the upload form rather than being scripted directly.
  user_agent        Which browser, which version.
  sha256            Hash of the bytes as received. This is the link that ties
                    E-008 to the endpoint copy (E-001) and the USB copy (E-006).

--------------------------------------------------------------------------
DELIBERATE LIMITATIONS — DOCUMENT THESE, DO NOT HIDE THEM
--------------------------------------------------------------------------
  1. HTTP, not HTTPS. A production provider uses TLS. Against TLS you would
     see only connection metadata, byte volume and timing. This service is
     therefore a BEST CASE for visibility, and the report must say so:

       "The simulated cloud service operated over HTTP, permitting full
        transaction-level visibility. Production cloud services employ TLS,
        in which case analysis is limited to connection metadata and byte
        volume. The cloud findings therefore represent a best case for upload
        attribution and should not be read as typical of live cloud
        investigation."

  2. The login accepts any credentials. Authentication is not what is being
     examined here; the upload transaction is. Do not read the login record
     as proof of identity — that would be exactly the attribution error this
     case is designed to punish.

  3. The clock is this Mac's clock. Record its offset from a trusted time
     source at the start and end of the incident, and note it in the
     examination notes.

--------------------------------------------------------------------------
RUN IT
--------------------------------------------------------------------------
  pip3 install flask
  python3 nimbusshare.py

  Then bind the hostname inside the VM (Runbook, Build phase):
    C:\\Windows\\System32\\drivers\\etc\\hosts
    <HOST_IP_FROM_VM>   nimbusshare.example

  Find <HOST_IP_FROM_VM> by running `ipconfig` inside the VM — it is the
  Default Gateway of the NAT adapter. That gateway is the Mac.
"""

import hashlib
import json
import os
import secrets
from datetime import datetime, timedelta, timezone

from flask import (
    Flask,
    g,
    redirect,
    render_template_string,
    request,
    session,
    url_for,
)

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------
IST = timezone(timedelta(hours=5, minutes=30))
ROOT = os.path.dirname(os.path.abspath(__file__))

# Where evidence is written.
#
# DEFAULT IS DELIBERATELY OUTSIDE THE REPOSITORY TREE. The uploads directory
# holds the files the subject exfiltrated, and the access log holds the record
# of the transaction. Both are evidence. Both would be committed and published
# if they lived beside the source and the repository were pushed.
#
# Override with --data-dir or the LXL_DATA_DIR environment variable.
def _default_data_dir():
    # Look for the case tree two levels up from the tool, if it exists.
    for candidate in (
        os.environ.get("LXL_DATA_DIR"),
        os.path.join(os.path.dirname(os.path.dirname(ROOT)),
                     "03_evidence", "cloud"),
    ):
        if candidate:
            return candidate
    return os.path.join(ROOT, "cloud_evidence")

DATA_DIR = _default_data_dir()
UPLOADS = os.path.join(DATA_DIR, "uploads")
LOGS = os.path.join(DATA_DIR, "logs")
ACCESS_LOG = os.path.join(LOGS, "access.jsonl")

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config["MAX_CONTENT_LENGTH"] = 512 * 1024 * 1024  # 512 MB


# --------------------------------------------------------------------------
# Logging
# --------------------------------------------------------------------------
def log_event(**fields):
    """Append one JSON record. One line per request, never rewritten."""
    now = datetime.now(timezone.utc)
    record = {"ts_utc": now.isoformat(), "ts_ist": now.astimezone(IST).isoformat()}
    record.update(fields)
    with open(ACCESS_LOG, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


@app.before_request
def _reset_extra():
    g.extra = {}


@app.after_request
def _log_request(response):
    """Log every request that reaches the application, including 404s."""
    merged = {
        "remote_addr": request.remote_addr,
        "method": request.method,
        "path": request.path,
        "status": response.status_code,
        "bytes_in": request.content_length or 0,
        "referer": request.headers.get("Referer"),
        "user_agent": request.headers.get("User-Agent"),
    }
    merged.update(getattr(g, "extra", {}))
    log_event(**merged)
    return response


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------
BASE_CSS = """
<style>
  :root { --ink:#12151a; --muted:#5b6472; --line:#e2e6ec; --accent:#1e5eff; }
  * { box-sizing:border-box; }
  body { margin:0; font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
         color:var(--ink); background:#f7f8fa; }
  .bar { background:#fff; border-bottom:1px solid var(--line); padding:14px 24px;
         display:flex; align-items:center; gap:10px; }
  .dot { width:22px; height:22px; border-radius:6px; background:var(--accent); }
  .bar b { font-size:16px; letter-spacing:-.2px; }
  .wrap { max-width:560px; margin:64px auto; padding:0 24px; }
  .card { background:#fff; border:1px solid var(--line); border-radius:12px; padding:28px; }
  h1 { font-size:20px; margin:0 0 6px; letter-spacing:-.3px; }
  p.sub { color:var(--muted); margin:0 0 22px; font-size:14px; }
  label { display:block; font-size:13px; font-weight:600; margin:16px 0 6px; }
  input[type=text], input[type=password], input[type=file] {
    width:100%; padding:10px 12px; border:1px solid var(--line); border-radius:8px;
    font:inherit; background:#fff; }
  button { margin-top:22px; width:100%; padding:11px; border:0; border-radius:8px;
           background:var(--accent); color:#fff; font:inherit; font-weight:600; cursor:pointer; }
  button:hover { background:#1749cc; }
  .note { margin-top:18px; font-size:12px; color:var(--muted); text-align:center; }
  .ok { background:#eaf6ee; border:1px solid #bfe3cb; color:#1c6b37; padding:12px 14px;
        border-radius:8px; font-size:14px; margin-bottom:18px; }
  code { background:#f0f2f5; padding:2px 6px; border-radius:4px; font-size:13px; }
  .foot { text-align:center; color:var(--muted); font-size:12px; margin-top:28px; }
</style>
"""

LOGIN_TEMPLATE = (
    BASE_CSS
    + """
<div class="bar"><div class="dot"></div><b>NimbusShare</b></div>
<div class="wrap">
  <div class="card">
    <h1>Sign in to NimbusShare</h1>
    <p class="sub">Share large files securely with anyone.</p>
    <form method="post" action="/login">
      <label for="u">Email address</label>
      <input type="text" id="u" name="username" autocomplete="off" autofocus>
      <label for="p">Password</label>
      <input type="password" id="p" name="password">
      <button type="submit">Sign in</button>
    </form>
    <div class="note">Demo environment &mdash; no real authentication</div>
  </div>
  <div class="foot">nimbusshare.example &middot; fictional provider for LXL-DFIR-001</div>
</div>
"""
)

UPLOAD_TEMPLATE = (
    BASE_CSS
    + """
<div class="bar"><div class="dot"></div><b>NimbusShare</b></div>
<div class="wrap">
  <div class="card">
    {% if uploaded %}
    <div class="ok">Upload complete &mdash; <strong>{{ uploaded }}</strong></div>
    {% endif %}
    <h1>Upload a file</h1>
    <p class="sub">Files up to 512 MB. Shared links expire in 7 days.</p>
    <form method="post" action="/upload" enctype="multipart/form-data">
      <label for="f">Select file</label>
      <input type="file" id="f" name="file" required>
      <button type="submit">Upload</button>
    </form>
    <div class="note">Signed in as {{ user }}</div>
  </div>
  <div class="foot">nimbusshare.example &middot; fictional provider for LXL-DFIR-001</div>
</div>
"""
)


# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------
@app.route("/")
def index():
    if session.get("user"):
        return redirect(url_for("upload_form"))
    return render_template_string(LOGIN_TEMPLATE)


@app.route("/login", methods=["POST"])
def login():
    session["user"] = request.form.get("username", "").strip() or "unknown"
    return redirect(url_for("upload_form"))


@app.route("/upload", methods=["GET"])
def upload_form():
    if not session.get("user"):
        return redirect(url_for("index"))
    return render_template_string(
        UPLOAD_TEMPLATE, user=session["user"], uploaded=None
    )


@app.route("/upload", methods=["POST"])
def upload():
    if not session.get("user"):
        return redirect(url_for("index"))

    incoming = request.files.get("file")
    if incoming is None or not incoming.filename:
        return render_template_string(
            UPLOAD_TEMPLATE, user=session["user"], uploaded=None
        ), 400

    original = os.path.basename(incoming.filename)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    stored_as = f"{stamp}_{original}"
    destination = os.path.join(UPLOADS, stored_as)

    digest = hashlib.sha256()
    total = 0
    with open(destination, "wb") as out:
        while True:
            chunk = incoming.stream.read(1 << 20)
            if not chunk:
                break
            digest.update(chunk)
            out.write(chunk)
            total += len(chunk)

    # Fields logged in addition to the standard request record.
    # sha256 is the link to the endpoint copy and the USB copy.
    g.extra = {
        "filename": original,
        "stored_as": stored_as,
        "sha256": digest.hexdigest(),
        "bytes_stored": total,
    }

    return render_template_string(
        UPLOAD_TEMPLATE, user=session["user"], uploaded=original
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=None,
                    help="directory for uploads/ and logs/ (outside the repo)")
    ap.add_argument("--port", type=int, default=8080)
    args = ap.parse_args()

    if args.data_dir:
        DATA_DIR = os.path.abspath(args.data_dir)
        UPLOADS = os.path.join(DATA_DIR, "uploads")
        LOGS = os.path.join(DATA_DIR, "logs")
        ACCESS_LOG = os.path.join(LOGS, "access.jsonl")

    os.makedirs(UPLOADS, exist_ok=True)
    os.makedirs(LOGS, exist_ok=True)

    print("NimbusShare — simulated provider for LXL-DFIR-001")
    print(f"  uploads : {UPLOADS}")
    print(f"  log     : {ACCESS_LOG}")
    print(f"  binding : 0.0.0.0:{args.port}")
    print()
    print("  Reach it from the VM at http://<NAT gateway IP>:8080")
    print("  (run `ipconfig` in the VM — the Default Gateway is this Mac)")
    print()
    app.run(host="0.0.0.0", port=args.port, debug=False)
