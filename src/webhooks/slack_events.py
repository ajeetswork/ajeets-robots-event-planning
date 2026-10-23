import os

from flask import Blueprint, Response, jsonify, request

from .verification import verify_slack_signature

slack_webhooks = Blueprint("slack_webhooks", __name__)


def dispatch_workspace_event(event: dict) -> None:
    print(f"slack-event:{event.get('type')}")


@slack_webhooks.post("/webhooks/slack/events")
def slack_events_webhook():
    raw_body = request.get_data()
    timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
    signature = request.headers.get("X-Slack-Signature", "")
    secret = os.environ.get("SLACK_SIGNING_SECRET", "")
    if not verify_slack_signature(raw_body, timestamp, signature, secret):
        return Response(status=401)

    payload = request.get_json(force=True)

    if payload.get("type") == "url_verification":
        return jsonify({"challenge": payload.get("challenge")})

    event = payload.get("event")
    if event:
        dispatch_workspace_event(event)

    return jsonify({"ok": True})
