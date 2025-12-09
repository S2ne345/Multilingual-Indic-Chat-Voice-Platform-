
import os
from dotenv import load_dotenv
load_dotenv()
APP_ENV = os.getenv('APP_ENV', 'dev')
APP_PORT = int(os.getenv('APP_PORT', '8000'))
LOG_LEVEL = os.getenv('LOG_LEVEL', 'info')
API_KEY = os.getenv('API_KEY', '')
KB_PATH = os.getenv('KB_PATH', './data/kb')
ASR_PROVIDER = os.getenv('ASR_PROVIDER', 'mock')
TTS_PROVIDER = os.getenv('TTS_PROVIDER', 'mock')
LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'mock')
