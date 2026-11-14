
import json
from datetime import datetime
from pathlib import Path

from agents.generator import generate_lesson
from agents.evaluator import evaluate_lesson
from core.retry_manager import MAX_RETRIES, should_retry, build_feedback

from memory.memory_manager import (
    get_memory_guidance,
    update_memory
)


OUTPUT_DIR = Path("storage/lesson_output")
REJECTION_DIR = Path("storage/rejection_logs")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REJECTION_DIR.mkdir(parents=True, exist_ok=True)


def run_lesson_workflow(
    topic="Introduction to RAG",
    initial_lesson=None
):
    """
    Generate, evaluate, and improve a lesson on any requested topic.

    Maximum attempts = 1 initial attempt + 2 retries.
    Persistent memory learns from every evaluation.
    """

    previous_lesson = ""
    feedback = ""
    rejection_history = []

    total_attempts = MAX_RETRIES + 1

    # Remove old results before starting a new workflow.
    old_approval = OUTPUT_DIR / "approved_lesson.md"
    old_report = OUTPUT_DIR / "final_evaluation.json"
    old_rejection_log = REJECTION_DIR / "rejection_log.json"

    for old_file in [old_approval, old_report, old_rejection_log]:
        if old_file.exists():
            old_file.unlink()

    for attempt in range(1, total_attempts + 1):

        print(f"\n{'=' * 55}")
        print(f"LESSON GENERATION - ATTEMPT {attempt}")
        print(f"TOPIC: {topic}")
        print(f"{'=' * 55}")

        if attempt == 1 and initial_lesson is not None:
            lesson = initial_lesson
            print("Using supplied initial lesson for evaluation.")

        else:
            memory_context = get_memory_guidance()

            lesson = generate_lesson(
                topic=topic,
                learner_level="Complete Beginner",
                previous_lesson=previous_lesson,
                evaluator_feedback=feedback,
                memory_context=memory_context
            )

        print("Evaluating lesson...")

        # Pass the requested topic to the evaluator.
        evaluation = evaluate_lesson(
            lesson=lesson,
            topic=topic
        )

        # Save what the system learned from this evaluation.
        update_memory(
            topic=topic,
            attempt=attempt,
            evaluation=evaluation
        )

        print("\nEvaluation:", evaluation.overall_status)

        for name, criterion in evaluation.criteria.items():
            print(f"{name}: {criterion.status}")

        attempt_record = {
            "topic": topic,
            "attempt": attempt,
            "timestamp": datetime.now().isoformat(),
            "status": evaluation.overall_status,
            "criteria": {
                name: result.model_dump()
                for name, result in evaluation.criteria.items()
            },
            "summary": evaluation.summary
        }

        # Approve only when every criterion passes.
        if evaluation.overall_status == "PASS":

            approved_path = OUTPUT_DIR / "approved_lesson.md"
            approved_path.write_text(lesson, encoding="utf-8")

            report_path = OUTPUT_DIR / "final_evaluation.json"
            report_path.write_text(
                json.dumps(
                    attempt_record,
                    indent=4,
                    ensure_ascii=False
                ),
                encoding="utf-8"
            )

            print("\nSUCCESS: Lesson approved!")
            print("Approved lesson:", approved_path)

            return {
                "status": "PASS",
                "topic": topic,
                "lesson": lesson,
                "attempts": attempt,
                "evaluation": evaluation
            }

        # Record every rejected attempt.
        rejection_history.append(attempt_record)

        rejection_path = REJECTION_DIR / "rejection_log.json"

        rejection_path.write_text(
            json.dumps(
                rejection_history,
                indent=4,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

        print("\nLesson rejected.")

        if should_retry(attempt, evaluation.overall_status):
            previous_lesson = lesson
            feedback = build_feedback(evaluation)
            print("Preparing an improved version...")

        else:
            print("Maximum retries reached. Lesson remains rejected.")

    return {
        "status": "FAIL",
        "topic": topic,
        "lesson": None,
        "attempts": total_attempts,
        "evaluation": None
    }
