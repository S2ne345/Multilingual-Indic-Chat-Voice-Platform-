
from fastapi import APIRouter, UploadFile, File
from app.services.asr import ASRService
from app.services.tts import TTSService
from app.services.telemetry import Telemetry
router = APIRouter()
telemetry = Telemetry()
@router.post('/asr')
async def asr_endpoint(file: UploadFile = File(...)):
    asr = ASRService()
    audio_bytes = await file.read()
    text = asr.transcribe(audio_bytes)
    telemetry.log_event('asr', {"filename": file.filename, "length": len(audio_bytes)})
    return {"text": text, "lang": "auto"}
@router.post('/tts')
async def tts_endpoint(payload: dict):
    tts = TTSService()
    text = payload.get('text', '')
    lang = payload.get('lang', 'en')
    audio_b64 = tts.synthesize(text, lang)
    telemetry.log_event('tts', {"lang": lang, "text_len": len(text)})
    return {"audio_base64": audio_b64, "format": "wav"}
