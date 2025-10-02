
import os
import stripe

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', '')

def create_payment_intent(amount_cents, currency='usd'):
    if not stripe.api_key:
        raise RuntimeError("Stripe API key not configured.")
    intent = stripe.PaymentIntent.create(
        amount=amount_cents,
        currency=currency
    )
    return intent
