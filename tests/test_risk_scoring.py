from opspilot.domain.risk import compute_risk


def test_risk_scoring():
    score, reasons = compute_risk('high', 5, True, 1, 2, 48, 2)
    assert 0 <= score <= 1
    assert 'base_severity' in reasons
