from typing import Dict, Any


class MockAIProvider:
    def triage(self, incident_text: str) -> Dict[str, Any]:
        # deterministic mock: simple keyword heuristics
        text = incident_text.lower()
        causes = []
        if 'timeout' in text or 'latency' in text:
            causes.append('performance')
        if 'exception' in text or 'trace' in text or '500' in text:
            causes.append('backend-error')
        if 'deploy' in text or 'release' in text:
            causes.append('deployment')
        if not causes:
            causes.append('unknown')
        summary = incident_text[:200]
        confidence = 0.9 if 'error' in text or 'failed' in text else 0.6
        missing = []
        if 'steps to reproduce' not in text and 'repro' not in text:
            missing.append('reproduction_steps')
        return {
            'summary': summary,
            'likely_causes': causes,
            'recommendations': ['check logs','restore from backup'] if 'backend-error' in causes else ['investigate latency','scale instances'],
            'confidence': confidence,
            'missing_context': missing
        }


class AIProviderInterface:
    def triage(self, incident_text: str) -> Dict[str, Any]:
        raise NotImplementedError()
