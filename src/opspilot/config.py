import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

class Settings:
    DB_PATH: str = os.environ.get('OPSPILOT_DB', str(ROOT / 'data' / 'opspilot.db'))
    HMAC_SECRET: str = os.environ.get('OPSPILOT_HMAC_SECRET', 'dev-secret')
    TOKEN_TTL_SECONDS: int = int(os.environ.get('OPSPILOT_TOKEN_TTL', '3600'))

settings = Settings()
