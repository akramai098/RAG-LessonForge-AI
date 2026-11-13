
from types import SimpleNamespace

from memory import memory_manager


def make_evaluation(status, failed_criteria=None):
    failed_criteria = failed_criteria or []

    criteria = {}

    all_criteria = [
        "accuracy",
        "beginner_friendly",
        "practical_example",
        "jargon_explained",
        "topic_coverage",
        "logical_flow"
    ]

    for name in all_criteria:
        criteria[name] = SimpleNamespace(
            status="FAIL" if name in failed_criteria else "PASS"
        )

    return SimpleNamespace(
        overall_status=status,
        criteria=criteria,
        summary="Automated test evaluation"
    )


def test_memory_starts_with_default_values(tmp_path, monkeypatch):
    memory_file = tmp_path / "learning_memory.json"

    monkeypatch.setattr(
        memory_manager,
        "MEMORY_FILE",
        memory_file
    )

    memory = memory_manager.load_memory()

    assert memory["total_runs"] == 0
    assert memory["total_passes"] == 0
    assert memory["total_failures"] == 0


def test_failed_evaluation_updates_memory(tmp_path, monkeypatch):
    memory_file = tmp_path / "learning_memory.json"

    monkeypatch.setattr(
        memory_manager,
        "MEMORY_FILE",
        memory_file
    )

    evaluation = make_evaluation(
        "FAIL",
        ["practical_example", "jargon_explained"]
    )

    memory_manager.update_memory(
        topic="Introduction to RAG",
        attempt=1,
        evaluation=evaluation
    )

    memory = memory_manager.load_memory()

    assert memory["total_runs"] == 1
    assert memory["total_failures"] == 1
    assert memory["total_passes"] == 0

    assert memory["failure_counts"]["practical_example"] == 1
    assert memory["failure_counts"]["jargon_explained"] == 1

    assert len(memory["improvement_rules"]) == 2
    assert len(memory["history"]) == 1


def test_passed_evaluation_updates_memory(tmp_path, monkeypatch):
    memory_file = tmp_path / "learning_memory.json"

    monkeypatch.setattr(
        memory_manager,
        "MEMORY_FILE",
        memory_file
    )

    evaluation = make_evaluation("PASS")

    memory_manager.update_memory(
        topic="Introduction to RAG",
        attempt=2,
        evaluation=evaluation
    )

    memory = memory_manager.load_memory()

    assert memory["total_runs"] == 1
    assert memory["total_passes"] == 1
    assert memory["total_failures"] == 0
    assert len(memory["history"]) == 1


def test_memory_guidance_returns_saved_rules(tmp_path, monkeypatch):
    memory_file = tmp_path / "learning_memory.json"

    monkeypatch.setattr(
        memory_manager,
        "MEMORY_FILE",
        memory_file
    )

    evaluation = make_evaluation(
        "FAIL",
        ["practical_example"]
    )

    memory_manager.update_memory(
        topic="Introduction to RAG",
        attempt=1,
        evaluation=evaluation
    )

    guidance = memory_manager.get_memory_guidance()

    assert "step-by-step practical example" in guidance
