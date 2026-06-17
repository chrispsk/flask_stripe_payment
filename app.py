import os

import stripe
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, jsonify

load_dotenv()

app = Flask(__name__)

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

DOMAIN = os.environ.get("DOMAIN", "http://localhost:5000")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            submit_type="donate",
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": 1999,
                        "product_data": {
                            "name": "Donation",
                            "description": "Donate for a good cause",
                        },
                    },
                    "quantity": 1,
                }
            ],
            success_url=f"{DOMAIN}/thankyou?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{DOMAIN}/cancel",
        )

        return redirect(session.url, code=303)

    except Exception as e:
        return jsonify(error=str(e)), 400


@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html", amount=19.99)


@app.route("/cancel")
def cancel():
    return render_template("cancel.html")


@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    if not STRIPE_WEBHOOK_SECRET:
        return jsonify(error="STRIPE_WEBHOOK_SECRET is not configured"), 500

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=STRIPE_WEBHOOK_SECRET,
        )
    except ValueError:
        return jsonify(error="Invalid payload"), 400
    except stripe.SignatureVerificationError:
        return jsonify(error="Invalid signature"), 400

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        # TODO: aici pui logica reală:
        # - marchezi donația ca plătită în DB
        # - trimiți email
        # - actualizezi comanda etc.
        print("Payment succeeded:", session.get("id"))

    return jsonify(received=True), 200


if __name__ == "__main__":
    app.run(debug=True)
