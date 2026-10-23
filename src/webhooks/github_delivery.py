import json
import os

from flask import Blueprint, Response, request

from .verification import verify_github_signature

github_webhooks = Blueprint("github_webhooks", __name__)


def enqueue_repository_sync(repository: str, delivery_id: str) -> None:
    print(f"repo-sync:{repository}:{delivery_id}")


@github_webhooks.post("/webhooks/github")
def github_delivery_webhook():
    raw_body = request.get_data(cache=False)
    signature = request.headers.get("X-Hub-Signature-256", "")
    secret = os.environ.get("GITHUB_WEBHOOK_SECRET", "")
    if not verify_github_signature(raw_body, signature, secret):
        return Response(status=401)

    event = json.loads(raw_body) if raw_body else {}
    event_name = request.headers.get("X-GitHub-Event", "")
    delivery_id = request.headers.get("X-GitHub-Delivery", "")

    if event_name == "push":
        enqueue_repository_sync(event["repository"]["full_name"], delivery_id)

    return Response(status=202)
