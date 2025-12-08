
from app.services.rag_vector import VectorKB
from app.services.llm import LLMService
from app.services.language import detect_lang

kb = VectorKB()
llm = LLMService()

# Positive cases
def test_positive_english_ration():
    docs = kb.search('How to apply for a ration card?', top_k=4)
    ans, cites = llm.generate('How to apply for a ration card?', 'en', docs)
    assert cites and len(cites) >= 1
    assert 'Visit the state civil supplies department portal' in ans
    assert kb.confidence(docs) > 0.25

def test_positive_tamil_banking():
    q = 'Balance check pannunga please'
    lang = detect_lang(q)
    docs = kb.search(q, top_k=4)
    ans, cites = llm.generate(q, lang, docs)
    assert cites and len(cites) >= 1

def test_positive_hindi_aadhaar():
    q = 'आधार अपडेट के लिए क्या चाहिए?'
    docs = kb.search(q, top_k=4)
    ans, cites = llm.generate(q, 'hi', docs)
    assert cites and len(cites) >= 1

# Negative cases
def test_negative_out_of_scope():
    q = 'How to renew a U.S. driver's license in California?'
    docs = kb.search(q, top_k=4)
    ans, cites = llm.generate(q, 'en', docs)
    conf = kb.confidence(docs)
    assert conf <= 0.25 or len(cites) == 0

def test_negative_empty_query():
    q = ''
    docs = kb.search(q, top_k=4)
    ans, cites = llm.generate(q, 'en', docs)
    assert len(cites) == 0
