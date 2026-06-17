# Flask Stripe Payment

A simple Flask application that integrates Stripe Checkout Sessions for accepting donation payments.

## Features

* Flask backend
* Stripe Checkout payment flow
* Donation button
* Success page
* Cancel page
* Stripe webhook endpoint
* Environment variable configuration with `.env`

## Project Structure

```text
flask_stripe_payment/
├── app.py
├── requirements.txt
├── .env.example
└── templates/
    ├── index.html
    ├── thankyou.html
    └── cancel.html
```

## Requirements

* Python 3.10+
* A Stripe account
* Stripe test API keys

## Installation

Clone the repository:

```bash
git clone https://github.com/chrispsk/flask_stripe_payment.git
cd flask_stripe_payment
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

```bash
# Windows
.venv\Scripts\activate
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the root of the project.

You can copy the example file:

```bash
# Windows
copy .env.example .env
```

```bash
# macOS / Linux
cp .env.example .env
```

Then update `.env` with your own Stripe keys:

```env
STRIPE_SECRET_KEY=sk_test_your_secret_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
DOMAIN=http://localhost:5000
```

Do not commit your `.env` file to GitHub.

## Running the App

Start the Flask app:

```bash
python app.py
```

Open your browser and go to:

```text
http://localhost:5000
```

Click the donation button to start a Stripe Checkout payment.

## Stripe Test Card

Use Stripe's test card:

```text
4242 4242 4242 4242
```

Use any future expiration date, any CVC, and any ZIP/postal code.

## Webhook Testing

To test Stripe webhooks locally, install the Stripe CLI and run:

```bash
stripe listen --forward-to localhost:5000/webhook
```

Stripe will return a webhook signing secret that starts with:

```text
whsec_
```

Copy that value into your `.env` file:

```env
STRIPE_WEBHOOK_SECRET=whsec_your_real_webhook_secret
```

The app listens for the following event:

```text
checkout.session.completed
```

This event is triggered when a Checkout payment is completed successfully.

## Important Notes

This project is intended for learning and testing purposes.

Before using it in production, you should:

* Add proper database storage for payments
* Add logging
* Improve error handling
* Configure production Stripe keys
* Set `DOMAIN` to your production domain
* Deploy over HTTPS
* Keep all secret keys out of GitHub

## License

This project is open source and available for educational use.
