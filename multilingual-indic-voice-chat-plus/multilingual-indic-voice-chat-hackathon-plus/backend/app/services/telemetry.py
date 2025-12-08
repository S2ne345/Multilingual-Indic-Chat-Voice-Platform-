
import os, json
from datetime import datetime
class Telemetry:
    def __init__(self):
        self.log_path = os.path.join(os.path.dirname(__file__), '../../..', 'logs')
        os.makedirs(self.log_path, exist_ok=True)
        self.log_file = os.path.join(self.log_path, 'telemetry.log')
    def log_event(self, event_type: str, payload: dict):
        record = {'ts': datetime.utcnow().isoformat(), 'type': event_type, 'payload': payload}
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record) + '
')
