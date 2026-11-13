
import streamlit as st

from core.workflow import run_lesson_workflow
from memory.memory_manager import load_memory


# Page configuration
st.set_page_config(
    page_title="RAG-LessonForge AI",
    page_icon="📚",
    layout="wide"
)


# Application heading
st.title("📚 RAG-LessonForge AI")
st.subheader("Self-Improving AI Lesson Generation System")

st.write(
    "Generate educational lessons using AI, "
    "evaluate their quality, and automatically improve them."
)

st.divider()


# Sidebar
st.sidebar.title("About the Project")
st.sidebar.write(
    "RAG-LessonForge AI uses multiple AI components "
    "to generate, evaluate, and improve educational content."
)

st.sidebar.info(
    "Maximum attempts: 3 "
    "(1 initial generation + 2 retries)"
)


# Lesson generation section
st.header("Generate a New Lesson")

topic = st.text_input(
    "Enter your lesson topic",
    value="Introduction to RAG",
    placeholder="Example: Introduction to Machine Learning"
)

generate_button = st.button(
    "🚀 Generate Lesson",
    type="primary"
)


if generate_button:

    if not topic.strip():
        st.warning("Please enter a lesson topic.")

    else:

        with st.spinner(
            "Generating and evaluating your lesson. Please wait..."
        ):

            try:
                result = run_lesson_workflow(topic=topic)

                st.session_state["workflow_result"] = result

            except Exception as error:
                st.error(f"Workflow error: {error}")


# Display workflow result
if "workflow_result" in st.session_state:

    result = st.session_state["workflow_result"]

    st.divider()
    st.header("Workflow Results")

    if result["status"] == "PASS":

        st.success("Lesson successfully approved!")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Final Status", "PASS")

        with col2:
            st.metric("Total Attempts", result["attempts"])

        st.subheader("Approved Lesson")

        st.markdown(result["lesson"])

        st.download_button(
            label="📥 Download Approved Lesson",
            data=result["lesson"],
            file_name="approved_lesson.md",
            mime="text/markdown"
        )

    else:

        st.error("Lesson was rejected after maximum retries.")

        st.metric("Total Attempts", result["attempts"])

        st.warning(
            "Check storage/rejection_logs/rejection_log.json "
            "for evaluation feedback."
        )


# Persistent memory dashboard
st.divider()
st.header("🧠 Persistent Learning Memory")

memory = load_memory()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Evaluations",
        memory["total_runs"]
    )

with col2:
    st.metric(
        "Successful Evaluations",
        memory["total_passes"]
    )

with col3:
    st.metric(
        "Failed Evaluations",
        memory["total_failures"]
    )

st.subheader("Learned Improvement Rules")

rules = memory.get("improvement_rules", [])

if rules:

    for index, rule in enumerate(rules, start=1):
        st.write(f"{index}. {rule}")

else:

    st.info("No improvement rules learned yet.")

st.caption("RAG-LessonForge AI | GenAI Content Systems")
