
from core.llm_client import generate_text


def generate_lesson(
    topic: str = "Introduction to RAG",
    learner_level: str = "Complete Beginner",
    previous_lesson: str = "",
    evaluator_feedback: str = "",
    memory_context: str = ""
) -> str:

    prompt = f"""
You are an expert instructional designer and AI educator.

Create a high-quality educational lesson.

TOPIC: {topic}
LEARNER LEVEL: {learner_level}

LESSON REQUIREMENTS:

1. Explain the topic accurately.
2. Assume the learner has no previous knowledge.
3. Use simple, beginner-friendly English.
4. Explain technical terms when they first appear.
5. Include at least one practical, realistic example.
6. Cover these important RAG concepts:
   - What RAG means
   - Why RAG is needed
   - Retrieval process
   - Augmentation process
   - Generation process
   - Embeddings
   - Vector databases
   - A real-world application
7. Explain the complete process in logical order.
8. Include a short conclusion.
9. Do not invent facts or make unsupported claims.

REQUIRED LESSON STRUCTURE:

# Introduction to RAG

## 1. Learning Objectives
## 2. What is RAG?
## 3. Why Do We Need RAG?
## 4. How RAG Works
## 5. Important Technical Terms
## 6. Practical Real-World Example
## 7. Real-World Applications
## 8. Summary

PREVIOUS LESSON:
{previous_lesson if previous_lesson else "No previous lesson. This is the first attempt."}

EVALUATOR FEEDBACK:
{evaluator_feedback if evaluator_feedback else "No evaluator feedback. Generate the initial lesson."}

PERSISTENT MEMORY FROM PREVIOUS RUNS:
{memory_context if memory_context else "No previous learning rules. Follow all lesson requirements carefully."}

IMPORTANT:

If evaluator feedback is provided, carefully correct every identified problem.

Preserve correct information while improving failed sections.

Use persistent memory rules to avoid repeating previous mistakes.

Return only the complete lesson in Markdown.
"""

    lesson = generate_text(
        prompt=prompt,
        temperature=0.3,
        max_output_tokens=4000
    )

    return lesson.strip()
