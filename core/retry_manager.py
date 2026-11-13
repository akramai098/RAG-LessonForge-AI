
MAX_RETRIES = 2


def should_retry(attempt_number: int, overall_status: str) -> bool:
    """Decide whether another generation attempt is allowed."""

    if overall_status == "PASS":
        return False

    return attempt_number <= MAX_RETRIES


def build_feedback(evaluation) -> str:
    """Convert failed evaluation criteria into actionable feedback."""

    feedback = []

    for name, criterion in evaluation.criteria.items():
        if criterion.status == "FAIL":
            feedback.append(
                f"""
Criterion: {name}
Problem: {criterion.reason}
Required improvement: Correct this problem clearly.
Evidence missing or insufficient: {criterion.evidence}
"""
            )

    if not feedback:
        return "Review the lesson carefully and improve its quality."

    return "\n".join(feedback)
