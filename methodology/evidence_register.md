# EVIDENCE REGISTER — Revision 2

`SIMULATED / ACADEMIC CASE — NOT FOR LEGAL USE`

**Supersedes:** `LXL-DFIR-001.md` §3.4 (Revision 1, 13 Oct 2026)
**Issued:** 31 Oct 2026, 20:40 IST
**Reason:** Revision 1 allocated exhibit numbers by *evidence type*. Acquisition
numbered by *item acquired*. The two disagreed. This revision records what was
actually acquired and retires the Revision 1 allocations.

---

## 1. The rule this revision applies

> **An exhibit number is assigned at acquisition, and is never reused or
> reassigned.**

This is why Revision 1's E-005, E-006 and E-007 are not recycled below. A number
that once meant "memory image" and later means "email store" makes every prior
note, timeline row and interview reference ambiguous. Numbers are cheap; ambiguity
is not.

### 1a. Folders exist only for acquired exhibits

`03_evidence/` contains **E-001, E-002, E-003, E-004, E-008** and nothing else.
It contains no E-005, E-006 or E-007 directory, because nothing was ever acquired
under those numbers, and it will contain no E-009 directory until that item is
acquired.

**This is deliberate.** An empty folder is ambiguous: a reader cannot tell whether
the item was never acquired or was acquired and subsequently lost. The absence of
a directory states plainly that nothing was acquired. The numbering scheme lives in
this register, not in the filesystem.

Consistency between the register and the folder names is a **quality-assurance**
issue, not an evidentiary one. It is corrected **before any analysis has been
performed**, so no finding in this case depends on the change.

---

## 2. Current exhibits

| ID | Item | Location | Acquired | SHA-256 |
|---|---|---|---|---|
| **E-001** | Full physical disk image, `AST-WKS-0471` — 50 GiB raw, from the VMDK chain tip `Virtual Disk-000005.vmdk` | SSD `forensics_images/AST-WKS-0471.raw` | 31 Oct 18:25 | `57ac362d…f9ea5c` |
| **E-002** | Full physical image, USB device `SanDisk 3.2Gen1` — 61,524,148,224 B raw | SSD `forensics_images/usb_E-002_run2.dd` | 31 Oct 20:24 | `2ae0d727…130f29` |
| **E-003** | Network capture, incident window — 218 packets, snaplen 524288 | `03_evidence/E-003/network/` | 30 Oct 16:26–17:12 | `92545c31…9ad0cc` |
| **E-004** | Email — incident message, control message, SMTP sink log | `03_evidence/E-004/mail/` | 30 Oct 17:01 | `a143595a…e6085` (incident) |
| **E-008** | Cloud service records — **two files** (see 2a) | `03_evidence/E-008/cloud/` | 30 Oct 17:03 | see 2a |
| **E-010** | Acquisition records — this register, hash manifest, chain of custody, ACQUISITION_RECORD_31Oct | `00_case/` | ongoing | — |
| **E-009** | Browser artefacts — Firefox profile | pending | Day 8–9 | — |
| **E-011** | *(reserved)* Windows artefact collection from the E-001 image — registry hives, `$MFT`, `$UsnJrnl`, event logs, ShellBags | pending | Day 6–7 | — |

**E-011 is new.** Revision 1 treated registry, `$MFT` and event logs as the
*primary acquisition* (E-001). They are now **derived artefacts extracted from
E-001**, not separately seized items. That is the correct relationship: they are
carved from the image and their provenance points at it.

---

## 3. Retired allocations

| ID | Revision 1 meaning | Why retired |
|---|---|---|
| E-005 | Email store — Thunderbird profile, mbox, Gloda | Email was captured as `.eml` files and an SMTP sink log at **E-004** instead. A full Thunderbird profile was not acquired. **Number retired, not reused.** |
| E-006 | USB — full physical E01 with embedded case metadata | The USB was imaged as **raw `dd` at E-002**, on macOS, where E01 tooling (EWF) was not used. The Rev 1 description also specified an E01; what was produced is a raw image with external hash record. **Number retired, not reused.** |
| E-007 | Network capture — PCAP of the incident window | The capture was assigned **E-003**. **Number retired, not reused.** |
| E-002 (Rev 1) | Memory image — `.vmem` + `.vmss`/`.vmsn` | **Permanently excluded.** The `.vmem` is encrypted by Fusion's vTPM scheme and is not readable without the key. No memory image exists or will exist. The number was **reassigned to the USB image at acquisition**, which is recorded here as a knowing reassignment made before analysis. |

**Note on the E-002 reassignment.** This is the one case where a number changed
meaning rather than being retired. It happened during acquisition on 31 Oct, before
any artefact in E-002 had been examined, and it is recorded here explicitly so that
no reader believes memory was ever imaged. If this case were ever tendered in
court, that reassignment is exactly the sort of thing opposing counsel would use
to suggest the record is unreliable — which is why it is disclosed in the register
rather than quietly corrected.

---

## 3a. E-008 is a two-file exhibit — both hashes recorded

**Correction, 12 Nov 2026.** Revision 2 listed a single hash against E-008 while
describing it as *"`access.jsonl` + stored uploaded artefact"*. **One hash cannot
describe two files.** Both are now recorded, and the description is explicit.

| File | Size | SHA-256 | Source of the value |
|---|---|---|---|
| `access.jsonl` | 2,419 B | `2df6a57e34356bf2f9c693dd854e6c047ce169577b1f689067db95d3f3c3f905` | **computed by the examiner, 12 Nov 2026** |
| stored upload (`Atlas_backup.7z` as received) | 8,296 B | `9c75f0db535a0b7fc22866f35800a9b9aa689af946376744860f53d18037074b` | **recorded by the service at receipt** (field `sha256`), and **independently by `icat` from E-002 inode 17** |

**Note the asymmetry, and keep it:** the log's hash is examiner-computed. The
stored artefact's hash is **the service's own assertion**, corroborated *from a
different exhibit* — the USB image — rather than from the stored file itself. **If
the stored file is ever produced as a discrete item it must be hashed directly and
this entry updated.**

## 4. Standing statement for the report

> Exhibits E-001 to E-004 and E-008 were acquired and hashed on or before
> 31 October 2026. E-001 and E-002 are full physical images verified by
> source-and-image SHA-256 comparison taken with the source volume unmounted.
> All artefacts are derived from a simulated environment built for the purpose of
> this exercise. No real individual's data is present.

`SIMULATED / ACADEMIC CASE — NOT FOR LEGAL USE`


### E-011 — artefacts derived from E-001 (updated Day 6, Tue 3 Nov 2026)

Derived, not acquired. Hashes recorded in
`04_extraction/E-011_ARTEFACT_HASHES.txt`.

| Artefact | Size | SHA-256 |
|---|---|---|
| `task_Asterion_Confidential_Backup.xml` | 4,098 B | `babf5318…ead0d46` |
| `hives/SYSTEM` | 12 MB | `b56c717a…c56fc` |
| `hives/SOFTWARE` | 77 MB | `ca541afa…37a37` |
| `hives/SAM` | 65,536 B | `48d98ef6…b0d89` |
| `hives/NTUSER.DAT` | 2.5 MB | `55bb35fb…4ef59` |

Still to be added as the case proceeds: registry/`$MFT`/event-log/ShellBag/LNK
extractions (Days 7–8), and the memory image, which was **never acquired** (Fusion
vTPM encrypts `.vmem`) — recorded here so the absence is not mistaken for a loss.
