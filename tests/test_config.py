from opspilot.config import settings

def test_settings_load():
    assert settings.DB_PATH is not None
    assert 'opspilot' in settings.DB_PATH
