from typing import Dict, Any, Tuple


def compute_risk(severity: str, error_freq: int, latency_spike: bool, failed_deployments: int, repeated_clients: int, age_hours: float, affected_services: int) -> Tuple[float, Dict[str,Any]]:
    # deterministic scoring: base by severity
    sev_map = {'low':0.1,'medium':0.4,'high':0.7,'critical':0.9}
    base = sev_map.get(severity.lower(), 0.2)
    score = base
    reasons = {'base_severity': base}
    score += min(0.2, error_freq * 0.02)
    reasons['error_freq'] = error_freq * 0.02
    if latency_spike:
        score += 0.1
        reasons['latency_spike'] = 0.1
    score += min(0.15, failed_deployments * 0.05)
    reasons['failed_deployments'] = failed_deployments * 0.05
    score += min(0.1, repeated_clients * 0.02)
    reasons['repeated_clients'] = repeated_clients * 0.02
    score += min(0.1, age_hours * 0.005)
    reasons['age_hours'] = age_hours * 0.005
    score += min(0.15, affected_services * 0.03)
    reasons['affected_services'] = affected_services * 0.03
    score = min(1.0, round(score, 3))
    return score, reasons
