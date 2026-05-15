#!/bin/bash
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG_FILE="$PROJECT_DIR/config/cloudflare.json"
ACCOUNT_ID=$(jq -r .account_id "$CONFIG_FILE")
PROJECT_NAME="autoflock"
API_TOKEN=$(jq -r .api_token "$CONFIG_FILE")
SITE_DIR="$(dirname "$PROJECT_DIR")/autoflock/publish"

cd "$SITE_DIR" || exit

echo "🐑 SHEEP 8: Uploading manually via Wrangler..."
CLOUDFLARE_API_TOKEN="$API_TOKEN" CLOUDFLARE_ACCOUNT_ID="$ACCOUNT_ID" npx wrangler pages deploy . --project-name "$PROJECT_NAME" --commit-dirty=true
