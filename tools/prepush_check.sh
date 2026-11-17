#!/usr/bin/env bash
# Run before every `git push` on this repository.
#
# Checks the two things that actually go wrong on a forensic portfolio repo:
#   1. evidence files staged for commit
#   2. identifiers and credentials in text
#
# Usage:  bash tools/prepush_check.sh

set -uo pipefail
fail=0

echo "== evidence files in the working tree =="
if find . -path ./.git -prune -o -type f \
     \( -name '*.dd' -o -name '*.raw' -o -name '*.E01' -o -name '*.e01' \
        -o -name '*.vmem' -o -name '*.vmdk' -o -name '*.pcap' -o -name '*.pcapng' \
        -o -name '*.eml' -o -name '*.mbox' -o -name '*.jsonl' -o -name '*.evtx' \
        -o -name '*.hive' -o -name 'places.sqlite' -o -name '*.7z' \
        -o -name '*.xlsx' \) -print | grep -q .; then
  echo "  FAIL - evidence or case files present:"
  find . -path ./.git -prune -o -type f \
     \( -name '*.dd' -o -name '*.raw' -o -name '*.pcap' -o -name '*.eml' \
        -o -name '*.jsonl' -o -name '*.evtx' -o -name '*.7z' \) -print | sed 's/^/    /'
  fail=1
else
  echo "  ok - none"
fi

echo "== identifiers and credentials in tracked text =="
# The device serial, both passwords, and any obvious plaintext credential fragment.
PATTERNS='03025409071825155737|Asterion2026|hi%40123|hi@123|password=[A-Za-z0-9]'
if git grep -nEI "$PATTERNS" -- . ':(exclude)tools/prepush_check.sh' 2>/dev/null | grep -q .; then
  echo "  FAIL - matches found:"
  git grep -nEI "$PATTERNS" -- . ':(exclude)tools/prepush_check.sh' | sed 's/^/    /'
  fail=1
else
  echo "  ok - none"
fi

echo "== classification footer present in the report =="
if grep -q "SIMULATED / ACADEMIC CASE — NOT FOR LEGAL USE" report/LXL-DFIR-001_REPORT.md 2>/dev/null; then
  echo "  ok"
else
  echo "  FAIL - classification marking missing from the report"
  fail=1
fi

echo
[ "$fail" -eq 0 ] && echo "PASS - safe to push" || echo "FAIL - do not push"
exit "$fail"
