
import base64
from app.utils.config import TTS_PROVIDER

def _sine_wave(duration_s=0.5, freq=440.0, sr=16000):
    import numpy as np
    t = np.linspace(0, duration_s, int(sr*duration_s), False)
    tone = 0.5*np.sin(2*np.pi*freq*t)
    audio = (tone * 32767).astype(np.int16)
    return audio.tobytes(), sr

class TTSService:
    def __init__(self):
        self.provider = TTS_PROVIDER
    def synthesize(self, text: str, lang: str = 'en') -> str:
        if self.provider == 'mock':
            audio_bytes, sr = _sine_wave()
            import io, struct
            buf = io.BytesIO()
            buf.write(b'RIFF')
            buf.write(struct.pack('<I', 36 + len(audio_bytes)))
            buf.write(b'WAVEfmt ')
            buf.write(struct.pack('<I', 16))
            buf.write(struct.pack('<HHIIHH', 1, 1, sr, sr*2, 2, 16))
            buf.write(b'data')
            buf.write(struct.pack('<I', len(audio_bytes)))
            buf.write(audio_bytes)
            return base64.b64encode(buf.getvalue()).decode('ascii')
        return base64.b64encode(b'').decode('ascii')
