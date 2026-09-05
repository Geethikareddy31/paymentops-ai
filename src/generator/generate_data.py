import random
import csv
from datetime import datetime, timedelta


random.seed(42)


INCIDENT_TYPES = [
    "INSUFFICIENT_FUNDS",
    "INVALID_CARD",
    "EXPIRED_CARD",
    "RISK_DECLINE",
    "ISSUER_DECLINE",
    "NETWORK_TIMEOUT",
    "GATEWAY_ERROR",
    "WEBHOOK_FAILURE"
]

METHODS = ["CARD", "UPI", "NETBANKING"]

ISSUERS = ["HDFC", "ICICI", "SBI", "AXIS", "KOTAK"]

RESPONSE_CODES = [
    "DECLINED",
    "AUTH_FAILED",
    "BANK_ERROR",
    "TIMEOUT",
    "NO_RESPONSE",
    "SERVICE_UNAVAILABLE",
    "SUCCESS"
]


def generate_incident(transaction_number):

    true_label = random.choice(INCIDENT_TYPES)

    transaction_id = f"TXN{transaction_number:05d}"

    amount = random.randint(100, 50000)

    timestamp = datetime.now() - timedelta(
        minutes=random.randint(0, 1440)
    )

    method = random.choice(METHODS)

    issuer = random.choice(ISSUERS)

    retry_count = random.randint(0, 2)

    gateway_response_code = random.choice(RESPONSE_CODES)

    gateway_response_time_ms = random.randint(
        200, 3000
    )

    webhook_status = random.choice(
        ["delivered", "pending", "failed"]
    )

    webhook_attempts = random.randint(0, 3)

    recent_same_issuer_failures = random.randint(
        0, 100
    )

    recent_same_method_failures = random.randint(
        0, 150
    )

    failure_rate_last_5min = round(
        random.uniform(0.01, 0.95),
        2
    )

    # -----------------------------------------
    # New diagnostic evidence
    # -----------------------------------------

    card_validity = random.choice([
        "valid",
        "invalid"
    ])

    card_expiry_days = random.randint(
        -365, 1000
    )

    available_balance = random.randint(
        500, 100000
    )

    risk_score = round(
        random.uniform(0.01, 0.99),
        2
    )

    customer_attempts_last_10min = random.randint(
        1, 10
    )

    # -----------------------------------------
    # Incident-specific patterns
    # -----------------------------------------

    if true_label == "INSUFFICIENT_FUNDS":

        method = random.choice(["CARD", "UPI"])

        gateway_response_code = random.choice([
            "DECLINED",
            "BANK_ERROR",
            "AUTH_FAILED"
        ])

        gateway_response_time_ms = random.randint(
            300, 2200
        )

        available_balance = random.randint(
            100, max(100, amount - 1)
        )

        card_validity = "valid"

        card_expiry_days = random.randint(
            30, 1000
        )

        risk_score = round(
            random.uniform(0.05, 0.65),
            2
        )

        customer_attempts_last_10min = random.randint(
            1, 4
        )

        recent_same_issuer_failures = random.randint(
            0, 20
        )

        failure_rate_last_5min = round(
            random.uniform(0.01, 0.25),
            2
        )


    elif true_label == "INVALID_CARD":

        method = "CARD"

        gateway_response_code = random.choice([
            "DECLINED",
            "AUTH_FAILED"
        ])

        gateway_response_time_ms = random.randint(
            200, 1800
        )

        card_validity = "invalid"

        card_expiry_days = random.randint(
            30, 1000
        )

        available_balance = random.randint(
            amount, 100000
        )

        risk_score = round(
            random.uniform(0.05, 0.60),
            2
        )

        customer_attempts_last_10min = random.randint(
            1, 4
        )

        recent_same_issuer_failures = random.randint(
            0, 15
        )

        failure_rate_last_5min = round(
            random.uniform(0.01, 0.20),
            2
        )


    elif true_label == "EXPIRED_CARD":

        method = "CARD"

        gateway_response_code = random.choice([
            "DECLINED",
            "AUTH_FAILED"
        ])

        gateway_response_time_ms = random.randint(
            200, 1800
        )

        card_validity = "valid"

        card_expiry_days = random.randint(
            -365, -1
        )

        available_balance = random.randint(
            amount, 100000
        )

        risk_score = round(
            random.uniform(0.05, 0.60),
            2
        )

        customer_attempts_last_10min = random.randint(
            1, 4
        )

        recent_same_issuer_failures = random.randint(
            0, 15
        )

        failure_rate_last_5min = round(
            random.uniform(0.01, 0.20),
            2
        )


    elif true_label == "RISK_DECLINE":

        method = random.choice([
            "CARD",
            "UPI"
        ])

        gateway_response_code = random.choice([
            "DECLINED",
            "AUTH_FAILED"
        ])

        gateway_response_time_ms = random.randint(
            400, 3000
        )

        card_validity = random.choice([
            "valid",
            "invalid"
        ])

        card_expiry_days = random.randint(
            -30, 1000
        )

        available_balance = random.randint(
            amount, 100000
        )

        risk_score = round(
            random.uniform(0.65, 0.99),
            2
        )

        customer_attempts_last_10min = random.randint(
            4, 10
        )

        recent_same_issuer_failures = random.randint(
            0, 30
        )

        failure_rate_last_5min = round(
            random.uniform(0.05, 0.40),
            2
        )


    elif true_label == "ISSUER_DECLINE":

        method = random.choice([
            "CARD",
            "UPI"
        ])

        gateway_response_code = random.choice([
            "DECLINED",
            "BANK_ERROR",
            "AUTH_FAILED"
        ])

        gateway_response_time_ms = random.randint(
            300, 3500
        )

        card_validity = "valid"

        card_expiry_days = random.randint(
            30, 1000
        )

        available_balance = random.randint(
            amount, 100000
        )

        risk_score = round(
            random.uniform(0.05, 0.70),
            2
        )

        customer_attempts_last_10min = random.randint(
            1, 5
        )

        recent_same_issuer_failures = random.randint(
            10, 70
        )

        failure_rate_last_5min = round(
            random.uniform(0.15, 0.75),
            2
        )


    elif true_label == "NETWORK_TIMEOUT":

        method = random.choice(METHODS)

        gateway_response_code = random.choice([
            "TIMEOUT",
            "NO_RESPONSE"
        ])

        gateway_response_time_ms = random.randint(
            5000, 10000
        )

        card_validity = "valid"

        card_expiry_days = random.randint(
            30, 1000
        )

        available_balance = random.randint(
            amount, 100000
        )

        risk_score = round(
            random.uniform(0.05, 0.70),
            2
        )

        customer_attempts_last_10min = random.randint(
            1, 5
        )

        recent_same_issuer_failures = random.randint(
            0, 30
        )

        failure_rate_last_5min = round(
            random.uniform(0.05, 0.55),
            2
        )

        webhook_status = random.choice([
            "pending",
            "failed"
        ])

        webhook_attempts = random.randint(
            1, 3
        )


    elif true_label == "GATEWAY_ERROR":

        method = random.choice(METHODS)

        gateway_response_code = random.choice([
            "SERVICE_UNAVAILABLE",
            "BANK_ERROR",
            "NO_RESPONSE"
        ])

        gateway_response_time_ms = random.randint(
            2500, 9000
        )

        card_validity = "valid"

        card_expiry_days = random.randint(
            30, 1000
        )

        available_balance = random.randint(
            amount, 100000
        )

        risk_score = round(
            random.uniform(0.05, 0.70),
            2
        )

        customer_attempts_last_10min = random.randint(
            1, 5
        )

        recent_same_method_failures = random.randint(
            20, 120
        )

        failure_rate_last_5min = round(
            random.uniform(0.20, 0.85),
            2
        )

        webhook_status = random.choice([
            "pending",
            "failed",
            "delivered"
        ])

        webhook_attempts = random.randint(
            0, 3
        )


    elif true_label == "WEBHOOK_FAILURE":

        method = random.choice(METHODS)

        gateway_response_code = "SUCCESS"

        gateway_response_time_ms = random.randint(
            200, 2000
        )

        card_validity = "valid"

        card_expiry_days = random.randint(
            30, 1000
        )

        available_balance = random.randint(
            amount, 100000
        )

        risk_score = round(
            random.uniform(0.05, 0.70),
            2
        )

        customer_attempts_last_10min = random.randint(
            1, 5
        )

        webhook_status = random.choice([
            "failed",
            "pending"
        ])

        webhook_attempts = random.randint(
            2, 5
        )


    # -----------------------------------------
    # Add noise so the features aren't perfect
    # -----------------------------------------

    if random.random() < 0.12:

        gateway_response_code = random.choice([
            "DECLINED",
            "BANK_ERROR",
            "AUTH_FAILED",
            "NO_RESPONSE"
        ])


    if random.random() < 0.10:

        gateway_response_time_ms = random.randint(
            1000, 7000
        )


    if random.random() < 0.10:

        risk_score = round(
            random.uniform(0.20, 0.90),
            2
        )


    if random.random() < 0.10:

        customer_attempts_last_10min = random.randint(
            1, 10
        )


    return {
        "transaction_id": transaction_id,
        "timestamp": timestamp.isoformat(),
        "amount": amount,
        "method": method,
        "issuer": issuer,
        "gateway_response_code": gateway_response_code,
        "gateway_response_time_ms": gateway_response_time_ms,
        "retry_count": retry_count,
        "webhook_status": webhook_status,
        "webhook_attempts": webhook_attempts,
        "recent_same_issuer_failures": recent_same_issuer_failures,
        "recent_same_method_failures": recent_same_method_failures,
        "failure_rate_last_5min": failure_rate_last_5min,
        "card_validity": card_validity,
        "card_expiry_days": card_expiry_days,
        "available_balance": available_balance,
        "risk_score": risk_score,
        "customer_attempts_last_10min": customer_attempts_last_10min,
        "true_label": true_label
    }


def generate_dataset(number_of_records):

    incidents = []

    for i in range(1, number_of_records + 1):

        incidents.append(
            generate_incident(i)
        )

    return incidents


if __name__ == "__main__":

    incidents = generate_dataset(800)

    fieldnames = incidents[0].keys()

    with open(
        "data/incidents.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(incidents)

    print(
        f"Generated {len(incidents)} synthetic incidents."
    )