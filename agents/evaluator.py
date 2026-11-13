
import json
import re

from pydantic import BaseModel, Field

from core.llm_client import generate_text
from core.rubric import RUBRIC, REQUIRED_CRITERIA


class CriterionResult(BaseModel):
    status: str = Field(description="Must be PASS or FAIL")
    reason: str
    evidence: str


class EvaluationResult(BaseModel):
    overall_status: str
    criteria: dict[str, CriterionResult]
    summary: str


def evaluate_lesson(lesson: str) -> EvaluationResult:
    """
    Independently evaluate a generated lesson against
    six strict pass/fail criteria.
    """

    rubric_text = json.dumps(RUBRIC, indent=2)

    prompt = f"""
You are a strict educational quality evaluator.

Evaluate the lesson below using EVERY criterion in the rubric.

RUBRIC:
{rubric_text}

RULES:
1. Evaluate the actual lesson, not what you think it intended to say.
2. Each criterion must independently receive PASS or FAIL.
3. PASS only when the requirement is clearly satisfied.
4. If evidence is missing or insufficient, assign FAIL.
5. Do not give partial credit.
6. Do not allow strong performance in one criterion to compensate
   for failure in another.
7. Include a short reason and direct evidence for each criterion.
8. overall_status must be PASS only if ALL six criteria pass.
9. Use exactly these six criterion keys:
   accuracy, beginner_friendly, practical_example,
   jargon_explained, topic_coverage, logical_flow.

LESSON:
<lesson>
{lesson}
</lesson>

Return ONLY valid JSON in this exact structure:

{{
  "overall_status": "PASS or FAIL",
  "criteria": {{
    "accuracy": {{
      "status": "PASS or FAIL",
      "reason": "Explanation",
      "evidence": "Evidence from the lesson"
    }},
    "beginner_friendly": {{
      "status": "PASS or FAIL",
      "reason": "Explanation",
      "evidence": "Evidence from the lesson"
    }},
    "practical_example": {{
      "status": "PASS or FAIL",
      "reason": "Explanation",
      "evidence": "Evidence from the lesson"
    }},
    "jargon_explained": {{
      "status": "PASS or FAIL",
      "reason": "Explanation",
      "evidence": "Evidence from the lesson"
    }},
    "topic_coverage": {{
      "status": "PASS or FAIL",
      "reason": "Explanation",
      "evidence": "Evidence from the lesson"
    }},
    "logical_flow": {{
      "status": "PASS or FAIL",
      "reason": "Explanation",
      "evidence": "Evidence from the lesson"
    }}
  }},
  "summary": "Short overall evaluation"
}}
"""

    response = generate_text(
        prompt=prompt,
        temperature=0,
        max_output_tokens=3000
    )

    # Remove Markdown code fences if the model includes them.
    cleaned_response = re.sub(
        r"^```(?:json)?\s*|\s*```$",
        "",
        response.strip(),
        flags=re.IGNORECASE
    )

    data = json.loads(cleaned_response)

    # Validate the model's output structure.
    result = EvaluationResult.model_validate(data)

    # Enforce exactly six required criteria.
    if set(result.criteria.keys()) != set(REQUIRED_CRITERIA):
        raise ValueError("Evaluator returned missing or unexpected criteria.")

    # Validate status values.
    for name, criterion in result.criteria.items():
        if criterion.status not in {"PASS", "FAIL"}:
            raise ValueError(f"Invalid status for criterion: {name}")

    # Independently calculate the final result.
    all_passed = all(
        result.criteria[name].status == "PASS"
        for name in REQUIRED_CRITERIA
    )

    expected_status = "PASS" if all_passed else "FAIL"

    if result.overall_status != expected_status:
        raise ValueError(
            "Evaluator overall status does not match individual criteria."
        )

    return result
