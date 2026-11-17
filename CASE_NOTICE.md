# Case notice

**This repository documents a simulated forensic examination.**

- Every person, company, address, credential, document and event is **fictional**.
- The environment was constructed for this exercise and executed by the examiner.
- No real individual's data is present, and no real incident is described.
- This is **not a legal document**, and nothing here is a legal opinion.
- Findings relate to a **simulated** case and carry no weight in any real matter.

## What is deliberately absent

| Excluded | Why |
|---|---|
| Disk images, memory captures, packet captures, mailbox files | Size, and the privacy habit a reviewer is actually assessing |
| Raw registry hives, event logs, `$MFT`, `$UsnJrnl` | Same — and they contain the case answer |
| The device hardware serial | A physical identifier tied to a real device, of no analytical value to a reader |
| The archive and service passwords | Publishing a credential teaches nothing and normalises publishing credentials |
| The sealed ground-truth file | Publishing the answer key would destroy the blind test |

## What is present

Everything needed to judge the work: the report, the measurement of the
report's own accuracy against the sealed answer key, the parsers used, and the
service that generated the cloud record. Every hash in the report is of a
synthetic file.

`SIMULATED / ACADEMIC CASE — NOT FOR LEGAL USE`
