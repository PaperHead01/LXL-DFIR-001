# Diagrams

Five figures. **All generated from source with PIL — none AI-generated.** That is
deliberate: every registry path, hash prefix and byte count in these images is
literal, and an image model will silently corrupt a hex string.

Regenerate them all with one command:

```bash
python3 tools/make_diagrams.py      # writes ./diagrams/*.png
```

**One script, five figures, no dependencies beyond Pillow.** Every figure is built
from literal strings in that file, so what you see in the image is what is in the
source.

| File | Shows | Read it for |
|---|---|---|
| `01_incident_timeline.png` | The twelve records that reconstruct 90 minutes, 16:31 → 17:10 IST | What a reconstructed timeline looks like when each row has a source |
| `02_four_recorders.png` | Four exhibits, four recording mechanisms, converging on one conclusion — and what they still don't prove | Why correlation is stronger than any single artefact |
| `03_hash_correlation.png` | The same 8,296 bytes leaving by two routes, hashed identically at both ends | The case's principal finding, in one image |
| `04_usbstor_uas_binding.png` | Why `Enum\USBSTOR` was empty for a device that was definitely connected | The false negative that every USB checklist hits |
| `05_usbstor_uas_wide.png` | The same, wide format | Presentation use |

## The two that matter when presenting

**02** answers "why should I believe a single finding?" — because four systems that
could not talk to each other agree.

**04** answers "what does this examiner know that a checklist doesn't?" — the most
relied-on Windows USB artefact can be legitimately, silently absent on modern
hardware.

## Marking

Every figure carries `SIMULATED ACADEMIC CASE · LXL-DFIR-001` in the footer. **No
figure carries the device serial, a password, or any ground-truth value.**
