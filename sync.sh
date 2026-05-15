#!/bin/bash

# AUTOFLOCK MASTER SYNC SCRIPT
# This script runs the full AI automation pipeline and pushes updates to the web.

PROJECT_DIR="/data/data/com.termux/files/home/projects/media/autoflock"
cd $PROJECT_DIR

echo "------------------------------------------"
echo "🤖 Starting Autoflock Sync: $(date)"
echo "------------------------------------------"

# 1. Run the Orchestrator (Scout -> Writer -> Social Poster)
echo "🐑 Step 1: Running AI Pipeline & Social Posting..."
python3 run_flock.py

# 2. Pull, Add, Commit, and Push to GitHub (Triggers Cloudflare Web Update)
echo "🚀 Step 2: Syncing to Web (GitHub/Cloudflare)..."
git pull origin main --rebase
git add .
git commit -m "Autoflock Update: $(date +'%Y-%m-%d %H:%M')" || echo "No changes to commit"
git push origin main

echo "------------------------------------------"
echo "✅ SYNC COMPLETE: Your AI tools are live!"
echo "🌐 URL: https://autoflock.cutbar.in"
echo "------------------------------------------"
