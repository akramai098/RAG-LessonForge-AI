
from core import workflow
from types import SimpleNamespace
from agents.evaluator import CriterionResult


def make_evaluation(status):
    criteria = {
        name: CriterionResult(
            status=status,
            reason="Test reason",
            evidence="Test evidence"
        )
        for name in [
            "accuracy",
            "beginner_friendly",
            "practical_example",
            "jargon_explained",
            "topic_coverage",
            "logical_flow"
        ]
    }

    return SimpleNamespace(
        overall_status=status,
        criteria=criteria,
        summary="Workflow test"
    )


def setup_test_environment(tmp_path, monkeypatch):
    output_dir = tmp_path / "lesson_output"
    rejection_dir = tmp_path / "rejection_logs"

    # Create temporary folders.
    output_dir.mkdir(parents=True, exist_ok=True)
    rejection_dir.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(workflow, "OUTPUT_DIR", output_dir)
    monkeypatch.setattr(workflow, "REJECTION_DIR", rejection_dir)

    monkeypatch.setattr(
        workflow,
        "get_memory_guidance",
        lambda: "Test memory"
    )

    monkeypatch.setattr(
        workflow,
        "update_memory",
        lambda **kwargs: None
    )

    return output_dir, rejection_dir


def test_workflow_passes_after_one_retry(tmp_path, monkeypatch):
    output_dir, rejection_dir = setup_test_environment(
        tmp_path, monkeypatch
    )

    evaluations = [
        make_evaluation("FAIL"),
        make_evaluation("PASS")
    ]

    monkeypatch.setattr(
        workflow,
        "generate_lesson",
        lambda **kwargs: "Generated lesson"
    )

    monkeypatch.setattr(
        workflow,
        "evaluate_lesson",
        lambda lesson: evaluations.pop(0)
    )

    result = workflow.run_lesson_workflow()

    assert result["status"] == "PASS"
    assert result["attempts"] == 2

    assert (output_dir / "approved_lesson.md").exists()
    assert (output_dir / "final_evaluation.json").exists()


def test_workflow_fails_after_maximum_retries(
    tmp_path, monkeypatch
):
    output_dir, rejection_dir = setup_test_environment(
        tmp_path, monkeypatch
    )

    monkeypatch.setattr(
        workflow,
        "generate_lesson",
        lambda **kwargs: "Generated lesson"
    )

    monkeypatch.setattr(
        workflow,
        "evaluate_lesson",
        lambda lesson: make_evaluation("FAIL")
    )

    result = workflow.run_lesson_workflow()

    assert result["status"] == "FAIL"
    assert result["attempts"] == 3

    assert not (output_dir / "approved_lesson.md").exists()
    assert (rejection_dir / "rejection_log.json").exists()
