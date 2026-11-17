# Ground truth vs. findings — 30 October 2026 incident

`SIMULATED / ACADEMIC CASE — NOT FOR LEGAL USE`

Comparison is **blind in the direction that matters**: the findings were derived from
artefacts first (Days 6–10) and compared to the frozen ground truth afterwards.
`GROUND_TRUTH_TIMELINE.csv` was frozen on 26 Oct; `GROUND_TRUTH_FROZEN_26Oct.txt`
`27329c2c…cc102f`. Amended once, on 30 Oct, **before** this comparison, for the
missing email attachment — the amendment is disclosed in the GT itself.

Companion data: `02_ground_truth/ACTUAL_TIMELINE_30Oct.csv` (27 rows).

---

## 1. Verdict summary — all 19 steps

| Verdict | Count | Steps |
|---|---|---|
| **CONFIRMED** | 13 | 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15 |
| **CONFIRMED with a time difference** | 3 | 14 (none), 16 (−4.4 s), 18 (−2 s) |
| **CONFIRMED but the expected artefact was wrong** | 3 | 1 (two logons), 9a (manual), 16 (no EID 26) |
| **NOT YET TABULATED** | 3 | 2 (ShellBags), 17 (Firefox history), 19 (lock) |
| **EXPECTED ARTEFACT DOES NOT EXIST — and cannot** | 1 | 3 (USBSTOR, UAS device) |
| **UNEXPLAINED** | 1 | X1 (port 8000) |

**No step failed to occur.** Every one of the 19 actions left evidence. The
discrepancies are in **artefact expectations and precision**, not in the events.

---

## 2. Where the ground truth was wrong about artefacts

### 2.1 `Enum\USBSTOR` cannot exist for this device (step 3)

GT expected **"USBSTOR serial"**. It is absent, and **its absence is not
suspicious**: the stick is a **UAS (USB Attached SCSI) device**, which enumerates
under the SCSI classes, not USBSTOR. Windows never writes `Enum\USBSTOR` for it.

**Report consequence:** the device is identified from `MountedDevices`,
`MountPoints2`, `setupapi.dev.log` and, decisively, **the filesystem's own volume
serial and artefacts**. A reviewer expecting a USBSTOR key would otherwise read
this as a collection failure. Say so explicitly.

### 2.2 Sysmon EID 26 is not configured on this VM (step 16)

GT expected **"Sysmon 23/26"**. **EID 23 present (×5), EID 26 absent because the
config does not enable it** — a configuration gap, not an absence of the event.
The deletion is nonetheless proven **three ways**: Sysmon 23, `$UsnJrnl`
rename/hard-link records, and the FAT `_robe.txt` deletion marker on the USB.

### 2.3 Two logons, one session (step 1)

GT expected **a** 4624 Type 2. There are **two**:

| LogonId | Time | Carries |
|---|---|---|
| `0x109b61f` | 16:31:46 | shell |
| `0x1286858` | 16:32:38 | 7-Zip, Thunderbird, Firefox — **all incident activity** |

**Attribution must be to user *and* session, not user alone.** A report that
attributes "the user did X" on the strength of a LogonId must name which one.

---

## 3. Where the note was wrong about time

The human incident note was written after the fact. **It is late, never early,
and by seconds:**

| Event | Note | Artefact | Δ |
|---|---|---|---|
| Step 16 deletion | 17:06:42 | **17:06:37.579** (`$J` + Sysmon 23) | note **+4.4 s** |
| Step 18 ejection | 17:10:37 | **17:10:35** (registry) | note **+2 s** |

**Deviation 3 of `INCIDENT_COMPLETE_30Oct.md` is also wrong on spacing.** It says
the three USB copies happened "within ~5 seconds". Sysmon shows:

```
16:56:28.595 → 16:56:40.113 → 16:56:52.806     24.2 s total, ~12 s apart
```

**The correction is recorded beside the deviation; the original text is left as
written.** Do not silently edit a contemporaneous record.

**Significance for Q8:** the deviation itself argues the selectivity finding does
not depend on interval — and it doesn't. But **the correction strengthens the
point**: a 24-second spread across three files is deliberate, sequential copying,
not a drag-select. **The report gets to say that because it checked.**

---

## 4. What the comparison is actually worth

**Two independent systems, with no visibility of each other, agree on the same
eight bytes of data:**

| Route | Record | Hash |
|---|---|---|
| USB | E-002 inode 17, `icat` | `9c75f0db…037074b` |
| Cloud | server `access.jsonl` | `9c75f0db…037074b` |
| Archive contents | 4 members decrypted | match 4/4 to E-001 originals |

**The email produced no data payload** — 424 B, text/plain, no attachment. It
evidences **an external communication**, not a transfer of files. Q11 is weaker
than designed and is reported as weaker. **This was caught by measuring the message
against a known baseline, not by looking at the interface.**

---

## 5. Open items carried out of this comparison

| ID | Item | Status |
|---|---|---|
| OPEN-1 | USB activity at **16:04:38–16:08:53**, ~26 min **before** the logon. `.fseventsd` 16:33:32 (macOS) precedes the Windows mount 16:33:37 by 5 s. Pre-flight or separate examiner activity — **needs the examiner's confirmation** | **OPEN** |
| OPEN-2 | `Sysmon/A6402EF3…CB3255.txt` on E-002, content `??probe` | **UNEXPLAINED** |
| OPEN-3 | Port 8000 loop, 17:09:08–17:09:10, 10 × SYN → RST+ACK | **UNEXPLAINED** |
| OPEN-4 | `access.jsonl` has **no `user` field**; the account is identified **only** from the PCAP login POST | **RESOLVED — state in report** |
| OPEN-5 | E-008 listed one hash for a two-file exhibit. **Resolved 12 Nov:** register §3a now records both — log `2df6a57e…c3f905` (examiner-computed), stored artefact `9c75f0db…037074b` (service-recorded, corroborated from E-002) | **CLOSED** |

## 6. Still not tabulated (honest gap)

Steps **2, 17, 19** — ShellBags, Firefox history/cache, and lock events — are
recorded in the note but **not yet reduced to artefact-level timestamps**. They are
marked `NOT YET TABULATED` in the CSV rather than filled with the note's times.
**A comparison table containing unverified numbers is worse than one with visible
gaps.**
