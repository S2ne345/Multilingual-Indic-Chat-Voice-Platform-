
import re, uuid
from datetime import datetime
class Guardrails:
    def redact_pii(self, text: str) -> str:
        text = re.sub(r"[\w\.-]+@[\w\.-]+", "[email_redacted]", text)
        text = re.sub(r"\+?\d[\d\- ]{7,}", "[phone_redacted]", text)
        return text
    def log_consent(self, lang: str, channel: str):
        return {'id': str(uuid.uuid4()), 'lang': lang, 'channel': channel, 'timestamp': datetime.utcnow().isoformat()}
