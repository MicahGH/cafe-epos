"""Class for a mock payment gateway used in the API."""

import uuid

from api.models import Payment


class MockPaymentGateway:
    """Class for a mock payment gateway used in the API."""

    FAILURE_VALUE_FOR_DEMO = 13

    def create_payment_intent(self, amount_p: int) -> dict:
        """Create a dummy payment intent."""
        payment_intent_id = str(uuid.uuid4())
        client_secret = str(uuid.uuid4())
        if amount_p == self.FAILURE_VALUE_FOR_DEMO:
            return {
                "id": payment_intent_id,
                "client_secret": client_secret,
                "status": Payment.Status.FAILED.value,
            }
        return {
            "id": payment_intent_id,
            "client_secret": client_secret,
            "status": Payment.Status.PENDING.value,
        }

    def confirm_payment_intent(self, intent_id: uuid.UUID) -> dict:
        """Create a dummy payment confirmation."""
        return {"id": intent_id, "status": Payment.Status.COMPLETED.value}
