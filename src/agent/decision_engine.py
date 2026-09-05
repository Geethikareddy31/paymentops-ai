CONFIDENCE_THRESHOLD = 0.85
MAX_PAYMENT_RETRIES = 2


def decide_action(diagnosis, confidence, retry_count=0):

    # -----------------------------------------
    # 1. Low confidence = human review
    # -----------------------------------------

    if confidence < CONFIDENCE_THRESHOLD:

        return {
            "action": "HUMAN_REVIEW",
            "reason": "Diagnosis confidence is too low for automatic action."
        }


    # -----------------------------------------
    # 2. Safe retryable incidents
    # -----------------------------------------

    if diagnosis == "NETWORK_TIMEOUT":

        if retry_count >= MAX_PAYMENT_RETRIES:

            return {
                "action": "HUMAN_REVIEW",
                "reason": "Maximum automatic payment retries reached."
            }

        return {
            "action": "RETRY_PAYMENT",
            "reason": "High-confidence network timeout is potentially transient."
        }


    if diagnosis == "GATEWAY_ERROR":

        if retry_count >= MAX_PAYMENT_RETRIES:

            return {
                "action": "HUMAN_REVIEW",
                "reason": "Maximum automatic payment retries reached."
            }

        return {
            "action": "RETRY_PAYMENT",
            "reason": "High-confidence gateway error may be transient."
        }


    # -----------------------------------------
    # 3. Webhook recovery
    # -----------------------------------------

    if diagnosis == "WEBHOOK_FAILURE":

        return {
            "action": "RETRY_WEBHOOK",
            "reason": "Payment succeeded but webhook delivery failed."
        }


    # -----------------------------------------
    # 4. Non-retryable payment problems
    # -----------------------------------------

    if diagnosis == "INSUFFICIENT_FUNDS":

        return {
            "action": "NO_RETRY",
            "reason": "Retrying is unlikely to succeed without additional funds."
        }


    if diagnosis == "INVALID_CARD":

        return {
            "action": "CUSTOMER_CORRECTION",
            "reason": "Customer should provide valid card details."
        }


    if diagnosis == "EXPIRED_CARD":

        return {
            "action": "CUSTOMER_CORRECTION",
            "reason": "Customer should update the expired card."
        }


    # -----------------------------------------
    # 5. Risk-related incident
    # -----------------------------------------

    if diagnosis == "RISK_DECLINE":

        return {
            "action": "ESCALATE",
            "reason": "Risk-related decline should not be automatically retried."
        }


    # -----------------------------------------
    # 6. Issuer decline
    # -----------------------------------------

    if diagnosis == "ISSUER_DECLINE":

        return {
            "action": "ESCALATE",
            "reason": "Issuer decline requires cautious handling."
        }


    # -----------------------------------------
    # 7. Safety fallback
    # -----------------------------------------

    return {
        "action": "HUMAN_REVIEW",
        "reason": "No approved automated action exists for this diagnosis."
    }