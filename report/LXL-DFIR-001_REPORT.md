# DIGITAL FORENSIC EXAMINATION REPORT

## LXL-DFIR-001 — Corporate Insider Data Transfer

**Client:** Asterion Technologies Pvt. Ltd. *(fictional)*
**System examined:** AST-WKS-0471 — Windows 11 ARM64, domain-joined workstation
**Examiner:** Aditya Pandey
**Report date:** 12 November 2026
**Case opened:** 17 October 2026
**Incident date:** 30 October 2026

> **SIMULATED / ACADEMIC CASE — NOT FOR LEGAL USE**
>
> This report relates to a simulated case constructed for training and
> assessment. No real person, company or data is involved. It is not a legal
> document and does not describe any real event.

---

## 1. EXECUTIVE SUMMARY

**The question asked.** Does the available digital evidence establish unauthorised
access, collection, transfer, or attempted concealment of corporate data during the
subject's notice period?

**What the examination established.**

1. **Four company files were opened** on AST-WKS-0471 on 30 October 2026 between
   16:35 and 16:39 IST, three of them from a folder marked CONFIDENTIAL and one
   from a folder marked RESTRICTED.
2. **A copy of those files was assembled** in a non-standard folder,
   `C:\Users\rahul.mehta\Documents\Backup`, between 16:41 and 16:42 IST, and
   compressed into a **password-protected 7-Zip archive at 16:48:47**.
3. **Three items were copied to a removable USB device** between 16:56:28 and
   16:56:52 IST — the archive and two of the four staged spreadsheets. **The two
   PDF documents were not copied.**
4. **The archive was uploaded to an external web service at 17:03:41 IST**, and
   **the file the service received is byte-for-byte identical** — SHA-256
   `9c75f0db…037074b` — to the copy on the USB device, and its four internal
   members are byte-for-byte identical to the four files still present on the
   workstation.
5. **A 424-byte email with no attachment** was sent from the subject's corporate
   account to an address at a different company at 17:01:01 IST, subject
   *"Atlas — for your review"*.
6. **The staging folder was deleted at 17:06:37.579 IST** using a method that
   bypasses the Recycle Bin.

**What the examination did not establish.**

- **Who was at the keyboard.** The evidence attributes activity to an account, a
  session, a device and a browser. It does not identify a human being.
- **Motive.** The pattern is equally consistent with deliberate targeting and with
  an urgent, legitimate deadline. Both are recorded.
- **That the email carried data.** It did not. The email evidences an external
  communication only.
- **The identity of the external recipient.**

**Confidence.** The principal transfer findings are assessed **HIGH**, resting on
hash equality between three independently-recorded sources. Attribution to a
*person* is assessed **UNDETERMINED** and is not asserted anywhere in this report.

**What the client may state.** That a company archive and two company spreadsheets
left the workstation by two independent routes and were found on a USB device; that
the archive was uploaded to an external service; and that the staging folder was
deleted. The client may not state, on this evidence alone, that the subject
personally performed these acts or intended harm.

---

## 2. BACKGROUND

### 2.1 Case background

Asterion Technologies Pvt. Ltd. is a fictional technology company. The subject,
Rahul Mehta (employee AST-0471), a Senior Product Engineer, resigned and was
serving a notice period. The client's concern was that confidential material was
being removed before the employment ended. AST-WKS-0471 was surrendered for
examination.

The environment — the workstation, the removable device, the mail server, the
cloud service and every document — was **constructed for this exercise**. The
incident itself was executed by the examiner on 30 October 2026 in a controlled
sequence, with a contemporaneous record made before the examination began. That
record is the ground truth against which this examination was later tested.

### 2.2 Objectives

> Does the available digital evidence establish unauthorised access, collection,
> transfer, or attempted concealment of corporate data during the subject's notice
> period?

### 2.3 Scope

**In scope.** The workstation image; one removable USB device; a network capture
taken across the incident window; the mail server's record of one message; the
cloud service's access log and the artefact it received.

**Out of scope, deliberately.** Memory acquisition of a live system; the subject's
personal devices; the recipient organisation; the subject's home network; any
device not connected to AST-WKS-0471. **This report makes no finding on any matter
outside this list,** and the exclusion is stated so that the report cannot be read
as having examined them.

### 2.4 Regulatory context

Asterion would be required to report a cyber security incident to **CERT-In within
six hours** under the IT Act and the 2022 directions. The **Digital Personal Data
Protection Act 2023** breach notification obligations under s.8(6) and Rule 7
commence **13 May 2027** and were **not in force** at the date of this incident;
any reference to them is forward-looking. This is a forensic examination, not a
legal opinion: the report states what the evidence establishes, and the client's
counsel determines what must be filed.

---

## 3. EVIDENCE

### 3.1 Inventory

| Ref | Description | Acquired | Integrity |
|---|---|---|---|
| **E-001** | Full physical image of AST-WKS-0471 storage, 50 GB raw | 31 Oct 2026 | `57ac362d…f9ea5c` |
| **E-002** | Full physical image of the USB device, 57 GB `dd` | 31 Oct 2026 | `2ae0d727…130f29` |
| **E-003** | Network capture, incident window, 218 packets | 30 Oct 2026 | `92545c31…9ad0cc` |
| **E-004** | Incident email (`a143595a…e6085`), control message, mail server log | 30 Oct 2026 | per-file in manifest |
| **E-008** | Cloud service: access log (`2df6a57e…c3f905`) and stored artefact (`9c75f0db…037074b`) | 30 Oct 2026 | both recorded |
| **E-011** | Derived Windows artefacts from E-001: registry hives, `$MFT`, `$UsnJrnl`, event logs, ShellBags | extracted | per-file in manifest |

Numbers E-005, E-006 and E-007 were allocated and retired without acquisition;
**no directory exists for them**, because an empty directory cannot be
distinguished from a lost exhibit. E-009 (browser profile) remains **reserved and
unallocated** — the 22–23 October browsing window it was reserved for has not been
acquired. E-011 was reserved prospectively and **has since been acquired**; its
per-file hashes are in the manifest.

### 3.2 Acquisition methods

**E-001 and E-002 — physical imaging.** Both source volumes were **unmounted at
the operating-system level before imaging** and remained unmounted throughout. Each
image was verified by comparing the SHA-256 of the source device against the
SHA-256 of the image. The USB device was imaged with `dd` because the device is a
UAS mass-storage device presenting a single FAT32 volume; a linear physical read
captures the partition table, boot sector, both FATs and all clusters, which is
what a filesystem-level examination requires.

**No hardware write-blocker was used.** The procedure relied on software
unmounting. This is a genuine limitation (§9.2) and is not mitigated by any claim
to the contrary.

**E-003 — live capture.** Taken on the host-only network interface during the
incident window, snaplen 524288, 218 packets, **0 dropped by the kernel**. Hashed
at 17:16 IST on 30 October, **before the file was opened, copied or examined**.

### 3.3 Integrity verification — three checkpoints

The value of a hash is that it is taken more than once, at points separated by
work.

