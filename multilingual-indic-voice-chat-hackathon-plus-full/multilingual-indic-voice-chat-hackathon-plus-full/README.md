
# Multilingual Indic Chat + Voice Platform

A conversational AI system that supports **Tamil, Hindi, Telugu, and English** (including **code-mixed queries**) via **text and voice**. Built with **FastAPI**, it uses **Retrieval-Augmented Generation (RAG)** for grounded answers with **citations**, and includes **pluggable adapters** for ASR/TTS/LLM (mock by default, ready to integrate providers such as Azure Speech and OpenAI).

---

## ✨ Features

- **Multilingual chat**: Tamil (`ta`), Hindi (`hi`), Telugu (`te`), English (`en`), plus code-mix handling.
- **RAG**: TF‑IDF + cosine similarity to retrieve relevant KB lines with **citations** and a **confidence score**.
- **Pluggable adapters**:
  - **ASR**: mock placeholders; ready for Azure Speech/Whisper/Vakyansh.
  - **TTS**: mock WAV beep; ready for Azure TTS/Coqui.
  - **LLM**: mock synthesizer; ready for OpenAI/Mistral/Llama.
- **Guardrails**: PII redaction (email/phone), consent logging (UUID), optional API key middleware.
- **Simple web UI**: text input, mic capture (MediaRecorder), TTS playback, citation display, copy-to-clipboard.
- **Dev tooling**: unit tests (pytest), Docker Compose, Kubernetes manifests, and CI-ready workflow.

---

## 📁 Project Structure

```text
.
├─ README.md
├─ .env.example
├─ docs/
│  ├─ tools.md                 # Tools, licenses, versions
│  ├─ architecture.png         # Architecture diagram (optional)
│  └─ architecture.md          # Mermaid diagram (optional)
├─ data/
│  └─ kb/
│     └─ gov_faqs.md           # Sample multilingual KB
├─ backend/
│  ├─ requirements.txt
│  ├─ Dockerfile
│  └─ app/
│     ├─ main.py               # FastAPI app
│     ├─ utils/config.py       # Env config
│     ├─ middleware/api_key.py # Optional API key protection
│     ├─ models/schemas.py     # Pydantic models
│     ├─ routers/
│     │  ├─ chat.py            # /api/v1/chat
│     │  ├─ asr_tts.py         # /api/v1/asr, /api/v1/tts
│     │  ├─ kb.py              # /api/v1/kb (list/add)
│     │  └─ health.py          # /health
│     ├─ services/
│     │  ├─ rag_vector.py      # TF‑IDF + cosine RAG
│     │  ├─ llm.py             # LLM adapter (mock + stub)
│     │  ├─ asr.py             # ASR adapter (mock + stub)
│     │  ├─ tts.py             # TTS adapter (mock + stub)
│     │  ├─ language.py        # Heuristic language detection
│     │  ├─ guardrails.py      # PII redaction + consent
│     │  └─ telemetry.py       # JSONL audit logging
│     └─ providers/            # Provider stubs (Azure/OpenAI)
│        ├─ asr_azure.py
│        ├─ tts_azure.py
│        └─ llm_openai.py
├─ frontend/
│  └─ web/
│     ├─ index.html
│     ├─ app.js
│     └─ styles.css
├─ deploy/
│  ├─ docker-compose.yml
│  └─ k8s/
│     ├─ deployment.yaml
│     └─ service.yaml
├─ outputs/
│  ├─ positive_tests_output.json
│  └─ negative_tests_output.json
└─ backend/tests/
   ├─ test_positive_TC1.py
   └─ test_negative_TC2.py
```

---

## 🚀 Quick Start

### Prerequisites
- Python **3.11+**
- `pip`

### Backend (FastAPI)
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

- OpenAPI docs: **http://localhost:8000/docs**

### Frontend (Static)
- Open `frontend/web/index.html` in your browser.

---

## ⚙️ Configuration

1. Copy `.env.example` → `.env`
2. Set providers and security:

```ini
APP_ENV=dev
APP_PORT=8000
LOG_LEVEL=info

ASR_PROVIDER=mock        # mock|azure|whisper|vakyansh
TTS_PROVIDER=mock        # mock|azure|coqui
LLM_PROVIDER=mock        # mock|openai|mistral|llama

API_KEY=change-me        # optional; send as x-api-key header

KB_PATH=./data/kb
```

