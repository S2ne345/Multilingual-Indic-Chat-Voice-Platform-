
from app.utils.config import ASR_PROVIDER
class ASRService:
    def __init__(self):
        self.provider = ASR_PROVIDER
    def transcribe(self, audio_bytes: bytes) -> str:
        if self.provider == 'mock':
            return 'ASR mock: transcription not implemented.'
        return '[ASR provider stub: integrate real ASR]'
