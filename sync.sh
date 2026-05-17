#!/bin/bash

# AUTOFLOCK MASTER SYNC SCRIPT
# This script runs the full AI automation pipeline and pushes updates to the web.

set -euo pipefail

PROJECT_DIR="/data/data/com.termux/files/home/projects/media/autoflock"
cd "$PROJECT_DIR"

fail() {
  echo "------------------------------------------"
  echo "❌ SYNC FAILED: $1"
  echo "------------------------------------------"
  exit 1
}

echo "------------------------------------------"
echo "🤖 Starting Autoflock Sync: $(date)"
echo "------------------------------------------"

# 0. Start from the latest remote state so generated files are based on current main.
echo "🔄 Step 0: Updating local branch from GitHub..."
git fetch origin main || fail "Could not fetch origin/main"
git rebase origin/main || fail "Could not rebase local commits onto origin/main. Resolve conflicts, then run: git rebase --continue"

# 1. Run the Orchestrator (Scout -> Writer -> Social Poster)
echo "🐑 Step 1: Running AI Pipeline & Social Posting..."
python3 run_flock.py || fail "AI pipeline failed"

# 2. Add, Commit, and Push to GitHub (Triggers Cloudflare Web Update)
echo "🚀 Step 2: Syncing to Web (GitHub/Cloudflare)..."
git add .
if git diff --cached --quiet; then
  echo "No changes to commit"
else
  git commit -m "Autoflock Update: $(date +'%Y-%m-%d %H:%M')" || fail "Commit failed"
fi

if ! git push origin main; then
  echo "Remote changed during sync. Rebasing once and retrying push..."
  git fetch origin main || fail "Could not fetch origin/main after push rejection"
  git rebase origin/main || fail "Could not rebase after push rejection. Resolve conflicts, then run: git rebase --continue && git push origin main"
  git push origin main || fail "Push failed after rebase retry"
fi

echo "------------------------------------------"
echo "✅ SYNC COMPLETE: Your AI tools are live!"
echo "🌐 URL: https://autoflock.cutbar.in"
echo "------------------------------------------"

# Keep only latest 150 article files
cd ~/projects/media/marketflock/publish
ls -t *.html | grep -v index.html | tail -n +151 | xargs rm -f 2>/dev/null
cd ~/projects/media/marketflock
