#!/usr/bin/env python3
"""USN_RECORD v2 parser for NTFS $UsnJrnl:$J. Read-only.
Skips zero (sparse/unused) regions in 4 KB blocks, so a 1 GB stream parses fast.
Prints ONLY records matching the filters (or the first --max with no filter)."""
import struct, sys, datetime

IST   = datetime.timedelta(hours=5, minutes=30)
EPOCH = datetime.datetime(1601, 1, 1)
ZBLK  = b"\x00" * 4096
R = [(0x1,"DATA_OVERWRITE"),(0x2,"DATA_EXTEND"),(0x4,"DATA_TRUNCATION"),
     (0x10,"FILE_CREATE"),(0x20,"FILE_DELETE"),(0x40,"EA_CHANGE"),
     (0x80,"SECURITY_CHANGE"),(0x100,"RENAME_OLD_NAME"),(0x200,"RENAME_NEW_NAME"),
     (0x400,"INDEXABLE_CHANGE"),(0x800,"BASIC_INFO_CHANGE"),(0x1000,"HARD_LINK_CHANGE"),
     (0x2000,"COMPRESSION_CHANGE"),(0x4000,"ENCRYPTION_CHANGE"),(0x8000,"OBJECT_ID_CHANGE"),
     (0x10000,"REPARSE_POINT_CHANGE"),(0x20000,"STREAM_CHANGE"),
     (0x40000,"TRANSACTED_CHANGE"),(0x80000000,"CLOSE")]

def rsn(m): return "|".join(n for b, n in R if m & b) or f"0x{m:08x}"
def ft(v):  return None if v == 0 else EPOCH + datetime.timedelta(microseconds=v // 10)

def parse(buf):
    n, off = len(buf), 0
    while off < n:
        # bulk-skip a whole 4 KB block of zeros (sparse region) in one C-level compare
        while off + 4096 <= n and buf[off:off+4096] == ZBLK:
            off += 4096
        if off + 60 > n:
            break
        length, major, _ = struct.unpack_from("<IHH", buf, off)
        if not (60 <= length <= 1024 and off + length <= n and 2 <= major <= 4):
            off += 8
            continue
        try:
            fre, par = struct.unpack_from("<QQ", buf, off + 8)
            usn = struct.unpack_from("<Q", buf, off + 24)[0]
            ts  = ft(struct.unpack_from("<Q", buf, off + 32)[0])
            r   = struct.unpack_from("<I", buf, off + 40)[0]
            nlen, noff = struct.unpack_from("<HH", buf, off + 56)
            if noff < 60 or off + noff + nlen > n:
                off += 8; continue
            name = buf[off+noff:off+noff+nlen].decode("utf-16-le", "replace")
        except Exception:
            off += 8; continue
        yield (ts, name, r, fre & 0xFFFFFFFFFFFF, par & 0xFFFFFFFFFFFF, usn)
        off += length

def main():
    args = [a for a in sys.argv[1:]]
    maxprint = 200
    if "--max" in args:
        i = args.index("--max"); maxprint = int(args[i+1]); del args[i:i+2]
    path = args[0]; filt = [s.lower() for s in args[1:]]

    buf = open(path, "rb").read()
    print(f"# {path}  {len(buf):,} bytes   filters={filt or 'NONE'}")
    tot = kept = 0; first = last = None
    for ts, name, r, fre, par, usn in parse(buf):
        tot += 1
        if first is None: first = ts
        last = ts
        if filt and not any(f in name.lower() for f in filt):
            continue
        kept += 1
        if kept <= maxprint:
            t = (ts + IST).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] if ts else "no-ts"
            print(f"{t} | {name!r:44} | {rsn(r):44} | file={fre} parent={par} usn={usn}")
    f_ = (first + IST).strftime("%Y-%m-%d %H:%M:%S") if first else "?"
    l_ = (last  + IST).strftime("%Y-%m-%d %H:%M:%S") if last  else "?"
    print(f"\n# records parsed: {tot:,}   matched: {kept:,}   range: {f_} .. {l_} (IST)")
    if kept > maxprint:
        print(f"# only first {maxprint} printed — raise with --max N")
    if tot == 0:
        print("# ZERO records — THE PARSE FAILED. This is not evidence of absence.")

if __name__ == "__main__":
    main()
