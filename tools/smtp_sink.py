#!/usr/bin/env python3
"""
LXL-DFIR-001 — SMTP sink for the simulated Asterion mail environment.

WHAT THIS IS
------------
A minimal SMTP server that accepts mail, writes the raw message to disk, and
appends one JSON line per transaction to a log.

WHY IT EXISTS
-------------
The case requires a Sent-folder record in Thunderbird (Q11: was data transmitted
by email, and what was attached; Q12: does the email evidence establish that a
human sent the message).

A fabricated mbox file would be detectable as fabricated and would undermine the
whole exercise. This instead accepts a REAL message over a REAL SMTP session,
so Thunderbird writes a genuine Sent record through its own normal code path.
The resulting mbox, its headers, and the base64 attachment are all artefacts the
application produced, not artefacts a script wrote.

The server log is a second, independent record of the same transaction — the
same principle as Sysmon and the Security log running side by side.

WHAT IT DOES NOT DO
-------------------
No authentication checks, no relay, no TLS. It binds to the host and accepts
anything from the guest. That is deliberate and is recorded as an environment
limitation, not presented as a mail server.

USAGE
-----
    python3 smtp_sink.py                 # listens on 0.0.0.0:2525
    python3 smtp_sink.py --port 2525 --out ./mail_capture

Then configure Thunderbird with:
    Server name : <host address, e.g. 172.16.167.1>
    Port        : 2525
    Security    : None
    Auth        : No authentication
"""

import argparse
import base64
import datetime as dt
import email
import email.policy
import hashlib
import json
import os
import socket
import threading

LOG_LOCK = threading.Lock()


def now():
    t = dt.datetime.now(dt.timezone.utc).astimezone()
    return t.strftime("%Y-%m-%dT%H:%M:%S%z")


def log_line(path, record):
    with LOG_LOCK:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def handle(conn, addr, outdir):
    conn.settimeout(120)
    fh = conn.makefile("rwb", buffering=0)

    def send(line):
        fh.write((line + "\r\n").encode())

    def readline():
        raw = fh.readline()
        if not raw:
            raise ConnectionError("client closed")
        return raw.decode("utf-8", "replace").rstrip("\r\n")

    session = {
        "ts": now(),
        "peer": f"{addr[0]}:{addr[1]}",
        "mail_from": None,
        "rcpt_to": [],
        "authenticated_as": None,
    }

    try:
        send("220 astermail.example ESMTP LXL-DFIR-001 sink")

        while True:
            line = readline()
            verb = line.split(" ", 1)[0].upper()

            if verb in ("EHLO", "HELO"):
                send("250-astermail.example greets you")
                send("250-SIZE 52428800")
                send("250-8BITMIME")
                send("250-AUTH PLAIN LOGIN")
                send("250 HELP")

            elif verb == "AUTH":
                parts = line.split(" ")
                if len(parts) >= 3 and parts[1].upper() == "PLAIN":
                    try:
                        decoded = base64.b64decode(parts[2]).decode("utf-8", "replace")
                        fields = decoded.split("\x00")
                        session["authenticated_as"] = fields[1] if len(fields) > 1 else decoded
                    except Exception:
                        session["authenticated_as"] = "<undecodable>"
                elif len(parts) >= 2 and parts[1].upper() == "LOGIN":
                    send("334 VXNlcm5hbWU6")
                    readline()
                    send("334 UGFzc3dvcmQ6")
                    readline()
                    session["authenticated_as"] = "<login-supplied>"
                send("235 2.7.0 Authentication successful")

            elif verb == "MAIL":
                # MAIL FROM:<addr> SIZE=123 — keep the address, drop the parameters
                rest = line.split(":", 1)[1].strip()
                addr_part = rest.split()[0] if rest else ""
                session["mail_from"] = addr_part.strip().strip("<>")
                send("250 2.1.0 Ok")

            elif verb == "RCPT":
                rest = line.split(":", 1)[1].strip()
                session["rcpt_to"].append((rest.split()[0] if rest else "").strip().strip("<>"))
                send("250 2.1.5 Ok")

            elif verb == "DATA":
                send("354 End data with <CR><LF>.<CR><LF>")
                chunks = []
                while True:
                    dline = readline()
                    if dline == ".":
                        break
                    chunks.append(dline)
                body = ("\r\n".join(chunks) + "\r\n").encode("utf-8")

                digest = hashlib.sha256(body).hexdigest()
                stamp = dt.datetime.now().strftime("%Y%m%dT%H%M%S")
                fname = f"{stamp}_{digest[:12]}.eml"
                fpath = os.path.join(outdir, fname)
                with open(fpath, "wb") as mf:
                    mf.write(body)

                # Parse the message once so the log carries decoded, usable
                # fields. Subject is decoded from RFC 2047; Message-ID is the
                # join key that ties this external record to the local mbox.
                try:
                    parsed = email.message_from_bytes(body, policy=email.policy.default)
                    subject = parsed.get("Subject")
                    message_id = parsed.get("Message-ID")
                    date_hdr = parsed.get("Date")
                except Exception:
                    subject = message_id = date_hdr = None

                record = dict(session)
                record.update({
                    "bytes": len(body),
                    "sha256": digest,
                    "stored_as": fname,
                    "subject": str(subject) if subject is not None else None,
                    "message_id": str(message_id) if message_id is not None else None,
                    "date_header": str(date_hdr) if date_hdr is not None else None,
                })
                log_line(os.path.join(outdir, "smtp_access.jsonl"), record)
                print(f"[{record['ts']}] {session['mail_from']} -> "
                      f"{','.join(session['rcpt_to'])}  {len(body)} B  {digest[:16]}")
                session["rcpt_to"] = []
                send("250 2.0.0 Ok: queued as LXL001")

            elif verb == "RSET":
                session["mail_from"] = None
                session["rcpt_to"] = []
                send("250 2.0.0 Ok")

            elif verb == "NOOP":
                send("250 2.0.0 Ok")

            elif verb == "QUIT":
                send("221 2.0.0 Bye")
                break

            else:
                send("502 5.5.2 Command not implemented")

    except Exception as exc:
        print(f"  connection from {addr} ended: {exc}")
    finally:
        try:
            fh.close()
        except Exception:
            pass
        conn.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=2525)
    ap.add_argument("--bind", default="0.0.0.0")
    ap.add_argument("--out", default="mail_capture")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    print(f"SMTP sink listening on {args.bind}:{args.port}")
    print(f"Captured mail -> {os.path.abspath(args.out)}")
    print(f"Log           -> {os.path.abspath(os.path.join(args.out,'smtp_access.jsonl'))}")
    print("Ctrl-C to stop.\n")

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((args.bind, args.port))
    srv.listen(5)

    try:
        while True:
            conn, addr = srv.accept()
            threading.Thread(target=handle, args=(conn, addr, args.out),
                             daemon=True).start()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        srv.close()


if __name__ == "__main__":
    main()
