from flask import Blueprint, jsonify, request

slack_webhooks = Blueprint("slack_webhooks", __name__)


def dispatch_workspace_event(event: dict) -> None:
    print(f"slack-event:{event.get('type')}")


@slack_webhooks.post("/webhooks/slack/events")
def slack_events_webhook():
    payload = request.get_json(force=True)

    if payload.get("type") == "url_verification":
        return jsonify({"challenge": payload.get("challenge")})

    event = payload.get("event")
    if event:
        dispatch_workspace_event(event)

    return jsonify({"ok": True})
