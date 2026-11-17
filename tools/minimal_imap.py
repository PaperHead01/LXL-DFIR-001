#!/usr/bin/env python3
"""
minimal_imap.py — a deliberately minimal IMAP4 server for LXL-DFIR-001.

PURPOSE
-------
Thunderbird's account wizard verifies the INCOMING server before it will
create an account. Nothing listens on 143 in this lab, so the wizard fails
and can dead-end. This gives it something to talk to so the account can be
created through the normal GUI path.

WHAT IT IS NOT
--------------
It is not a mail store. It holds no messages, accepts no deliveries, and
stores nothing. It answers the handful of commands an IMAP client needs in
order to complete a connection and discover that there is one empty INBOX.

The case examines OUTGOING mail and a LOCAL store. Received mail is out of
scope. This server deliberately cannot receive or store mail, so it cannot
contaminate the evidence.

CLASSIFICATION: SIMULATED / ACADEMIC — part of the LXL-DFIR-001 lab.

USAGE
    python3 minimal_imap.py --port 8114
"""

import argparse
import socket
import threading

GREETING = b"* OK [CAPABILITY IMAP4rev1] asterion.example IMAP ready\r\n"


def handle(conn, addr):
    """Serve one IMAP connection until the client logs out or disconnects."""
    try:
        conn.sendall(GREETING)
        buf = b""
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            buf += chunk
            while b"\r\n" in buf:
                raw, buf = buf.split(b"\r\n", 1)
                line = raw.decode("utf-8", "replace").strip()
                if not line:
                    continue

                parts = line.split(" ", 2)
                tag = parts[0]
                verb = parts[1].upper() if len(parts) > 1 else ""

                if verb == "CAPABILITY":
                    conn.sendall(b"* CAPABILITY IMAP4rev1 LITERAL+\r\n")
                elif verb in ("SELECT", "EXAMINE"):
                    conn.sendall(
                        b"* FLAGS (\\Seen \\Answered \\Flagged \\Deleted \\Draft)\r\n"
                        b"* OK [PERMANENTFLAGS ()] Read-only mailbox\r\n"
                        b"* 0 EXISTS\r\n"
                        b"* 0 RECENT\r\n"
                        b"* OK [UIDVALIDITY 1] UIDs valid\r\n"
                        b"* OK [UIDNEXT 1] Predicted next UID\r\n"
                    )
                elif verb == "LIST":
                    conn.sendall(b'* LIST (\\HasNoChildren) "/" "INBOX"\r\n')
                elif verb == "LSUB":
                    conn.sendall(b'* LSUB () "/" "INBOX"\r\n')
                elif verb == "STATUS":
                    conn.sendall(b"* STATUS INBOX (MESSAGES 0 UIDNEXT 1)\r\n")
                elif verb == "NOOP":
                    pass
                elif verb == "LOGOUT":
                    conn.sendall(b"* BYE logging out\r\n")
                    conn.sendall(f"{tag} OK LOGOUT completed\r\n".encode())
                    conn.close()
                    return

                # Every verb — including LOGIN, which this server accepts
                # blindly — is answered OK. There are no accounts and no
                # credentials here. Nothing of value is being protected.
                conn.sendall(f"{tag} OK {verb or 'OK'} completed\r\n".encode())
                print(f"  [{addr[0]}:{addr[1]}] {line}", flush=True)
    except (ConnectionResetError, BrokenPipeError):
        pass
    finally:
        try:
            conn.close()
        except OSError:
            pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8114)
    ap.add_argument("--bind", default="0.0.0.0")
    args = ap.parse_args()

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((args.bind, args.port))
    srv.listen(8)
    print(f"minimal IMAP listening on {args.bind}:{args.port}", flush=True)
    print("No mail is stored by this server.", flush=True)
    try:
        while True:
            conn, addr = srv.accept()
            threading.Thread(target=handle, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\nstopping", flush=True)
    finally:
        srv.close()


if __name__ == "__main__":
    main()
