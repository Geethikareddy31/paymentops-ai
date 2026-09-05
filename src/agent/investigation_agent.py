import ollama


def investigate(incident, diagnosis, confidence, decision, result):

    if decision["action"] in ["HUMAN_REVIEW", "ESCALATE"]:
        attention_required = "Human attention is required."
    elif decision["action"] == "CUSTOMER_CORRECTION":
        attention_required = "Customer action is required."
    elif (
        decision["action"] in ["RETRY_PAYMENT", "RETRY_WEBHOOK"]
        and result["status"] == "FAILED"
    ):
        attention_required = "Human attention may be required because the automatic action failed."
    else:
        attention_required = "No further human attention is required."

    # -----------------------------------------
    # 1. Prepare verified evidence
    # -----------------------------------------

    evidence = f"""
Transaction ID: {incident.get("transaction_id")}
Amount: ₹{incident["amount"]}
Payment method: {incident["method"]}
Issuer: {incident["issuer"]}
Gateway response: {incident["gateway_response_code"]}
Gateway response time: {incident["gateway_response_time_ms"]} ms
Retry count: {incident["retry_count"]}
Webhook status: {incident["webhook_status"]}
Webhook attempts: {incident["webhook_attempts"]}
Recent same-issuer failures: {incident["recent_same_issuer_failures"]}
Recent same-method failures: {incident["recent_same_method_failures"]}
Failure rate last 5 minutes: {incident["failure_rate_last_5min"]}
Card validity: {incident["card_validity"]}
Card expiry days: {incident["card_expiry_days"]}
Available balance: ₹{incident["available_balance"]}
Risk score: {incident["risk_score"]}
Customer attempts last 10 minutes: {incident["customer_attempts_last_10min"]}

Required decision action: {decision["action"]}
Execution result: {result["status"]}
Required decision action: {decision["action"]}
Execution result: {result["status"]}
Verified attention status: {attention_required}
"""


    # -----------------------------------------
    # 2. Give the LLM a strict role
    # -----------------------------------------

    prompt = f"""
You are the explanation layer of PaymentOps AI.

You are NOT the decision maker.

The ML model, Decision Engine, and Action Executor have already
processed this incident. Your job is ONLY to explain what they did.

STRICT RULES:
1. The verified ML diagnosis is the root cause.
2. Do NOT question or change the diagnosis.
3. The Decision Engine action is authoritative.
4. The execution result is authoritative.
5. There was EXACTLY ONE execution for this invocation.
6. Do NOT mention a first execution, second execution, previous execution,
   future execution, or multiple executions.
7. Do NOT invent thresholds, policies, values, events, or evidence.
8. Do NOT infer information that is not provided.
9. Do NOT recommend a different action.
10. Do NOT claim real money was recovered.
11. Only report the amount recovered provided in the execution result.
12. Use the verified attention status exactly as provided.

Explain these five things:

1. Root cause
2. Key evidence
3. Why the Decision Engine selected the action
4. Result of the ONE execution
5. Whether human attention or customer action is required

VERIFIED INCIDENT:
{evidence}

VERIFIED DIAGNOSIS:
{diagnosis}

VERIFIED CONFIDENCE:
{confidence:.2%}

VERIFIED DECISION:
{decision["action"]}

VERIFIED DECISION REASON:
{decision["reason"]}

VERIFIED EXECUTION RESULT:
{result["status"]}

VERIFIED EXECUTION MESSAGE:
{result["message"]}

VERIFIED AMOUNT RECOVERED:
₹{result["amount_recovered"]}

VERIFIED ATTENTION STATUS:
{attention_required}

Write a concise, factual explanation for a merchant support engineer.
"""


    # -----------------------------------------
    # 3. Ask local Ollama model
    # -----------------------------------------

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    # -----------------------------------------
    # 4. Return explanation
    # -----------------------------------------

    return response["message"]["content"]