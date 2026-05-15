# Cleanup - Delete old Cloudflare deployments
import json, os, requests

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"

def run():
    print("🐑 Cleanup: Deleting old deployments...")
    try:
        with open(f"{PROJECT}/config/cloudflare.json") as f:
            cf = json.load(f)
        account_id = cf["account_id"]
        token = cf["api_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        pages_project = os.environ.get("AUTOFLOCK_CLOUDFLARE_PROJECT", "autoflock")
        url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects/{pages_project}/deployments"
        r = requests.get(url, headers=headers)
        deployments = r.json().get("result", [])
        
        # Delete all except the first one (keep a backup)
        for dep in deployments[1:]:
            dep_id = dep["id"]
            del_url = f"{url}/{dep_id}"
            requests.delete(del_url, headers=headers)
        
        print(f"   Cleaned {max(0, len(deployments)-1)} old deployments ✓")
    except Exception as e:
        print(f"   Cleanup skipped: {e}")

if __name__ == "__main__":
    run()
