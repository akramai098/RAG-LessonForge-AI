
from core.llm_client import generate_text


def generate_lesson(
    topic: str = "Introduction to RAG",
    learner_level: str = "Complete Beginner",
    previous_lesson: str = "",
    evaluator_feedback: str = "",
    memory_context: str = ""
) -> str:

    prompt = f"""
You are an expert instructional designer, subject-matter educator,
and educational content creator.

Your task is to create a complete, accurate, high-quality lesson
on the exact topic provided below.

TOPIC: {topic}
LEARNER LEVEL: {learner_level}

IMPORTANT TOPIC INSTRUCTIONS:

1. Focus entirely on the requested topic: {topic}.
2. Do not automatically explain RAG unless RAG is the requested topic
   or is directly relevant to the requested topic.
3. Identify the most important concepts, principles, terminology,
   and skills associated with the requested topic.
4. Adapt the lesson content to the subject. For example:
   - Programming topics should include relevant code examples.
   - AI/ML topics should explain relevant algorithms and concepts.
   - Science topics should explain relevant principles and processes.
   - Business topics should include relevant practical scenarios.
5. Never force unrelated concepts into the lesson.

LESSON REQUIREMENTS:

1. Explain the topic accurately.
2. Assume the learner has no previous knowledge.
3. Use simple, beginner-friendly English.
4. Explain technical terms when they first appear.
5. Include at least one practical, realistic example.
6. Cover the essential concepts relevant to the requested topic.
7. Explain processes and concepts in a logical order.
8. Include real-world applications or use cases where relevant.
9. Include a short conclusion and summary.
10. Do not invent facts or make unsupported claims.

REQUIRED LESSON STRUCTURE:

# {topic}

## 1. Learning Objectives
## 2. Introduction
## 3. Understanding the Topic
## 4. Key Concepts and Terminology
## 5. How It Works
## 6. Practical Example
## 7. Real-World Applications
## 8. Summary and Conclusion

Adapt section content to the requested topic.
If a section is not relevant, replace it with a more useful
topic-specific section.

PREVIOUS LESSON:
{previous_lesson if previous_lesson else "No previous lesson. This is the first attempt."}

EVALUATOR FEEDBACK:
{evaluator_feedback if evaluator_feedback else "No evaluator feedback. Generate the initial lesson."}

PERSISTENT MEMORY FROM PREVIOUS RUNS:
{memory_context if memory_context else "No previous learning rules. Follow all lesson requirements carefully."}

IMPORTANT:

- If evaluator feedback is provided, carefully correct every identified problem.
- Preserve correct information while improving failed sections.
- Use persistent memory rules to avoid repeating previous mistakes.
- Keep the lesson focused on the exact requested topic.
- Do not include unrelated topic-specific requirements.
- Return only the complete lesson in Markdown.

"""

    lesson = generate_text(
        prompt=prompt,
        temperature=0.3,
        max_output_tokens=4000
    )

    return lesson.strip()
