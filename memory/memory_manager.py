
import json
from pathlib import Path
from datetime import datetime

MEMORY_FILE = Path("memory/learning_memory.json")

DEFAULT_MEMORY = {
    "total_runs": 0,
    "total_passes": 0,
    "total_failures": 0,
    "failure_counts": {},
    "improvement_rules": [],
    "history": []
}


def load_memory():
    """Load persistent memory from JSON."""

    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not MEMORY_FILE.exists():
        save_memory(DEFAULT_MEMORY)

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return DEFAULT_MEMORY.copy()


def save_memory(memory):
    """Save updated memory to JSON."""

    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4, ensure_ascii=False)


def get_memory_guidance():
    """Convert previous failures into instructions for the generator."""

    memory = load_memory()

    rules = memory.get("improvement_rules", [])

    if not rules:
        return "No previous learning history. Follow all lesson requirements carefully."

    return "\n".join(
        f"- {rule}" for rule in rules
    )


def update_memory(topic, attempt, evaluation):
    """Learn from each evaluation and persist the result."""

    memory = load_memory()

    memory["total_runs"] += 1

    if evaluation.overall_status == "PASS":
        memory["total_passes"] += 1
    else:
        memory["total_failures"] += 1

    failed_criteria = []

    for name, criterion in evaluation.criteria.items():

        if criterion.status == "FAIL":
            failed_criteria.append(name)

            memory["failure_counts"][name] = (
                memory["failure_counts"].get(name, 0) + 1
            )

    # Create improvement rules from recurring failures.
    rule_templates = {
        "accuracy": "Verify technical explanations and avoid unsupported claims.",
        "beginner_friendly": "Use simpler language and explain difficult concepts step by step.",
        "practical_example": "Always include a detailed, realistic, step-by-step practical example.",
        "jargon_explained": "Define every important technical term in simple language.",
        "topic_coverage": "Check every required topic before completing the lesson.",
        "logical_flow": "Organize the lesson in a clear sequence from basics to applications."
    }

    for criterion in failed_criteria:
        rule = rule_templates.get(criterion)

        if rule and rule not in memory["improvement_rules"]:
            memory["improvement_rules"].append(rule)

    memory["history"].append({
        "timestamp": datetime.now().isoformat(),
        "topic": topic,
        "attempt": attempt,
        "status": evaluation.overall_status,
        "failed_criteria": failed_criteria,
        "summary": evaluation.summary
    })

    # Keep the history manageable.
    memory["history"] = memory["history"][-100:]

    save_memory(memory)

    print("\nPersistent memory updated!")
    print("Total recorded evaluations:", memory["total_runs"])
    print("Learned improvement rules:", len(memory["improvement_rules"]))
