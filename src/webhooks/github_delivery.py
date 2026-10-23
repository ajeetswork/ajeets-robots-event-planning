from flask import Blueprint, Response, request

github_webhooks = Blueprint("github_webhooks", __name__)


def enqueue_repository_sync(repository: str, delivery_id: str) -> None:
    print(f"repo-sync:{repository}:{delivery_id}")


@github_webhooks.post("/webhooks/github")
def github_delivery_webhook():
    event = request.get_json(force=True)
    event_name = request.headers.get("X-GitHub-Event", "")
    delivery_id = request.headers.get("X-GitHub-Delivery", "")

    if event_name == "push":
        enqueue_repository_sync(event["repository"]["full_name"], delivery_id)

    return Response(status=202)
