#!/usr/bin/env python3
"""Recover the USBSTOR identity from a SYSTEM hive and compare it to the
hardware reference. regipy 6.x API. Read-only; prints, never writes."""
import sys
from regipy.registry import RegistryHive
from regipy.utils import convert_wintime

REF = "<DEVICE_SERIAL_REDACTED>"     # recorded from ioreg 17 Oct 2026, before the scenario;
                                        # redacted for publication - see CASE_NOTICE.md

def subkeys(k):
    try:
        return list(k.iter_subkeys() or [])
    except Exception as e:
        print("    [subkey read error:", e, "]"); return []

def values(k):
    try:
        return list(k.iter_values(trim_values=False))
    except Exception as e:
        print("    [value read error:", e, "]"); return []

def lw(k):
    try:
        return convert_wintime(k.header.last_modified, as_json=False)
    except Exception:
        return "?"

def dump(k, indent="    "):
    print(f"{indent}instance : {k.name!r}   lastwrite {lw(k)}")
    for v in values(k):
        val = v.value
        if isinstance(val, (bytes, bytearray)) and len(val) > 200:
            val = f"<{len(val)} bytes>"
        print(f"{indent}  {v.name} = {val!r}")

hive = RegistryHive(sys.argv[1] if len(sys.argv) > 1 else "SYSTEM")
cur = hive.get_key("\\Select").get_value("Current")
cs = "\\ControlSet%03d" % cur
print(f"Select\\Current = {cur}  ->  {cs}\n")

print("=== Enum\\USBSTOR — class keys VERBATIM ===")
for cls in subkeys(hive.get_key(cs + "\\Enum\\USBSTOR")):
    print("  class key:", repr(cls.name))
    for inst in subkeys(cls):
        dump(inst)
        for sub in subkeys(inst):          # Device Parameters, Properties
            print(f"    subkey   : {sub.name!r}")
            dump(sub, indent="      ")

print("\n=== Enum\\USB\\VID_0781&PID_55A9 — VERBATIM ===")
for cls in subkeys(hive.get_key(cs + "\\Enum\\USB")):
    if "0781" in cls.name.upper():
        print("  class key:", repr(cls.name))
        for inst in subkeys(cls):
            dump(inst)

print("\n=== COMPARISON vs 17 Oct hardware reference ===")
found = []
for cls in subkeys(hive.get_key(cs + "\\Enum\\USBSTOR")):
    for inst in subkeys(cls):
        if inst.name == REF:
            found.append((cls.name, inst.name))
if found:
    print("  MATCH — reference serial recovered from the registry")
    for c, i in found:
        print(f"    {c!r}  /  {i!r}")
else:
    print("  NO MATCH — stop. Do not look for a near-miss string.")
