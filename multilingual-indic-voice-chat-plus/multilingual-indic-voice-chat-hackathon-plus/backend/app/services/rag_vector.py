
import os, math, re
from collections import defaultdict, Counter
KB_DIR = os.environ.get('KB_PATH', os.path.join(os.path.dirname(__file__), '../../..', 'data', 'kb'))
KB_FILE = os.path.join(KB_DIR, 'gov_faqs.md')
class VectorKB:
    def __init__(self):
        self.docs = []
        self.vocab = {}
        self.idf = {}
        self.doc_vectors = []
        self._load()
    def _tokenize(self, text):
        return re.findall(r"[a-zA-Z஀-௿ऀ-ॿఀ-౿]+", text.lower())
    def _load(self):
        if not os.path.exists(KB_FILE):
            return
        with open(KB_FILE, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                line = line.strip()
                if line:
                    self.docs.append((line, f'gov_faqs.md#L{i+1}'))
        self._build_index()
    def _build_index(self):
        df = defaultdict(int)
        tokenized_docs = []
        for text, _ in self.docs:
            toks = set(self._tokenize(text))
            tokenized_docs.append(toks)
            for t in toks:
                df[t] += 1
        N = len(self.docs)
        self.idf = {t: math.log((N + 1) / (df_t + 1)) + 1 for t, df_t in df.items()}
        self.vocab = {t: i for i, t in enumerate(self.idf.keys())}
        self.doc_vectors = []
        for text, _ in self.docs:
            toks = self._tokenize(text)
            tf = Counter(toks)
            vec = {}
            for t, c in tf.items():
                if t in self.vocab:
                    vec[self.vocab[t]] = (c / max(1, len(toks))) * self.idf[t]
            self.doc_vectors.append(vec)
    def _vectorize_query(self, query):
        toks = self._tokenize(query)
        tf = Counter(toks)
        vec = {}
        for t, c in tf.items():
            if t in self.vocab:
                vec[self.vocab[t]] = (c / max(1, len(toks))) * self.idf[t]
        return vec
    def _cosine(self, v1, v2):
        if not v1 or not v2:
            return 0.0
        dot = sum(v1.get(i, 0.0) * v2.get(i, 0.0) for i in set(v1.keys()) | set(v2.keys()))
        n1 = math.sqrt(sum(x*x for x in v1.values()))
        n2 = math.sqrt(sum(x*x for x in v2.values()))
        if n1 == 0 or n2 == 0:
            return 0.0
        return dot / (n1 * n2)
    def search(self, query: str, top_k: int = 3):
        qv = self._vectorize_query(query)
        ranked = []
        for i, (text, src) in enumerate(self.docs):
            sim = self._cosine(qv, self.doc_vectors[i])
            ranked.append((i, sim))
        ranked.sort(key=lambda x: x[1], reverse=True)
        return [{'doc_id': i, 'text': self.docs[i][0], 'score': s, 'source': self.docs[i][1]} for i, s in ranked[:top_k] if s > 0]
    def confidence(self, docs):
        if not docs:
            return 0.0
        avg = sum(d['score'] for d in docs) / len(docs)
        return max(0.0, min(1.0, avg))
    def add(self, text: str, source: str):
        self.docs.append((text, source))
        self._build_index()