---

## 🔌 Swapping Providers (Adapters)

- **ASR** (`backend/app/services/asr.py`)
  - Implement `AzureASR` in `providers/asr_azure.py` and set `ASR_PROVIDER=azure`.
- **TTS** (`backend/app/services/tts.py`)
  - Implement `AzureTTS` or `Coqui` adapter and set `TTS_PROVIDER=azure|coqui`.
- **LLM** (`backend/app/services/llm.py`)
  - Implement `OpenAIProvider` or similar in `providers/llm_openai.py` and set `LLM_PROVIDER=openai|mistral|llama`.

> Keep credentials in `.env` and load via `utils/config.py`.

---

## 🧠 RAG (Retrieval-Augmented Generation)

- **VectorKB** (TF‑IDF + cosine similarity)
- Returns **citations** (`gov_faqs.md#L<line>`) and a **confidence score**.
- If confidence is low or citations are empty, the system **abstains** and asks for clarification.

---

## 🔐 Security & Privacy

- **PII redaction**: masks emails and phone numbers in user queries.
- **Consent logging**: `consent_id` (UUID) with timestamp per interaction.
- **Optional API key**: protect `/api/*` routes using `x-api-key` when enabled.
- **Telemetry**: JSONL logs capture `{citations, confidence, lang, channel}`.

---

## 🧪 Testing

Run all tests:
```bash
cd backend
pytest -q
```

Run specific files:
```bash
pytest backend/tests/test_positive_TC1.py -q
pytest backend/tests/test_negative_TC2.py -q
```

---

## 🧰 API Endpoints

**Chat (Text)**
```http
POST /api/v1/chat
Body: { "text": "...", "lang": "auto|en|ta|hi|te", "channel": "text" }
Response: { "answer", "citations": [], "redacted_query", "consent_id", "confidence" }
```

**ASR (Voice Upload, mock by default)**
```http
POST /api/v1/asr
FormData: file=<audio.webm|wav>
Response: { "text": "ASR mock: transcription not implemented.", "lang": "auto" }
```

**TTS (Mock WAV beep)**
```http
POST /api/v1/tts
Body: { "text": "...", "lang": "en|ta|hi|te" }
Response: { "audio_base64": "<wav-base64>", "format": "wav" }
```

**Knowledge Base (Admin)**
```http
GET  /api/v1/kb     -> { "count", "samples": [...] }
POST /api/v1/kb     -> { "status": "ok" }  # body: { "text": "...", "source": "api" }
```

**Health Check**
```http
GET /health -> { "status": "ok" }
```

---

## 🐳 Docker

```bash
cd deploy
docker compose up --build
```

Backend: `http://localhost:8000`

---

## ☸️ Kubernetes (Optional)

- Edit images and replica counts in `deploy/k8s/deployment.yaml`
- Apply manifests:
```bash
kubectl apply -f deploy/k8s/deployment.yaml
kubectl apply -f deploy/k8s/service.yaml
```

---

## 🛠 Tech Stack

- **Backend:** FastAPI, Uvicorn, Pydantic
- **RAG:** Custom TF‑IDF + cosine similarity
- **Language Detection:** Heuristic based on Unicode ranges
- **Frontend:** HTML/CSS/JavaScript (MediaRecorder for mic capture)
- **Infra/CI:** Docker, Kubernetes manifests, Pytest, GitHub Actions (optional)

See `docs/tools.md` for **licenses, URLs, and versions**.

---

## 📄 License

**MIT License** — see `LICENSE`.

---

## 🤝 Contributing

1. Fork the repo & create a feature branch
2. Ensure tests pass: `pytest -q`
3. Submit a PR with a clear description, screenshots (optional), and any configuration notes

---

## 📣 Notes

- The repo includes **mock ASR/TTS/LLM** to keep it runnable without GPU/cloud keys.
- To improve answer quality and enable real voice synthesis/transcription, **wire the provider adapters** and add credentials in `.env`.
- For production, consider **hybrid search** (BM25 + dense embeddings), **structured prompts**, and **eval harnesses** (faithfulness & grounding).