| Exhibit | 1. At acquisition | 2. Before examination | 3. At report |
|---|---|---|---|
| E-001 | `57ac362d…f9ea5c` | same | same |
| E-002 | `2ae0d727…130f29` | same (12 Nov 2026) | same |
| E-003 | `92545c31…9ad0cc` (17:16, 30 Oct) | same | same |

**E-002 is the exhibit whose integrity was previously in doubt and is now
settled.** On 31 October a hash disagreement was recorded between the device and
its image. The cause was established as **the source volume having been mounted
read-write while the image was being taken**, proved by repeating the acquisition
with the volume unmounted and obtaining an exact match. **The original mismatch is
disclosed, not removed from the record**; see §9.2.

### 3.4 Chain of custody

Full form at Appendix C. Every transfer of every exhibit is recorded with date,
time, from, to and purpose. The CHAIN_OF_CUSTODY entries for E-002 record the
31 October mismatch and its resolution.

---

## 4. METHODOLOGY

### 4.1 Examination environment

Examination was conducted on an Apple Silicon host running macOS, with Windows 11
ARM64 guests under VMware Fusion. Artefact extraction used The Sleuth Kit and
`pytsk`-based tooling; event log parsing used `python-evtx`; hive parsing used
`regipy`; archive extraction used `py7zr`; packet analysis used `tshark`; timeline
work used Plaso.

**These are statements of description.** Every tool whose output supports a finding
appears in §5 with the specific test that validated it. **No finding in this
report depends on a tool that was not tested against a known value.**

### 4.2 Approach

**The examination was question-driven, not tool-driven.** Eighteen questions were
fixed **before** examination began (Appendix F) and were not altered afterwards.
Tools were selected to answer a question; no tool was run to see what it would
produce. This order matters: a question set fixed in advance can be failed by the
evidence, whereas a question set written after the evidence can only be confirmed
by it.

### 4.3 Order of volatility

Volatile data (network traffic) was preserved first, then removable media, then
disk artefacts, in accordance with RFC 3227. In this case E-003 was captured live
on the incident day; E-001 and E-002 were imaged on 31 October, after the
workstation had already been powered down.

### 4.4 Analysis techniques, and what was expected before looking

| Artefact class | Examined with | Expected to yield | Actually yielded |
|---|---|---|---|
| `$MFT` | Sleuth Kit `fls`, `istat` | File creation, modification, inode numbers | Inode map; staging folder **123225**; originals 154479/154337/154335/154481 |
| `$UsnJrnl:$J` | `usn_parse.py` (custom, skip-zero optimisation) | Change journal: creates, renames, deletes **by name** | **324,908 records**, 739 relevant; the deletion and its name |
| Sysmon Operational | `evtx_window.py` (custom) | Process creation with command lines; file creates; file deletes | **113,755 records**; the 7-Zip command line **including the password**; 5 delete events |
| Security / System | `evtx_window.py` | Logons and session boundaries | **Two** LogonIds; scheduled-task execution |
| Registry | `regipy` | Device identification, mount history, USB removal | `MountedDevices`, `MountPoints2`, `USB` key removal timestamp |
| Filesystem (USB) | Sleuth Kit `fls`, `icat` | Filenames, timestamps, deleted entries | Three copied files; a **deleted `probe.txt`** still in the directory entry |
| Network capture | `tshark` | Session timing and byte counts | SMTP session, HTTP POST, a refused-port loop |
| Archive | `py7zr` | Contents of the container | **All four members, each matching an original** |

---

## 5. TOOL VALIDATION

### 5.1 Validation approach

**A tool is validated when it has been shown to produce the correct answer on data
whose correct answer is already known.** Version numbers, vendor reputation and
popularity are not validation. For each tool used to support a finding, a test was
constructed with a known outcome and the tool's output compared against it.

### 5.2 The anchor: device identity recovered from two independent parsers

Before any evidence existed, the removable device's identifying values were
**recorded from the physical device** — volume label, volume serial and geometry.
After imaging, those values were recovered from the image by two unrelated
methods:

- the **partition table**, read directly from the image's byte offsets; and
- the **FAT32 boot sector**, parsed by The Sleuth Kit.

Both returned the recorded values. **A parser that invented plausible output
could not reproduce a value it had never seen.**

### 5.3 Known-value tests

| Tool | Version | Test | Known value | Outcome |
|---|---|---|---|---|
| The Sleuth Kit (`fls`, `icat`, `mmls`, `fsstat`) | 4.12 | Recover volume identity from E-002 | recorded pre-acquisition | **match** |
| `usn_parse.py` (custom) | in-repo | Parse `$J`; skip 4 KB zero blocks | record count vs. raw scan | **match**, 324,908 |
| `evtx_window.py` (custom) | in-repo | Window extraction across 3 logs | seen/showed/unparseable counts reconciled | **0 unparseable** of 113,755 |
| `py7zr` | 1.1.4 | Round-trip an archive with a known password; then with a wrong one | correct password succeeds, wrong fails | **both as expected** |
| `py7zr` | 1.1.4 | Decrypt E-002's archive and hash members | hashes of the four originals | **4/4 match** |
| `tshark` | 4.x | Byte counts vs. server log | `bytes_in` 8,529 vs `bytes_stored` 8,296 | **consistent** |
| `regipy` | current | Device keys present/absent | physically observed state | **match** |

### 5.4 Tools not validated, and the consequence

**`python-evtx`** was validated against output volume and parse success, but its
timestamp format differs from the ISO-8601 convention (it emits
`2026-10-18 12:53:30`, space-separated). **All times were re-parsed and
cross-checked against a second artefact class before use**; the two independent
records agree to the millisecond (§7.3). *Consequence: no finding is downgraded.*

**Plaso** produced the working super-timeline, but **no finding in this report
rests on Plaso output alone**; each is corroborated by a primary artefact read
directly from the image.

---

## 6. FINDINGS

![Figure 1 — Four independent recorders converging on one conclusion, and what they still do not establish](diagrams/02_four_recorders.png)


Each finding is stated, evidenced, and then tested against the counter-hypothesis
that the activity was **legitimate, work-related file handling**. A finding
supported by the evidence but not tested against that alternative is not finished.

### 6.1 Q1 — Devices connected during the notice period

**Finding.** One removable storage device was connected to AST-WKS-0471 on
30 October 2026, appearing as drive **E:**, and it was in use from approximately
16:33 to 17:10 IST. **No other removable device was connected during the period
examined.**

**Evidence.** The device's filesystem shows `System Volume Information` created at
16:05:26 and a macOS metadata directory `.fseventsd` at 16:33:32 — the moment the
device was presented to the host. Windows-side mount records and the device's own
directory timestamps place the mount at **16:33:37**, five seconds after the macOS
write. **The device was removed at 17:10:35**, recorded in the registry.

**Note on the disk's own label.** The device carries the label `NO NAME`, not the
`BACKUP` label anticipated in the case design. **The label is not evidence of
purpose** and is recorded exactly as found.

**Two logons, one session — a point of attribution.** Two interactive logons are
recorded on 30 October: `0x109b61f` at 16:31:46, which carries only the shell, and
`0x1286858` at 16:32:38, which carries **all of the incident activity**. **Findings
in this report are attributed to the session that carries the activity, not to the
user account in general.** A report that attributes activity to "the user" on the
strength of a LogonId must say which one.

