from datetime import datetime

class NotificationService:
    def prepare_escalation_payload(self, escalation: dict) -> dict:
        target = escalation.get('notification_targets', [])
        if not target:
            target = [f"{escalation.get('assigned_team','operations')}@ops.example.com"]
        subject = f"Escalation {escalation.get('escalation_id')} for incident {escalation.get('incident_id')}"
        body = (
            f"Incident {escalation.get('incident_id')} requires attention. "
            f"Severity: {escalation.get('severity')}. Reason: {escalation.get('reason')}. "
            f"Assigned to: {escalation.get('assigned_team')}."
        )
        priority = 'high' if escalation.get('severity') == 'critical' else 'normal'
        created_at = datetime.utcnow().isoformat() + 'Z'
        return {
            'target': target[0],
            'channel': 'email',
            'subject': subject,
            'body': body,
            'incident_id': escalation.get('incident_id'),
            'escalation_id': escalation.get('escalation_id'),
            'priority': priority,
            'created_at': created_at,
        }
