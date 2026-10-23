import os

from flask import Blueprint, Response, request

from .verification import verify_statushub_token

statushub_webhooks = Blueprint("statushub_webhooks", __name__)


def update_incident_state(alert: dict) -> None:
    print(f"incident:{alert.get('incident_id')}:{alert.get('state')}")


@statushub_webhooks.post("/webhooks/statushub")
def statushub_alert_webhook():
    token = request.headers.get("X-StatusHub-Token", "")
    if not verify_statushub_token(token, os.environ["STATUSHUB_INGRESS_TOKEN"]):
        return Response(status=401)

    alert = request.get_json(force=True)
    update_incident_state(alert)
    return Response(status=204)
