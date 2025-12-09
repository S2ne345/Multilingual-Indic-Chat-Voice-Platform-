
from app.services.rag_vector import VectorKB
from app.services.llm import LLMService
from app.services.language import detect_lang

def test_TC1_positive_english_ration_card():
    """
    TC#1 — English Ration Card Query
    Description:
      User types an English query: "How to apply for a ration card?" via /api/v1/chat
      with lang="auto" and channel="text".

    Expected Results:
      - System detects language = 'en'.
      - RAG retrieves ≥1 KB line.
      - Answer includes ≥1 citation (e.g., gov_faqs.md#L1).
      - Confidence ≥ 0.25.
    """
    kb = VectorKB()
    llm = LLMService()
    query = "How to apply for a ration card?"
    lang = detect_lang(query)
    assert lang == "en"
    docs = kb.search(query, top_k=4)
    assert len(docs) >= 1
    answer, citations = llm.generate(query, lang, docs)
    assert citations
    assert any(c.startswith("gov_faqs.md#L") for c in citations)
    assert "Visit the state civil supplies department portal" in answer
    conf = kb.confidence(docs)
    assert conf >= 0.25
