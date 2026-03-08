# modules/module2_rag/actuator.py
from config import Config
import json
from datetime import datetime
import requests

#class CRMActuator:
#    def __init__(self, cfg: Config):
#        self.log_path = cfg.DATA_DIR / "crm_actions.json"
#
#    def log_activity(self, activity: dict) -> bool:
#        entry = {"ts": datetime.utcnow().isoformat() + "Z", **activity}
#        self.log_path.parent.mkdir(parents=True, exist_ok=True)
#        with self.log_path.open("a", encoding="utf-8") as f:
#            f.write(json.dumps(entry) + "\n")
#        return True

class CRMActuator:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.log_path = cfg.DATA_DIR / "crm_log.jsonl"

    def log_activity(self, activity: dict) -> bool:
        entry = {"ts": datetime.utcnow().isoformat() + "Z", **activity}

        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

        if self.cfg.CRM_API_ENDPOINT:
            try:
                r = requests.post(
                    self.cfg.CRM_API_ENDPOINT,
                    headers={"Authorization": f"Bearer {self.CRM_API_KEY}"},
                    json=entry,
                    timeout=10
                )
                r.raise_for_status()
            except Exception as e:
                print(f"CRM POST warning: {e}")
        return True
