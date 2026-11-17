#!/usr/bin/env python3
"""Print event-log records inside a time window (given in IST), for chosen EventIDs.

The file stores times in UTC. Everything here is converted so you always type and
read IST. Read-only.

Usage:
  python3 evtx_window.py <file.evtx> <start "YYYY-MM-DD HH:MM"> <end> [EID ...]
"""
import sys, datetime, xml.etree.ElementTree as ET
from Evtx.Evtx import Evtx

NS  = "{http://schemas.microsoft.com/win/2004/08/events/event}"
IST = datetime.timedelta(hours=5, minutes=30)

def parse_ist(s):
    return datetime.datetime.strptime(s, "%Y-%m-%d %H:%M") - IST   # -> naive UTC

def main():
    path  = sys.argv[1]
    start = parse_ist(sys.argv[2]); end = parse_ist(sys.argv[3])
    want  = {int(x) for x in sys.argv[4:]}
    shown = seen = bad = 0
    first = last = None
    with Evtx(path) as log:
        for rec in log.records():
            seen += 1
            try:
                root = ET.fromstring(rec.xml())
            except Exception:
                bad += 1
                continue
            sysn = root.find(NS + "System")
            eid  = sysn.find(NS + "EventID")
            tc   = sysn.find(NS + "TimeCreated")
            if eid is None or tc is None:
                continue
            eid = int(eid.text)
            stamp = datetime.datetime.strptime(tc.get("SystemTime")[:19], "%Y-%m-%dT%H:%M:%S")
            if first is None: first = stamp
            last = stamp
            if not (start <= stamp <= end):
                continue
            if want and eid not in want:
                continue
            shown += 1
            data = {}
            ed = root.find(NS + "EventData")
            if ed is not None:
                for d in ed:
                    data[d.get("Name") or "?"] = (d.text or "")
            keep = ("Image","CommandLine","TargetFilename","UtcTime","User","LogonId",
                    "EventType","RuleName","Device","DeviceDescription","ClassName",
                    "DestinationIp","Protocol","SourceImage","TargetObject","Details")
            bits = " ".join(f"{k}={data[k]}" for k in keep if data.get(k))
            print(f"{(stamp+IST).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}  EID {eid:<5} {bits[:300]}")
    print(f"\n# {path}")
    print(f"# records: {seen:,}   shown: {shown:,}   unparseable: {bad:,}")
    if first:
        print(f"# log range (IST): {(first+IST)} .. {(last+IST)}")
    if seen == 0:
        print("# ZERO records read - wrong file or unsupported format. Not evidence of absence.")

if __name__ == "__main__":
    main()
