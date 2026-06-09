# Escalation Workflow

## When escalations are created

OpsPilot creates an escalation record when one of these rules is met:

- Critical incidents escalate immediately.
- High-risk unresolved incidents escalate after a configurable delay threshold.
- Repeated failed deployments for the same service trigger escalation.
- Resolved or closed incidents do not generate new escalations.
- Duplicate active escalations for the same incident are prevented.

Escalation creation is exposed through the API and CLI, and when an escalation is created the system enqueues a notification job.

## Escalation record fields

Each escalation includes:

- `escalation_id`
- `incident_id`
- `severity`
- `assigned_team`
- `reason`
- `status`
- `created_at`
- `acknowledged_at`
- `resolved_at`
- `notification_targets`

## Status transitions

Escalations flow through these statuses:

- `pending`: created and awaiting notification execution.
- `notified`: notification job has been queued and marked by workflow execution.
- `acknowledged`: the on-call team has acknowledged the escalation.
- `resolved`: the escalation has been closed.
- `cancelled`: the escalation was cancelled.

The API supports acknowledge and resolve actions.

## Notification preparation

Notification payloads are prepared deterministically by `NotificationService` and include:

- `target`
- `channel`
- `subject`
- `body`
- `incident_id`
- `escalation_id`
- `priority`
- `created_at`

The system does not send real emails or external requests. It prepares payloads and enqueues jobs for notification handling.

## Job queue integration

When an escalation is created, a `escalation_notification` job is enqueued in the job queue with:

- `job_id`
- `job_type`
- `payload`
- `status`
- `attempts`
- `next_run_at`
- `last_error`
- `idempotency_key`

The workflow runner processes escalation notification jobs and updates escalation status from `pending` to `notified`.

## CLI usage

- `python -m opspilot.cli escalations --db path`
- `python -m opspilot.cli escalate --db path --incident INC-001`
- `python -m opspilot.cli pending-notifications --db path`

## API endpoints

- `GET /escalations`
- `POST /incidents/{incident_id}/escalate`
- `POST /escalations/{escalation_id}/acknowledge`
- `POST /escalations/{escalation_id}/resolve`
