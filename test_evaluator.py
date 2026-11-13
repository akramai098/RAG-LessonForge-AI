
import json

from agents.evaluator import evaluate_lesson


with open(
    "storage/lesson_output/first_lesson.md",
    "r",
    encoding="utf-8"
) as file:
    lesson = file.read()

print("\nEvaluating your generated RAG lesson...\n")

result = evaluate_lesson(lesson)

print("=" * 55)
print("LESSON EVALUATION REPORT")
print("=" * 55)

for name, criterion in result.criteria.items():
    print(f"\n{name.upper()}: {criterion.status}")
    print(f"Reason: {criterion.reason}")
    print(f"Evidence: {criterion.evidence}")

print("\n" + "=" * 55)
print("OVERALL RESULT:", result.overall_status)
print("SUMMARY:", result.summary)

with open(
    "storage/lesson_output/evaluation_report.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        result.model_dump(),
        file,
        indent=4,
        ensure_ascii=False
    )

print("\nEvaluation report saved successfully!")
