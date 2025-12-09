
from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.services.guardrails import Guardrails
from app.services.rag_vector import VectorKB
from app.services.llm import LLMService
from app.services.telemetry import Telemetry
from app.services.language import detect_lang

router = APIRouter()

guard = Guardrails()
kb = VectorKB()
llm = LLMService()
telemetry = Telemetry()

@router.post('/chat', response_model=ChatResponse)
def chat(req: ChatRequest):
    user_lang = req.lang if req.lang != 'auto' else detect_lang(req.text)
    redacted = guard.redact_pii(req.text)
    consent = guard.log_consent(user_lang, req.channel)
    docs = kb.search(redacted, top_k=4)
    answer, citations = llm.generate(redacted, user_lang, docs)
    confidence = kb.confidence(docs)
    if confidence < 0.25 and not citations:
        answer = ("I'm not confident. Please specify the department/service or share more details.")
    telemetry.log_event('chat', {'lang': user_lang, 'channel': req.channel, 'citations': citations, 'confidence': confidence})
    return ChatResponse(answer=answer, citations=citations, redacted_query=redacted, consent_id=consent['id'], confidence=confidence)
