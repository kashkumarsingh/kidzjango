"""
Service layer for handling payment-related business logic with Stripe.
"""

import stripe
from django.conf import settings
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

# Initialize Stripe with the secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentService:
    @staticmethod
    def create_payment_intent(amount, currency="gbp", metadata=None):
        """
        Creates a Stripe Payment Intent.

        Args:
            amount (int): Amount in pence (e.g., 12500 for £125.00).
            currency (str): Currency code (default: 'gbp').
            metadata (dict): Additional metadata to attach to the payment intent.

        Returns:
            dict: Stripe Payment Intent object.

        Raises:
            stripe.error.StripeError: If there is an issue with Stripe API.
        """
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                metadata=metadata or {},
                payment_method_types=['card'],
            )
            logger.info(f"Created Payment Intent: {payment_intent.id}")
            return payment_intent
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create Payment Intent: {str(e)}")
            raise

    @staticmethod
    def confirm_payment_intent(payment_intent_id):
        """
        Confirms a Stripe Payment Intent.

        Args:
            payment_intent_id (str): The ID of the Payment Intent to confirm.

        Returns:
            dict: Confirmed Stripe Payment Intent object.

        Raises:
            stripe.error.StripeError: If confirmation fails.
        """
        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            if payment_intent.status == 'succeeded':
                logger.info(f"Payment Intent {payment_intent_id} already succeeded.")
                return payment_intent
            payment_intent = stripe.PaymentIntent.confirm(payment_intent_id)
            logger.info(f"Confirmed Payment Intent: {payment_intent_id}")
            return payment_intent
        except stripe.error.StripeError as e:
            logger.error(f"Failed to confirm Payment Intent {payment_intent_id}: {str(e)}")
            raise

    @staticmethod
    def validate_payment_amount(package_price, payment_amount):
        """
        Validates that the payment amount matches the package price.

        Args:
            package_price (str): Package price as a string (e.g., "£125").
            payment_amount (int): Payment amount in pence.

        Raises:
            ValidationError: If the amounts do not match.
        """
        try:
            # Extract numeric value from package price (e.g., "£125" -> 125)
            price = float(package_price.replace("£", "").strip())
            expected_amount = int(price * 100)  # Convert to pence
            if expected_amount != payment_amount:
                raise ValidationError(f"Payment amount ({payment_amount/100} GBP) does not match package price ({price} GBP).")
        except (ValueError, AttributeError) as e:
            logger.error(f"Error validating payment amount: {str(e)}")
            raise ValidationError("Invalid package price format.")