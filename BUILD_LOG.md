# Build Log — LXL-DFIR-001

A daily record of what was done, what broke, and what was learned. Written in five minutes at the end of each working session from `00_case/examiner_notes.md`.

**Why this exists:** in forensics, documentation is the deliverable, not a by-product of it. This log is also the raw material for the public posts — and the "Learned" and "Broke" lines are the only ones worth reading.

---

## Day 0 — Sat 17 Oct 2026

**Phase:** Prep

**Did:**
- Case tree created at `~/Cases/LXL-DFIR-001/`
- Host tooling installed: sleuthkit, python@3.12, wireshark, p7zip
- USB hardware descriptors recorded (VID/PID/serial) before any evidence existed
- Cloud service built and tested end to end

**Broke:**
- Flask app threw `NameError: name 'session' is not defined` on first run — the `session` import was missing from the `flask` import list. Caught by testing rather than by shipping it.

**Learned:**
- A tool is validated when it produces the correct answer on data whose answer you already know. Recording the USB serial from hardware *today* means that on Day 6, when I recover the same serial from the Windows registry, I'm not hoping the parsing worked — I'm demonstrating it did.
- `bytes_in` in the cloud server log (18,442,418) does not equal `bytes_stored` (18,442,199). The 219-byte gap is MIME multipart framing. If you don't know that, the discrepancy looks like an error.

**Decided:**
- Manual PowerShell collection as the primary acquisition method. KAPE's behaviour under ARM64 emulation is unverified, and acquisition day is the wrong day to discover that.

**Artefacts produced:** `02_ground_truth/usb_identity.txt`, `01_lab/validation/`, `tools/nimbusshare.py`

---

## Day 1 — Sun 18 Oct 2026

**Phase:** Build — VM

**Did:**

**Broke:**

**Learned:**

**Decided:**

**Artefacts produced:**

---

<!--
Template — copy for each day.

## Day N — DDD DD Mon 2026

**Phase:**

**Did:**

**Broke:**

**Learned:**

**Decided:**

**Artefacts produced:**
-->
