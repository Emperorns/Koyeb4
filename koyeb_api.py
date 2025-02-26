import requests
import json
from typing import Dict, List

KOYEB_API = "https://app.koyeb.com/v1"

class KoyebAPI:
    def __init__(self, api_key: str):
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    def get_apps(self) -> List[Dict]:
        try:
            res = requests.get(f"{KOYEB_API}/apps", headers=self.headers)
            return res.json().get("apps", [])
        except Exception as e:
            return []

    def app_action(self, app_id: str, action: str) -> bool:
        try:
            res = requests.post(
                f"{KOYEB_API}/apps/{app_id}/{action}",
                headers=self.headers
            )
            return res.status_code == 200
        except:
            return False
    
    def get_logs(self, app_id: str) -> str:
        try:
            res = requests.get(
                f"{KOYEB_API}/apps/{app_id}/logs",
                headers=self.headers
            )
            return res.text[:4000]  # Truncate for Telegram limits
        except:
            return "Failed to fetch logs"
