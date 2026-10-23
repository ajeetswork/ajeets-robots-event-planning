import os

from flask import Blueprint, Response, request

from .verification import construct_stripe_event

stripe_webhooks = Blueprint("stripe_webhooks", __name__)


def record_paid_invoice(invoice: dict) -> None:
    print(f"invoice-paid:{invoice['id']}")


@stripe_webhooks.post("/webhooks/stripe")
def stripe_billing_webhook():
    raw_body = request.get_data(cache=False)
    signature = request.headers.get("Stripe-Signature", "")
    secret = os.environ["STRIPE_WEBHOOK_SECRET"]

    try:
        event = construct_stripe_event(raw_body, signature, secret)
    except Exception:
        return Response(status=400)

    if event["type"] == "invoice.paid":
        record_paid_invoice(event["data"]["object"])

    return Response(status=204)
