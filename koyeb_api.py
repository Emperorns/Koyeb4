import requests
from typing import List, Dict, Optional

KOYEB_API = "https://app.koyeb.com/v1"

class KoyebAPI:
    def __init__(self, api_key: str):
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    def get_apps(self) -> List[Dict]:
        try:
            response = requests.get(f"{KOYEB_API}/apps", headers=self.headers)
            response.raise_for_status()
            return response.json().get("apps", [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching apps: {e}")
            return []

    def app_action(self, app_id: str, action: str) -> bool:
        try:
            response = requests.post(
                f"{KOYEB_API}/apps/{app_id}/{action}",
                headers=self.headers
            )
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Error performing {action} on {app_id}: {e}")
            return False
    
    def get_logs(self, app_id: str) -> Optional[str]:
        try:
            response = requests.get(
                f"{KOYEB_API}/apps/{app_id}/logs",
                headers=self.headers
            )
            response.raise_for_status()
            return response.text[:4000]  # Truncate for Telegram limits
        except requests.exceptions.RequestException as e:
            print(f"Error fetching logs for {app_id}: {e}")
            return None