**Against the counter-hypothesis.** A single device connected for 37 minutes is
consistent with ordinary file transfer. What distinguishes this instance is not
the device but **what was placed on it** (§6.10).

### 6.2 Q2 — Device identification

**Finding.** The device can be identified by its **volume serial, filesystem
geometry and volume label**, all recovered from the image. It **cannot** be
identified from `Enum\USBSTOR`, and the absence of that key is **expected, not
suspicious**.

**Evidence.** The device is a **USB Attached SCSI (UAS) mass-storage device**.
Windows records UAS devices under the SCSI device classes; it does **not** create
a per-device `USBSTOR` entry for them. The key's absence is therefore a property
of the device class, not of the collection.

Identification rests instead on: the volume serial number, recorded from the
physical device before imaging and recovered from the image (§5.2); the partition
table and FAT32 boot sector; and the mount records.

> **Deliberate omission:** the device's hardware serial is **not reproduced in
> this report.** It is recorded in the case file and available to the client on
> request. Publishing a serial in a document that may be circulated is a
> disclosure risk with no analytical benefit.

![Figure 2 — Why Enum\USBSTOR was legitimately absent](diagrams/04_usbstor_uas_binding.png)

**Residual limitation.** Had the device been a conventional USB mass-storage
device, `USBSTOR` would have supplied a hardware-level identifier. For this class
of device the identification is **filesystem-level**, which is weaker against a
deliberate attempt to substitute an identically-formatted device. Nothing in the
evidence suggests such a substitution.

### 6.3 Q3 — Files accessed, and from where

**Finding.** Four files were opened on the workstation on 30 October 2026, all
between 16:35 and 16:39 IST. **Three came from a folder marked CONFIDENTIAL and
one from a folder marked RESTRICTED.** None came from the SHARED folder.

| File | Source folder | Classification | Opened | Closed |
|---|---|---|---|---|
| `Project_Atlas_Strategy.pdf` | `04_Restricted` | RESTRICTED | ~16:35 | — |
| `Client_Master_List.xlsx` | `03_Confidential` | CONFIDENTIAL | 16:36:00 | 16:36:33 |
| `Q4_Financial_Model.xlsx` | `03_Confidential` | CONFIDENTIAL | 16:37:30 | 16:38:03 |
| `Source_Code_Architecture.pdf` | `04_Restricted` | RESTRICTED | 16:38:36 | 16:39:16 |

**Evidence.** Shell item and jump-list records for the four documents, and the
`$MFT` records of the files themselves (inodes 154479, 154337, 154335, 154481).

**Significance of the folder structure.** The case tree contained four folders:
`01_Projects`, `02_Shared`, `03_Confidential`, `04_Restricted`. **The subject's
role gave legitimate access to `01_Projects` and `02_Shared`.** Every file opened
came from the two folders carrying a classification marking, and **no file was
opened from either folder the role required.**

#### 6.3.1 Folder navigation recovered from ShellBags

A fourth, independent record of file access was recovered from the user's
`UsrClass.dat` ShellBag keys (`BagMRU`). **It records folder names and the time each
folder record was last written — something neither the change journal nor the
endpoint sensor records.**

