```bash
#!/usr/bin/env bash
# ----------------------------------------------------------------------------- #
#  audit_marketflock.sh  –  Audit & report on
#  /data/data/com.termux/files/home/projects/media/marketflock
#
#  Works in Termux / Android (Bash + coreutils packages).
#  Requires: bash, coreutils (du, find, stat, sha256sum), awk, sort, head, tail.
#
#  Usage:
#     chmod +x audit_marketflock.sh
#     ./audit_marketflock.sh
#
#  Results are written to:
#     $HOME/marketflock_audit_YYYYMMDD_HHMMSS.txt
# ----------------------------------------------------------------------------- #

set -euo pipefail

# ----------------------------------------------------------------------------- #
# Configuration
TARGET="/data/data/com.termux/files/home/projects/media/marketflock"
LOGDIR="$HOME"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
LOGFILE="$LOGDIR/marketflock_audit_${TIMESTAMP}.txt"

# ----------------------------------------------------------------------------- #
# Helper: safe printf (not strictly needed, but keeps the code tidy)
pr() { printf "%-30s %s\n" "$1" "$2"; }

# ----------------------------------------------------------------------------- #
# Header
echo "📦  Auditing MarketFlock project" > "$LOGFILE"
echo "🔍  Target:" "$TARGET" >> "$LOGFILE"
echo "📅  Datetime:" "$(date)" >> "$LOGFILE"
echo "" >> "$LOGFILE"

# ----------------------------------------------------------------------------- #
# 1. Basic statistics
du -sh "$TARGET" | awk '{print "Total size: "$1}' >> "$LOGFILE"
find "$TARGET" -type f | wc -l | awk '{print "File count: "$1}' >> "$LOGFILE"
find "$TARGET" -type d | wc -l | awk '{print "Dir  count: "$1}' >> "$LOGFILE"
avg_size=$(find "$TARGET" -type f -exec stat -c %s {} + \
           | awk '{sum+=$1} END{if(NR>0){printf "%.2f", sum/NR} else{print 0}}')
echo "Average file size:" "${avg_size} bytes" >> "$LOGFILE"
echo "" >> "$LOGFILE"

# ----------------------------------------------------------------------------- #
# 2. Biggest files (top 10)
echo "🌟  Biggest files:" >> "$LOGFILE"
find "$TARGET" -type f -printf '%s\t%p\n' | sort -nr | head -n10 \
     | awk -F'\t' '{printf "%-50s %10s bytes\n", $2, $1}' >> "$LOGFILE"
echo "" >> "$LOGFILE"

# ----------------------------------------------------------------------------- #
# 3. Permission / ownership anomalies
echo "⚠️  Permission / ownership issues:" >> "$LOGFILE"

# 3.1 World‑writable files
writable=$(find "$TARGET" -type f -perm -o=w -printf '%p\n')
if [[ -z $writable ]]; then
  echo "  • No world‑writable files found." >> "$LOGFILE"
else
  echo "  • World‑writable:" >> "$LOGFILE"
  echo "$writable" >> "$LOGFILE"
fi

# 3.2 Set‑UID / Set‑GID
echo "" >> "$LOGFILE"
echo "  • Set‑UID:" >> "$LOGFILE"
find "$TARGET" -type f -perm -4000 -printf '%p\n' >> "$LOGFILE" || echo "    none" >>
 "$LOGFILE"
echo "  • Set‑GID:" >> "$LOGFILE"
find "$TARGET" -type f -perm -2000 -printf '%p\n' >> "$LOGFILE" || echo "    none" >>
 "$LOGFILE"

# 3.3 Non‑root ownership
echo "" >> "$LOGFILE"
echo "  • Files owned by non‑root users (excluding root):" >> "$LOGFILE"
find "$TARGET" -type f ! -user root -printf '%u:%g  %p\n' \
     | sort | uniq >> "$LOGFILE"
echo "" >> "$LOGFILE"

# ----------------------------------------------------------------------------- #
# 4. File type distribution
echo "📊  File type counts (x) (y)": >> "$LOGFILE"
find "$TARGET" -type f -printf '%y\n' | sort | uniq -c | sort -nr >> "$LOGFILE"
echo "" >> "$LOGFILE"

# ----------------------------------------------------------------------------- #
# 5. SHA‑256 integrity baseline (first 10 files)
echo "📜  SHA‑256 integrity baseline (first 10 files):" >> "$LOGFILE"
find "$TARGET" -type f -print0 | xargs -0 -e sha256sum | head -n 10 >> "$LOGFILE"

# ----------------------------------------------------------------------------- #
# Done
echo "✅  Audit complete. Log written to $LOGFILE"
```
