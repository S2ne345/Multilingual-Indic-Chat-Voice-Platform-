
from app.services.rag_vector import VectorKB
from app.services.llm import LLMService
from app.services.language import detect_lang

def test_TC2_negative_out_of_scope_us_drivers_license():
    """
    TC#2 — Out-of-Scope US Driver’s License
    Description:
      User types: "How to renew a U.S. driver's license in California?" via /api/v1/chat.

    Expected Results:
      - RAG finds no relevant Indian KB lines → citations may be empty.
      - Confidence < 0.25.
      - Answer includes abstain-style message.
    """
    kb = VectorKB()
    llm = LLMService()
    query = "How to renew a U.S. driver's license in California?"
    lang = detect_lang(query)
    docs = kb.search(query, top_k=4)
    answer, citations = llm.generate(query, lang, docs)
    conf = kb.confidence(docs)
    assert conf < 0.25 or not citations
    assert ("I'm not confident" in answer) or ("I couldn't find reliable information" in answer)
