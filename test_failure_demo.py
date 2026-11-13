
from core.workflow import run_lesson_workflow

# Deliberately flawed lesson: it has no practical example,
# no explanation of embeddings, and incomplete topic coverage.

bad_lesson = """
# Introduction to RAG

RAG stands for Retrieval-Augmented Generation.

RAG retrieves information and uses an AI model to generate
an answer.

It is useful for answering questions using external information.
"""

print("\nDELIBERATE FAILURE DEMONSTRATION")
print("The initial lesson intentionally misses important requirements.")

result = run_lesson_workflow(
    topic="Introduction to RAG",
    initial_lesson=bad_lesson
)

print("\nDEMO RESULT")
print("Final status:", result["status"])
print("Total attempts:", result["attempts"])
