from ..domain.ai_triage import MockAIProvider, AIProviderInterface

class AIService:
    def __init__(self, provider: AIProviderInterface | None = None):
        self.provider = provider or MockAIProvider()

    def triage(self, incident_id_or_text: str):
        # For CLI we accept incident id or text; keep simple
        return self.provider.triage(incident_id_or_text)
from ..domain.ai_triage import MockAIProvider

class AIService:
    def __init__(self, provider=None):
        self.provider = provider or MockAIProvider()

    def triage(self, incident_id_or_text: str):
        # allow passing raw text or id
        return self.provider.triage(incident_id_or_text)
