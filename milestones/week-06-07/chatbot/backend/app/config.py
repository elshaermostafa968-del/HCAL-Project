from pathlib import Path
from functools import lru_cache
from typing import Literal
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / '.env', override=False)

@lru_cache
def settings():
    provider = os.getenv('LLM_PROVIDER', 'local').lower()
    if provider not in {'local', 'gemini', 'openai'}:
        raise ValueError('LLM_PROVIDER must be local, gemini, or openai')
    return {
        'provider': provider,
        'gemini_key': os.getenv('GEMINI_API_KEY', ''),
        'openai_key': os.getenv('OPENAI_API_KEY', ''),
        'gemini_model': os.getenv('GEMINI_MODEL', 'gemini-2.5-flash'),
        'openai_model': os.getenv('OPENAI_MODEL', 'gpt-4.1-mini'),
        'feedback_path': Path(os.getenv('FEEDBACK_PATH', str(ROOT / 'data' / 'feedback.jsonl'))),
    }
