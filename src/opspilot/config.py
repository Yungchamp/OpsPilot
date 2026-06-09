import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

class Settings:
    DB_PATH: str = os.environ.get('OPSPILOT_DB', str(ROOT / 'data' / 'opspilot.db'))
    HMAC_SECRET: str = os.environ.get('OPSPILOT_HMAC_SECRET', 'dev-secret')
    TOKEN_TTL_SECONDS: int = int(os.environ.get('OPSPILOT_TOKEN_TTL', '3600'))
    ESCALATION_HIGH_RISK_DELAY_MINUTES: int = int(os.environ.get('OPSPILOT_ESCALATION_DELAY_MINUTES', '30'))
    ESCALATION_HIGH_RISK_SCORE: float = float(os.environ.get('OPSPILOT_ESCALATION_HIGH_RISK_SCORE', '0.7'))
    ESCALATION_REPEATED_FAILURES: int = int(os.environ.get('OPSPILOT_ESCALATION_REPEATED_FAILURES', '3'))

settings = Settings()