| Folder node | Record last written (IST) | Child entries recorded in that node |
|---|---|---|
| `This PC` | **30 Oct 16:56:26** | `C:\`, `E:\` |
| `C:\` | **30 Oct 16:32:53** | `Tools`, **`Asterion`**, `Windows` |
| `C:\Asterion` | **30 Oct 16:41:22** | `01_Projects`, `02_Shared`, **`03_Confidential`**, **`04_Restricted`** |
| `C:\Asterion\01_Projects` … `04_Restricted` | 21 Oct 18:43–18:44 | *(individual entries)* |
| user `Documents` | **30 Oct 16:41:11** | **`Backup`** |
| `Documents\Backup` | **30 Oct 16:54:41** | **`Atlas_backup.7z`** |
| `E:\` | **30 Oct 16:56:26** | *(removable volume)* |

**Each of these lands beside an event already established from other artefacts:**

| ShellBag record written | Nearest established event | Difference |
|---|---|---|
| `C:\` shows `Asterion` | interactive logon 16:32:38 | +15 s |
| `C:\Asterion` | first staged copy 16:41:13.006 | **−1.6 s** |
| `Documents` shows `Backup` | staging folder created 16:40:15.490 | +56 s |
| `Documents\Backup` shows `Atlas_backup.7z` | archive created 16:48:47.643 | +6 min |
| **`E:\`** | first copy to removable media 16:56:28.595 | **−2.6 s** |
| root `BagMRU` | `POST /upload` 17:03:41.119 | **−12.3 s** |

**Two limitations, stated rather than glossed:**

1. **A ShellBag key's last-write time is when that key was last modified — not a
   visit log.** It establishes that a folder appeared in Explorer and when that
   record last changed. **It does not establish how many times the folder was
   opened**, and no visit count is asserted here.
2. **`C:\Asterion` carries a 30 October time, but the four folders beneath it carry
   21 October.** ShellBags therefore evidence the *Asterion* folder being opened on
   30 October; they do **not** by themselves evidence descending into the individual
   classification folders that day. **The individual file opens are evidenced by
   shell items and jump lists above, not by these keys.**

**Value.** This is the fourth independent source for the file-access finding, and
the only one that records **folder names as typed by the filesystem**. The `E:\`
record additionally corroborates the operator being in the removable volume's folder
**2.6 seconds before** the first file was written to it.

### 6.4 Q4 — Consistency with the established working pattern

**Finding.** The access pattern on 30 October **is not consistent with the pattern
recorded in the pre-collection baseline**, but the baseline is **thin**, and this
finding is assessed **LOW-MEDIUM** confidence.

**Evidence.** A baseline of the workstation's prior file-access activity was
recorded on 26 October, before the incident. It does not contain an instance of
bulk, sequential access to classified material of the kind seen on 30 October.

**Limitations, stated plainly.** A single baseline day cannot establish what a
person "normally" does. **Absence of a prior instance in a one-day baseline is weak
evidence of unusual behaviour**, and the report does not present it as strong. To
raise this finding above LOW-MEDIUM would require weeks of baseline activity, which
the engagement did not collect.

### 6.5 Q5 — Whether files were copied from their original locations

**Finding.** All four files were copied from their original folders into a staging
folder. **The originals were not moved or deleted; they remained in place.**

**Evidence.** The `$MFT` records for the originals show no deletion and no rename.
New records appear in the staging folder with content matching the originals
byte-for-byte (§6.7). `$UsnJrnl` records the creation of the staged copies without
any corresponding delete or rename on the originals.

**Against the counter-hypothesis.** Copying rather than moving preserves the
originals, which is what a careful employee working to a deadline would do. It is
also what a careful exfiltrator would do. **The evidence does not distinguish
them.**

### 6.6 Q6 — Collection staged in a non-standard location

**Finding.** A folder `Documents\Backup` was created at **16:40:15.490 IST** and
four files were copied into it between **16:41:13.006 and 16:42:14.880 IST**.

**Evidence.** `$UsnJrnl` records the folder's creation with a `COMPRESSION_CHANGE`
reason at 16:40:15.490; the folder's `$MFT` record is inode **123225**. Four Sysmon
event ID 11 (file create) records follow:

```
16:41:13.006   16:41:31.899   16:41:53.311   16:42:14.880
```

**Naming.** A folder called `Backup` in a user's `Documents` directory is not
intrinsically suspicious. **What makes it a staging location is not its name but
that fifteen minutes later its contents were compressed into a single archive and
the folder was deleted** (§6.7, §6.15).

### 6.7 Q7 — Whether an archive was created, and what can be established about its contents

**Finding.** A password-protected 7-Zip archive was created at **16:48:47.643 IST**
containing **exactly the four files staged in §6.6**. Each file inside the archive
is **byte-for-byte identical** to its original on the workstation.

**Evidence — and an improvement on the expected position.** The case design
anticipated that the archive's contents could not be examined because the password
would be unknown, and that contents could only be inferred from size and timing.
**That proved unnecessary.** The password was recovered from a command line
recorded by Sysmon:

```
7z a -t7z -p<redacted> ...      (16:48:47.643)
7z l ...                          (16:49:04.019)
```

The archive was then decrypted and its members extracted and hashed:

| Member | Size | SHA-256 | Identical to original on E-001 |
|---|---|---|---|
| `Client_Master_List.xlsx` | 5,237 B | `e16242e6…52a81f` | **yes** |
| `Q4_Financial_Model.xlsx` | 5,175 B | `f24be0c7…04743f` | **yes** |
| `Project_Atlas_Strategy.pdf` | 2,434 B | `47492af2…e4d3c24` | **yes** |
| `Source_Code_Architecture.pdf` | 2,212 B | `63b612bb…78ed1c2f` | **yes** |

**Total 15,058 bytes**, matching the sum of the four staged files, compressed to
**8,296 bytes** using `LZMA2:14` with `7zAES` encryption.

**What the archive does not contain.** `Vendor_Contracts_Summary.docx` and
`Salary_Bands_2026.xlsx`, both present and accessible in the same source folders,
are **absent**. **Selectivity is therefore established at content level, not
inferred from timings.**

**A second observation, recorded and not interpreted.** Seventeen seconds after
creating the archive, the same process **listed** it (`7z l`, 16:49:04.019). This
is consistent with the operator verifying his own output before relying on it. **It
is described, not concluded.**

![Figure 3 — The same 8,296 bytes leaving by two routes, hashed identically at both ends](diagrams/03_hash_correlation.png)

> **⚠ Credential-handling note.** The archive password and the cloud-service
> password recovered during this examination are recorded in the case file and are
> **deliberately redacted from this report.** Where a password's existence and
> provenance are relevant, they are stated; the value itself is not reproduced in
> a circulable document.

### 6.8 Q8 — What the timing and selectivity suggest

**Finding.** Of the files available in the four company folders, **four were
staged and three were transferred**; the two most sensitive document types present
— the two PDFs — were **staged but not transferred to removable media**, while
being **included in the archive that was uploaded to the cloud**.

**Selectivity, at two levels:**

| Level | Taken | Not taken |
|---|---|---|
| Staged | 4 files, 15,058 B | `Vendor_Contracts_Summary.docx`, `Salary_Bands_2026.xlsx`, and all `01_Projects`/`02_Shared` material |
| Copied to USB | 3 files, 18,708 B | the two PDFs |
| Uploaded (inside archive) | all 4 staged files | the two files never staged |

**Timing.** The three USB copies are spaced **~12 seconds apart, 24.2 seconds in
total** — sequential, file-by-file copying rather than a single bulk transfer.

**Analysis.** Selectivity of this kind is analytically meaningful: *"all files
copied"* suggests a bulk backup; *"some files copied, and not the same some at each
stage"* suggests a considered selection. **It does not establish intent.** A
colleague assembling material for a specific piece of work would make the same
selection. **Both readings are recorded and neither is preferred.**

**A correction to the contemporaneous note.** The incident note recorded the three
USB copies as occurring *"within ~5 seconds of each other"*. The artefact record
shows **24.2 seconds total, ~12 seconds apart**. The note is corrected here and the
original is retained unaltered in the case file. **The correction strengthens the
selectivity analysis rather than weakening it**, since a 24-second spread is not
what a drag-select produces.

### 6.9 Q9 — Whether files were transferred to removable media

**Finding.** Three items were copied to the USB device between **16:56:28.595 and
16:56:52.806 IST**.

**Evidence — and an explicit statement of what does not exist.** **There is no
Windows event that records "file copied."** No artefact states the act. The finding
rests on a correlation of four records:

1. **Sysmon event ID 11** (file create) reporting `TargetFilename=E:\…` at
   16:56:28.595, 16:56:40.113 and 16:56:52.806;
2. the **USB filesystem's own timestamps** for the three files, which agree **to
   the second** — 16:56:28, 16:56:40, 16:56:52;
3. the **hashes** of the files now on the USB device (§6.10); and
4. the **preserved modification times** carried in transit, which a re-created
   file would not carry.

**Why the agreement matters.** FAT32 timestamps are weak evidence in isolation:
they are stored in local time with 2-second precision and no timezone. **They are
strong when they agree with a second, independent record — which is exactly what
happened here.** The report states both the limitation and the corroboration.

### 6.10 Q10 — Which specific files, individually identified

| File | Size | SHA-256 | Equals original on E-001 |
|---|---|---|---|
| `Atlas_backup.7z` | 8,296 B | `9c75f0db…037074b` | **equals the cloud upload** |
| `Client_Master_List.xlsx` | 5,237 B | `e16242e6…52a81f` | **yes** |
| `Q4_Financial_Model.xlsx` | 5,175 B | `f24be0c7…04743f` | **yes** |

Each file was extracted from the USB image with `icat` and hashed. **The
modification times carried on the USB device — 19 September 2026 09:15:00 and
12 October 2026 18:22:00 — match those of the originals on the workstation**, which
is consistent with a copy operation and inconsistent with a file re-created from
content.

### 6.11 Q11 — Whether data was transmitted by email, and what was attached

**Finding.** A message **was** transmitted from `rahul.mehta@asterion.example` to
`s.varma@novaedge.example` at **17:01:01 IST**. **No file was attached to it.**

| Field | Value |
|---|---|
| Message-ID | `fe619c67-96d6-40c9-af41-07881b4bbf1a@asterion.example` |
| Size | **424 bytes** |
| Content-Type | `text/plain; charset=UTF-8` |
| Subject | *"Atlas — for your review"* |
| Body | `short, plausible` |
| Attachments | **none** |

**Evidence.** Three independent records agree: the mail server's transaction log
and stored message, the sender's own Sent folder, and the **network capture**, which
contains the complete SMTP dialogue — `MAIL FROM`, `RCPT TO`, `DATA`, the full
message headers, and the server's `250 Ok: queued as LXL001`.

**How the absence of an attachment was established.** Not by looking at the
interface — the compose window, the Sent folder and the recipient field all
indicated a completed send. **By measurement.** A text-only control message sent on
23 October was **415 bytes**; this message is **424 bytes**. A 2,212-byte PDF would
have produced a message of roughly **3,600 bytes**. It is 424.

> **This is the case's clearest methodological lesson.** The most dangerous errors
> are not failed collections; they are successful-looking ones. **An artefact is
> verified by measurement against a known value, or it is not verified.**

**What the email does establish.** An external communication, to a different
organisation, on a subject line referring to the material under examination, sent
by the subject's corporate account, **160 seconds before the archive was uploaded
to the cloud service**.

**Reading the two together.** The email carries no data; the upload carries all of
it. **On this evidence the email is the notification and the upload is the
delivery.** That reading is an inference, is consistent with the counter-hypothesis
of normal correspondence, and is stated as inference.

### 6.12 Q12 — Whether the email evidence establishes a human sender

**Finding. No.** The email evidence establishes that a message **existed in a local
mail store** and **was transmitted from an account** by a mail client. **An account
is not a person; a client is not a human.**

The `User-Agent: Mozilla Thunderbird` header identifies software. The From address
identifies an account. Neither identifies who composed the text or pressed send.
**To move from account to person requires evidence outside digital forensics** —
physical access records, workstation camera footage, badge data, or admission.

### 6.13 Q13 — Whether data was transmitted to an external network service

**Finding. Yes.** An 8,529-byte HTTP `POST /upload` was made from AST-WKS-0471 to
a web service at `172.16.167.1:8080` at **17:03:41.119 IST**, and the service
recorded storing **8,296 bytes** with SHA-256 `9c75f0db…037074b`.

**Evidence — four records that agree across three systems:**

| Record | Time | Value |
|---|---|---|
| Packet capture, frame 159 | 17:03:41.119 | `POST /upload`, `Content-Length` **8,529**, response **200** |
| Service access log | 17:03:41.138 | `bytes_in` **8,529**, `bytes_stored` **8,296**, `status` 200 |
| **Service's stored copy, hashed directly** | — | **`9c75f0db…037074b`** |
| USB image, `icat` inode 17 | 16:56:28 (FAT) | `9c75f0db…037074b` |

**The third row is what makes this finding stand without inference.** The service's
own copy of the uploaded file is retained in exhibit E-008 and was hashed by the
examiner directly, rather than accepted from the service's logged assertion.

**The triangle, all three legs hashed by the examiner from three separate exhibits:**

| Object | Exhibit | Method | SHA-256 |
|---|---|---|---|
| Original on the workstation | E-001 | `icat`, inode **123858** | `9c75f0db…037074b` |
| Copy on the removable device | E-002 | `icat`, inode **17** | `9c75f0db…037074b` |
| Copy retained by the service | E-008 | `shasum`, direct | `9c75f0db…037074b` |

**No service assertion, no inference, no single point of failure.** Three independent
extractions of three separate physical objects produced the same 8,296 bytes. The
cloud service's logged hash agrees with all three, but **the finding does not depend
on that agreement** — which is the difference between evidence and corroboration.

**The 233-byte difference between 8,529 and 8,296 is the multipart envelope** —
boundaries and part headers — and is itself evidence that a file was carried inside
a form submission rather than posted as a bare body.

**The strongest correlation in the case.** The same 8,296 bytes left the machine by
two routes that had no knowledge of each other — removable media, and an HTTP
upload — and **the same hash was recorded on both sides.** This is a fact, not an
inference.

**Sequence preceding the upload, from the capture:**

```
17:02:25.206  GET /            200      browser reaches the service
17:03:22.428  POST /login      302      login accepted (redirect on success)
17:03:22.517  GET /upload      200      upload form served
17:03:41.119  POST /upload     200      8,529 bytes submitted
```

### 6.14 Q14 — Whether the cloud evidence establishes authorship

**Finding. No — and the evidence that comes closest is a network artefact, not the
service log.**

The service's access log records an IP address, a timestamp, byte counts and a
user agent. **It does not record a user.** The account used was identified only
from the packet capture, which contains the login submission **in cleartext**
because the service operates over HTTP rather than TLS:

- the account is a **personal webmail address**, not the corporate account used for
  the email in §6.11;
- the credential was transmitted unprotected and is recorded in the case file but
  **redacted from this report**.

**What this establishes.** That a browser session authenticated to the service and
uploaded the archive. **A session is not an identity.** The chain
`artefact → process → session → account → human` terminates in **inference** at the
final step.

**What this establishes for the client, positively.** The use of a personal account
on a corporate machine, in combination with the timing, is a legitimate matter for
an employer's investigation. **It is not, on its own, proof that any particular
person performed the upload.**

> **Incidental finding, reported because it matters to the client.** The service
> accepted authentication over unencrypted HTTP. Had Asterion's own systems
> behaved the same way, credentials would be exposed to any party on the path.
> **This is a security observation about the external service, not about Asterion.**

### 6.15 Q15 — Whether there was an attempt to remove or conceal evidence

**Finding.** The staging folder was deleted at **17:06:37.579 IST** by a method
that bypasses the Recycle Bin, and browsing history for the service was partially
cleared. **The archive itself was not deleted from the USB device.**

**Evidence — the deletion, corroborated to the millisecond by two independent
sources:**

```
$UsnJrnl    hard-link removal ×2 + rename    17:06:37.579
Sysmon      FileDelete ×5                    17:06:37.579
```

**Evidential significance of the agreement.** The change journal and the event log
are written by different Windows subsystems at different times for different
purposes. **Their agreement to the millisecond is not a coincidence and cannot be
produced by a simulation artefact**; it is what two independent recorders of the
same event look like.

**The contemporaneous note recorded this event as 17:06:42 — 4.4 seconds late.
The artefact record is preferred**, and the note is retained unaltered in the case
file.

**Concealment assessed against the counter-hypothesis.** Deleting a temporary
working folder is ordinary housekeeping, and **the evidence does not distinguish
housekeeping from concealment**. Three points bear on it and none is conclusive:

1. the folder was deleted **after** the archive had been uploaded and the device
   written — the order that matters if concealment was the object, and equally the
   order produced by tidying up when finished;
2. deletion **bypassed the Recycle Bin**, which is a deliberate act rather than a
   default;
3. **the archive was left on the USB device**, which a person concealing evidence
   would not do.

**Point 3 is the strongest argument against concealment**, and it is stated for that
reason.

**Point 4 — and it cuts the other way.** The browsing record of the external service
has been removed from the browser profile *entirely*: `moz_places` contains no entry
for the service at all, not merely a missing visit row (§6.15.1). **Deleting a
history entry is a routine menu action. Removing the place row as well is not what
the interface offers.** That asymmetry is recorded against the counter-hypothesis of
routine housekeeping.

**The concealment finding is therefore assessed MEDIUM-HIGH**, raised from MEDIUM on
the strength of §6.15.1.

#### 6.15.1 The browser profile holds no record of the external service

| Source | Records Firefox accessing the service |
|---|---|
| Packet capture, frames 108–175 | `Firefox/158.0` — 22 Oct, 23 Oct, 30 Oct |
| Service access log `access.jsonl` | same user agent, three dates |
| Sysmon process records | `firefox.exe` launched 17:02:19.493 |
| **`places.sqlite` `moz_places`** | **nothing. No row for `172.16.167.1:8080`.** |

**All 23 surviving history visits are dated 21 October 18:23–18:59** — the VM build.
The profile records the internal case-data server on port 8000 and says nothing
whatsoever about the external service on port 8080.

**Two supporting facts, each independently established:**

- **The write-ahead log is zero bytes**, so the database had been checkpointed and
  closed cleanly — **there are no unmerged writes hiding the records.**
- **The file contains 3.5 MB beyond its logical page count, and that region is
  entirely null** — so the records are not recoverable from unused space either.
  Tested, not assumed: no occurrence of `8080`, `nimbusshare` or `atlas_backup`
  appears anywhere in the raw file.

**The time of the clearing is not recoverable and is not stated.**

**Consequence for the case, stated plainly:** the browser can no longer corroborate
the upload. **That finding rests on the packet capture and the service's log**, which
is precisely why the three-way hash equality in §6.13 carries the weight it does.

**A limit of this examination.** Sysmon event ID 26 (file delete, recording the
deleting *process*) is **not enabled** in this workstation's configuration. Its
absence is a **configuration gap, not an absence of the event**, and the five EID 23
records carry the deletion regardless.

### 6.16 Q16 — Whether apparently suspicious activity is attributable to system or scheduled processes

**Finding. One piece of apparently suspicious activity is attributable to a
scheduled system process and must not be attributed to the subject.**

At **16:45:28 IST** a scheduled backup task fired, running as `SYSTEM`, outside the
subject's session. Its configuration shows it operates on `Documents\Backup` — **the
staging folder**. On its face this is the strongest-looking artefact in the case:
a system process touching the folder where the material was collected.

**It is not evidence of user activity.**

| Indicator | Value |
|---|---|
| Task | AtlasBackup — scheduled task |
| Account | **SYSTEM**, not the subject |
| Logon type | service logon, not interactive |
| LastTaskResult | **2** — no files copied (destination already current) |
| Timing | fired **after** the subject's own staging (16:41–16:42) |

**Assessment.** The task ran, achieved nothing, and is **system activity**. It is
reported because a reviewer who found it without this analysis would draw the wrong
conclusion, and because **demonstrating the difference between system and user
activity is a core examiner skill**.

**A limitation of that day's record.** The task had been scheduled to fire earlier
but the guest machine was powered off at that time; it was therefore started
manually from an elevated session. **The execution path was manual even though the
process identity was SYSTEM.** This is disclosed rather than glossed: the
attribution to SYSTEM is sound, but the *trigger* was the examiner's, not the
scheduler's, and the case design's intent (an autonomous scheduled event) was not
fully realised.

### 6.17 Q17 — Fact, inference, and undetermined

| # | Proposition | Status | Basis |
|---|---|---|---|
| 1 | Four identified files were opened on AST-WKS-0471 on 30 Oct 2026, 16:35–16:39 | **FACT** | Shell items, jump lists, `$MFT` |
| 1a | The folders `C:\Asterion`, `Documents\Backup` and `E:\` were navigated in Explorer on 30 Oct 2026, the last within 2.6 s of the first copy | **FACT** | ShellBags (`BagMRU`), §6.3.1 |
| 2 | A folder `Documents\Backup` was created at 16:40:15.490 and four files copied into it | **FACT** | `$UsnJrnl`, Sysmon 11 |
| 3 | A password-protected archive was created at 16:48:47.643 containing exactly those four files | **FACT** | Sysmon 1, decryption, 4/4 hash match |
| 4 | Three items were copied to the USB device at 16:56:28–16:56:52 | **FACT** | Sysmon 11, FAT timestamps, hashes |
| 5 | The USB copy of the archive is byte-identical to the file uploaded to the cloud service | **FACT** | SHA-256 equality |
| 6 | A 424-byte message with no attachment was sent to `s.varma@novaedge.example` at 17:01:01 | **FACT** | Three records, incl. full SMTP dialogue |
| 7 | The staging folder was deleted at 17:06:37.579 | **FACT** | `$UsnJrnl` + Sysmon, to the ms |
| 7a | **No record of the external service survives in the browser profile** — no place row, no visit row — although four other records show Firefox accessing it | **FACT** | `moz_places` + PCAP + `access.jsonl`, §6.15 |
| 7b | The session **ended by logoff at 17:13:32**, it did not lock — no `4800` exists in the window | **FACT** | Security 4647 + Sysmon reboot, §6.16 |
| 8 | Corporate data left the workstation by two routes | **FACT** | Items 4, 5 and 6 together |
| 9 | The email was a notification for the upload rather than a delivery | **INFERENCE — MEDIUM** | Timing, absence of attachment, subject line |
| 10 | The selection of files was deliberate rather than incidental | **INFERENCE — MEDIUM** | Selectivity at two levels; no counter-evidence |
| 11 | The deletion was an attempt to conceal | **INFERENCE — MEDIUM** | Order, Recycle-Bin bypass; archive retained argues against |
| 12 | The subject personally performed these acts | **UNDETERMINED** | Account ≠ person |
| 13 | The subject intended to harm the company | **UNDETERMINED** | No evidence of motive in digital artefacts |
| 14 | The material reached the recipient named in the email | **UNDETERMINED** | No visibility beyond Asterion's boundary |

### 6.18 Q18 — What the client may lawfully state

**The client may state, on this evidence:**

- that identified company documents were collected into a staging folder on
  AST-WKS-0471 on 30 October 2026 and compressed into a password-protected archive;
- that the archive, or a byte-identical copy, was copied to a removable USB device
  and separately uploaded to an external web service;
- that the staging folder was subsequently deleted by a method that bypasses the
  Recycle Bin;
- that a message was sent from the subject's corporate account to an external
  address referring to the material, carrying no attachment.

**The client may not state, on this evidence alone:**

- that the subject personally performed any act — **an account is not a person**;
- that the subject acted with intent to harm, or with any particular motive;
- that any data reached the recipient organisation;
- that the deletion was a concealment rather than housekeeping.

**Form.** Electronic records produced in support of these statements require
certification under **s.63 of the Bharatiya Sakshya Adhiniyam, 2023** (§8), with
hash values and algorithm disclosed in the Schedule format. **No certificate is
produced or claimed in this simulated examination**, and no lawful custodian for
Part A exists within it.

---

## 7. TIMELINE AND CORRELATION

### 7.1 Method

Artefacts were read from their primary sources and only then assembled into a
timeline. **Where two sources disagreed, the disagreement is recorded rather than
resolved by preference** (§7.4). The full table of 27 rows is at
`02_ground_truth/ACTUAL_TIMELINE_30Oct.csv`; a condensed form follows.

### 7.2 Consolidated timeline — 30 October 2026

![Figure 4 — Ninety minutes in twelve records](diagrams/01_incident_timeline.png)


| IST | UTC | Event | Source |
|---|---|---|---|
| 16:04:38 | 10:34:38 | USB device registered with the host | registry |
| 16:05:26 | 10:35:26 | `System Volume Information` created on device | FAT |
| 16:07:24 | 10:37:24 | `probe.txt` written then deleted (examiner) | FAT |
| 16:08:53 | 10:38:53 | `Sysmon/` folder created on device (examiner) | FAT |
| 16:26 | 10:56 | Network capture started | `capinfos` |
| 16:31:46 | 11:01:46 | Interactive logon, LogonId `0x109b61f` | Security 4624 |
| 16:32:38 | 11:02:38 | Second logon, `0x1286858` — carries all incident activity | Security 4624 |
| 16:33:32 | 11:03:32 | `.fseventsd` written by macOS | FAT |
| 16:33:37 | 11:03:37 | Device mounted as `E:` | registry + FAT |
| 16:35–16:39 | 11:05–11:09 | Four documents opened and closed | Shell items |
| 16:40:15.490 | 11:10:15.490 | Staging folder `Documents\Backup` created | `$UsnJrnl` |
| 16:41:13.006 | 11:11:13.006 | File 1 → staging | Sysmon 11 |
| 16:41:31.899 | 11:11:31.899 | File 2 → staging | Sysmon 11 |
| 16:41:53.311 | 11:11:53.311 | File 3 → staging | Sysmon 11 |
| 16:42:14.880 | 11:12:14.880 | File 4 → staging | Sysmon 11 |
| 16:45:28 | 11:15:28 | Scheduled task fires as SYSTEM, result 2 | task log |
| **16:48:47.643** | 11:18:47.643 | **`7z a -t7z -p<redacted>` executed** | Sysmon 1 |
| 16:48:48.336 | 11:18:48.336 | Archive written, 8,296 B | `$UsnJrnl` |
| 16:49:04.019 | 11:19:04.019 | `7z l` — archive listed | Sysmon 1 |
| 16:56:28.595 | 11:26:28.595 | `Atlas_backup.7z` → `E:` | Sysmon 11 + FAT |
| 16:56:40.113 | 11:26:40.113 | `Client_Master_List.xlsx` → `E:` | Sysmon 11 + FAT |
| 16:56:52.806 | 11:26:52.806 | `Q4_Financial_Model.xlsx` → `E:` | Sysmon 11 + FAT |
| **17:01:01.642** | 11:31:01.642 | **SMTP session opens** | PCAP |
| 17:01:01 | 11:31:01 | Message sent, 424 B, no attachment | sink + Sent mbox |
| 17:01:07.257 | 11:31:07.257 | SMTP session closes | PCAP |
| 17:02:25.206 | 11:32:25.206 | `GET /` → 200 | PCAP |
| 17:03:22.428 | 11:33:22.428 | `POST /login` → 302 | PCAP |
| 17:03:22.517 | 11:33:22.517 | `GET /upload` → 200 | PCAP |
| **17:03:41.119** | 11:33:41.119 | **`POST /upload` → 200, 8,529 B** | PCAP |
| 17:03:41.138 | 11:33:41.138 | Service stores 8,296 B, SHA-256 recorded | access log |
| **17:06:37.579** | 11:36:37.579 | **Staging folder deleted (5 events)** | `$UsnJrnl` + Sysmon 23 |
| 17:09:08–17:09:10 | 11:39:08–11:39:10 | 10 connection attempts to :8000, all refused | PCAP |
| ~17:09:11 | ~11:39:11 | Firefox history partially cleared | browser |
| 17:10:35 | 11:40:35 | Device removed | registry |
| 17:13:32 | 11:43:32 | **Session ended — user logoff (`4647`); no `4800`, so it did not lock** | Security |
| 17:12 | 11:42 | Capture stopped, 218 packets, 0 dropped | `capinfos` |

### 7.3 The correlation chains, drawn explicitly

**The USB chain:**

```
Shell items        → four documents opened 16:35–16:39          FACT
ShellBags          → C:\Asterion opened 16:41:22                 FACT
ShellBags          → Documents\Backup held Atlas_backup.7z 16:54:41  FACT
ShellBags          → E:\ navigated 16:56:26                     FACT
$UsnJrnl           → staging folder created 16:40:15.490        FACT
Sysmon 11 ×4       → four files copied 16:41:13–16:42:14        FACT
Sysmon 1           → 7z archive created 16:48:47.643            FACT
py7zr + SHA-256    → 4/4 members match the four originals       FACT
Sysmon 11          → archive and two xlsx copied to E:           FACT
E-002 FAT + icat   → same files present on the device, same hash FACT
------------------------------------------------------------------
→ company data was copied to removable media during this session
                                                        INFERENCE, HIGH
