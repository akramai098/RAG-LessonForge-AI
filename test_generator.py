
from agents.generator import generate_lesson

print("\nGenerating your first RAG lesson...\n")

lesson = generate_lesson()

print("=" * 60)
print("GENERATED LESSON")
print("=" * 60)

print(lesson)

with open(
    "storage/lesson_output/first_lesson.md",
    "w",
    encoding="utf-8"
) as file:
    file.write(lesson)

print("\nLesson saved successfully!")
print("Location: storage/lesson_output/first_lesson.md")
