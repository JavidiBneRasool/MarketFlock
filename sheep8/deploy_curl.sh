#!/bin/bash
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG_FILE="$PROJECT_DIR/config/cloudflare.json"
ACCOUNT_ID=$(jq -r .account_id "$CONFIG_FILE")
TOKEN=$(jq -r .api_token "$CONFIG_FILE")
PROJECT_NAME="marketflock"
ZIP_PATH="$PROJECT_DIR/output/marketflock-deploy.zip"
MANIFEST_PATH="$PROJECT_DIR/output/manifest.json"

# Build manifest.json correctly
python3 -c '
import json, hashlib, zipfile, sys
zip_path = sys.argv[1]
manifest = {}
with zipfile.ZipFile(zip_path, "r") as zf:
    for name in zf.namelist():
        content = zf.read(name)
        manifest["/" + name] = hashlib.sha256(content).hexdigest()
with open("manifest.json", "w") as f:
    json.dump(manifest, f)
' "$ZIP_PATH"

echo "Deploying to Cloudflare..."
curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/$PROJECT_NAME/deployments" \
     -H "Authorization: Bearer $TOKEN" \
     -F "manifest=$(cat manifest.json)" \
     -F "branch=main" \
     -F "file=@$ZIP_PATH" | jq .