```

**The cloud chain:**

```
PCAP frame 159     → POST /upload 17:03:41.119, 8,529 B, 200      FACT
access.jsonl       → bytes_in 8,529, bytes_stored 8,296           FACT
access.jsonl       → sha256 = 9c75f0db…037074b                    FACT
icat E-002 inode17 → sha256 = 9c75f0db…037074b                    FACT
------------------------------------------------------------------
→ the file uploaded to the service is byte-identical to the file
  on the USB device                                              FACT
→ the uploaded archive is the one created at 16:48:47.643        INFERENCE, HIGH
```

**Eight bytes of hash, recorded by two systems with no knowledge of each other.**
This is the case's principal finding.

### 7.4 Where artefacts disagree, and why that is expected

| Discrepancy | Cause | Treatment |
|---|---|---|
| Note 17:06:42 vs artefacts 17:06:37.579 | human note written after the fact, ~4.4 s late | artefact preferred; note retained |
| Note "~5 s apart" vs 24.2 s actual | misjudged interval | corrected; original retained |
| FAT 2-second precision vs NTFS 100 ns | filesystem design | FAT used only where corroborated |
| FAT local time, no timezone | FAT32 stores no offset | agreement with Sysmon resolves it |
| `$SI` vs `$FN` timestamp variance | **artificial ageing of simulated documents** | simulation artefact, **not** anti-forensic activity (§9.5) |

**A perfectly consistent timeline would be suspicious.** Recorded discrepancies of
seconds, and precision differences between filesystems, are what real examinations
produce.

---

## 8. ADMISSIBILITY — BHARATIYA SAKSHYA ADHINIYAM, 2023

### 8.1 The requirement

Section 63 BSA 2023 replaced s.65B of the Indian Evidence Act and came into force
on **1 July 2024**. Electronic records offered as secondary evidence require a
**certificate in the Schedule format**, signed in **two parts** — Part A by the
custodian of the device, Part B by an expert — and the certificate must disclose
the **hash value and the algorithm used**. The Supreme Court has upheld the
mandatory character of s.63(4) certification.

### 8.2 Records produced by this examination

| Record | Type | Particulars required | Hash |
|---|---|---|---|
| E-001 workstation image | Secondary — copy of storage | device particulars, hash, algorithm, Part A + B | `57ac362d…f9ea5c` |
| E-002 USB image | Secondary — copy of storage | as above | `2ae0d727…130f29` |
| E-003 network capture | Original, born-digital | capture conditions, hash, tool | `92545c31…9ad0cc` |
| E-004 incident email | Original, born-digital | origin, hash | `a143595a…e6085` |
| E-008 access log | Original, born-digital | origin, hash | `2df6a57e…c3f905` |
| Derived extracts (E-011) | Secondary — derived | provenance to E-001, tool and version, hash | per manifest |

### 8.3 Simulation boundary

> In a live engagement Part A would be executed by the custodian of the source
> device and Part B by an expert as defined under s.63(4). **In this simulated
> examination no lawful custodian exists, and no certificate is produced or
> claimed.** The records above are identified so that a live engagement could be
> certified without re-examination.

### 8.4 Why the hash values matter

Hashing is not a technical nicety. **It is the mechanism by which a copy is
connected to an original** — the difference between "a file called
`Atlas_backup.7z`" and "the file." Every principal finding in this report turns on
a hash equality, and each equality is recorded from a source that had no knowledge
of the other.

---

## 9. LIMITATIONS

### 9.1 Scope limitations

The examination was **targeted collection, not full-disk content review**. No
unallocated-space, slack-space or volume-shadow analysis was performed. **Deleted
content that was never written to a named file is not examined here.**

### 9.2 Method limitations

- **No hardware write-blocker was used.** Software unmounting was the control.
  This is disclosed without qualification. The 31 October hash mismatch was caused
  by the source volume being mounted during imaging, and was resolved by repeating
  the acquisition with it unmounted — `2ae0d727…130f29`, matching.
- **The workstation was imaged after power-down.** Volatile memory, running
  processes and network state at the time of the incident are unavailable. The
  30 October network capture partly compensates.
- Two logons exist (§6.1); findings are attributed to the **session** carrying the
  activity, not to the user globally.

### 9.3 Data limitations

- The cloud service operated over **unencrypted HTTP**. This is the best case for
  examiner visibility and the worst case for realism; a TLS service would have
  hidden the login entirely.
- The email carried **no DKIM signature**; its authenticity is established by the
  capture and the server log, not cryptographically.
- **FAT32 timestamps** are local-time with 2-second precision and no timezone.
  Where they are relied on, they are corroborated (§6.9).

### 9.4 Tool limitations, per finding

| Tool | Limitation | Affected finding | Consequence |
|---|---|---|---|
| `evtx_window.py` | does not extract `DestinationPort` | §6.13 | none — PCAP supplies it |
| `python-evtx` | non-ISO timestamp format | all log timings | none — normalised and cross-checked |
| Sysmon config | EID 26 not enabled | §6.15 | deleting *process* not recorded; event itself proven |
| FAT32 | 2 s, local time | §6.9–6.10 | resolved by corroboration |
| `regipy` 6.5.0 | does not decode shell items to paths; returns hex, needs manual extraction | §6.3.1 | folder names recovered as fragments; **two paths not decoded** |

### 9.5 Simulation artefacts

Document timestamps were artificially aged during scenario construction using .NET
file-time properties, which write to `$STANDARD_INFORMATION` but not to
`$FILE_NAME`. **The resulting `$SI`/`$FN` discrepancy is an artefact of simulation
design and must not be interpreted as subject anti-forensic activity.**

### 9.6 Exhibits carrying non-case material

**The USB device was not blank when it entered the case.** Its filesystem contains
macOS and Android artefacts — `.Spotlight-V100`, `.fseventsd`, a
`$OrphanFiles/DATA` tree from an Android file manager — predating the case. These
are recorded as **pre-existing examiner activity and prior personal use of the
medium**, are excluded from all findings, and are disclosed so that a reader is not
misled about the medium's provenance.

Three further items on the device fall inside the case window and are **recorded as
unattributed**:

| Item | Time | Status |
|---|---|---|
| `probe.txt`, written then deleted | 16:07:24 | examiner health-gate activity |
| `Sysmon/` folder, and a hash-named file containing `??probe` | 16:08:53 | **unexplained — not attributed** |
| USB activity from 16:04:38, ~27 min before the subject's logon | 16:04–16:08 | **examiner pre-flight, per the examiner's record** |

**The last item is disclosed because the artefact alone cannot distinguish examiner
preparation from subject activity** — only the examiner's contemporaneous record
can. That is a limitation of the *log*, and a reason why contemporaneous notes are
an evidentiary requirement.

### 9.7 Unattributed network traffic

Between **17:09:08 and 17:09:10**, ten `SYN` packets from two alternating source
ports to `172.16.167.1:8000` were each answered with `RST+ACK`. **No session was
established and no data transferred.** The process responsible is **not identified**
and the activity is **not attributed**. It is recorded because leaving it out of a
capture summary would be a misdescription of the capture.

---

## 10. CONCLUSION

**What was established.** Company documents were selected from two folders carrying
classification markings, collected into a staging folder on the workstation,
compressed into a password-protected archive, and removed by **two independent
routes** — a removable USB device and an upload to an external web service. The two
routes carry **the same file, proved by hash from both ends.** The staging folder
was then deleted by a method that bypasses the Recycle Bin. A message referring to
the material was sent from the subject's corporate account to an external
organisation, **carrying no attachment.**

**What was not established.** Who was at the keyboard. Why the material was taken.
Whether the deletion was concealment or housekeeping. Whether any data reached the
recipient organisation.

**What would resolve the remainder.** Physical and access-control records
establishing who was present at AST-WKS-0471 during 16:30–17:15 on 30 October;
the recipient organisation's own records; and, if available, the subject's account
of the material's purpose. **None of these is a digital artefact, and no further
examination of this evidence will produce them.**

---

## 11. EXAMINER'S DECLARATION

I declare that this examination was conducted by me; that the evidence was acquired,
handled and stored as documented in the chain of custody; that the tools used are
identified in §5 with the tests performed against known values; that findings are
distinguished from inferences and both from undetermined matters; that discrepancies
between sources are recorded rather than resolved in favour of a preferred
narrative; and that I am able to explain and defend each finding in this report.

I further declare that this report describes a **simulated case** constructed for
training and assessment, that no real individual's data is present, and that it is
not a legal document.

**Aditya Pandey** — Examiner
Date: 12 November 2026

---

## APPENDICES

**A — Tool inventory.** The Sleuth Kit 4.12 · `python-evtx` 0.8.1 · `py7zr` 1.1.4 ·
`regipy` · `tshark` 4.x · Plaso · `usn_parse.py` and `evtx_window.py` (custom,
in-repo) · 7-Zip.

**B — Hash manifest.** `case_file_manifest.csv`.

**C — Chain of custody.** `00_case/CHAIN_OF_CUSTODY.md`.

**D — Master timeline.** `02_ground_truth/ACTUAL_TIMELINE_30Oct.csv` (27 rows).

**E — Acquisition commands.** `ACQUISITION_RECORD_31Oct.md`.

**F — Findings matrix and question set.** `00_case/CASE_DOSSIER.md` §3,
`06_report/FINDINGS_MATRIX_template.md`.

**G — Ground truth comparison.** `05_findings/GROUNDTRUTH_VS_FINDINGS_30Oct.md`.

---

`SIMULATED / ACADEMIC CASE — NOT FOR LEGAL USE`
