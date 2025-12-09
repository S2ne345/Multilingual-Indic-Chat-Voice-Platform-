
from typing import List, Tuple
from app.utils.config import LLM_PROVIDER
class LLMService:
    def __init__(self):
        self.provider = LLM_PROVIDER
    def generate(self, query: str, lang: str, results: List[dict]) -> Tuple[str, List[str]]:
        if self.provider == 'mock':
            if not results:
                return ("I couldn't find reliable information. Please specify more details or service name.", [])
            bullets = '
'.join([f"- {r['text']}" for r in results])
            cites = [r['source'] for r in results]
            answer = f"({lang}) Relevant info found:
{bullets}

I can guide step-by-step or share official links."
            return answer, cites
        return ("[LLM provider stub: integrate model API]", [r['source'] for r in results])
