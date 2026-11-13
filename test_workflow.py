
from core.workflow import run_lesson_workflow


print("\nSTARTING RAG LESSONFORGE AI")
print("Maximum retries: 2")

result = run_lesson_workflow()

print("\n" + "=" * 55)
print("FINAL WORKFLOW RESULT")
print("=" * 55)

print("Status:", result["status"])
print("Total attempts:", result["attempts"])

if result["status"] == "PASS":
    print("Lesson successfully approved!")
    print("Saved at: storage/lesson_output/approved_lesson.md")
else:
    print("Lesson rejected after maximum attempts.")
    print("Check: storage/rejection_logs/rejection_log.json")
