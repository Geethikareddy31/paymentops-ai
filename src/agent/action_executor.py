import random


def execute_action(action, incident):

    # -----------------------------------------
    # Retry payment
    # -----------------------------------------

    if action == "RETRY_PAYMENT":

        # Simulate a payment gateway response
        success = random.random() < 0.80

        if success:

            return {
                "status": "SUCCESS",
                "message": "Payment retry succeeded.",
                "amount_recovered": incident["amount"]
            }

        else:

            return {
                "status": "FAILED",
                "message": "Payment retry failed again.",
                "amount_recovered": 0
            }


    # -----------------------------------------
    # Retry webhook
    # -----------------------------------------

    if action == "RETRY_WEBHOOK":

        success = random.random() < 0.90

        if success:

            return {
                "status": "SUCCESS",
                "message": "Webhook delivered successfully.",
                "amount_recovered": 0
            }

        else:

            return {
                "status": "FAILED",
                "message": "Webhook retry failed.",
                "amount_recovered": 0
            }


    # -----------------------------------------
    # No automatic action
    # -----------------------------------------

    if action == "NO_RETRY":

        return {
            "status": "SKIPPED",
            "message": "Automatic retry was intentionally avoided.",
            "amount_recovered": 0
        }


    # -----------------------------------------
    # Customer correction
    # -----------------------------------------

    if action == "CUSTOMER_CORRECTION":

        return {
            "status": "WAITING",
            "message": "Customer action is required.",
            "amount_recovered": 0
        }


    # -----------------------------------------
    # Escalation
    # -----------------------------------------

    if action == "ESCALATE":

        return {
            "status": "ESCALATED",
            "message": "Incident escalated for human review.",
            "amount_recovered": 0
        }


    # -----------------------------------------
    # Human review / unknown action
    # -----------------------------------------

    return {
        "status": "HUMAN_REVIEW",
        "message": "No automatic action was executed.",
        "amount_recovered": 0
    }