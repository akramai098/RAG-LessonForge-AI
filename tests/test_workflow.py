
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

    received_topics = []

    monkeypatch.setattr(
        workflow,
        "generate_lesson",
        lambda **kwargs: "Generated lesson"
    )

    def mock_evaluator(lesson, topic="Introduction to RAG"):
        received_topics.append(topic)
        return evaluations.pop(0)

    monkeypatch.setattr(
        workflow,
        "evaluate_lesson",
        mock_evaluator
    )

    result = workflow.run_lesson_workflow(
        topic="Introduction to Machine Learning"
    )

    assert result["status"] == "PASS"
    assert result["attempts"] == 2
    assert result["topic"] == "Introduction to Machine Learning"
    assert received_topics == [
        "Introduction to Machine Learning",
        "Introduction to Machine Learning"
    ]

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
        lambda lesson, topic="Introduction to RAG": make_evaluation("FAIL")
    )

    result = workflow.run_lesson_workflow(
        topic="Python Programming"
    )

    assert result["status"] == "FAIL"
    assert result["attempts"] == 3
    assert result["topic"] == "Python Programming"

    assert not (output_dir / "approved_lesson.md").exists()
    assert (rejection_dir / "rejection_log.json").exists()
