# RAG-LessonForge AI

### Self-Improving AI Lesson Generation and Evaluation System

RAG-LessonForge AI is a multi-agent educational content generation system that uses Google's Gemini API to create beginner-friendly lessons about Retrieval-Augmented Generation (RAG), evaluate lesson quality against a structured rubric, and automatically improve rejected content through a controlled retry mechanism.

The system also maintains persistent learning memory to record evaluation results and improvement rules across workflow executions.

---

## Project Overview

Generating educational content with AI is not enough. The content must also be accurate, understandable, complete, and logically structured.

RAG-LessonForge AI addresses this challenge through an automated workflow:

1. Generate an educational lesson.
2. Evaluate the lesson against predefined quality criteria.
3. Identify missing or weak sections.
4. Regenerate the lesson using evaluator feedback.
5. Retry up to two times if the lesson fails.
6. Save approved lessons and rejection logs.
7. Store evaluation history and improvement rules in persistent memory.

The system is designed to demonstrate agent-based content generation, automated quality assurance, controlled retries, and persistent memory.

## Key Features

- **AI Lesson Generation:** Uses Google Gemini to generate beginner-friendly educational content.
- **Automated Evaluation:** Evaluates lessons using a structured six-criterion rubric.
- **Pass/Fail Quality Control:** Approves lessons only when all required criteria pass.
- **Automatic Retry Mechanism:** Allows one initial generation and a maximum of two retries.
- **Evaluator Feedback:** Uses identified failures to guide lesson regeneration.
- **Persistent Learning Memory:** Stores evaluation history, failure counts, and improvement rules.
- **Rejection Logging:** Records rejected attempts and evaluation feedback.
- **Streamlit Interface:** Provides a browser-based interface for running the lesson workflow.
- **Automated Testing:** Includes tests for retry logic, memory management, and workflow behavior.

## System Architecture

The project uses separate components for generation, evaluation, retry management, workflow orchestration, and persistent memory.

```text
                 USER
                   |
                   v
            STREAMLIT APP
                   |
                   v
          WORKFLOW ORCHESTRATOR
                   |
                   v
            LESSON GENERATOR
                   |
                   v
             GEMINI API
                   |
                   v
           GENERATED LESSON
                   |
                   v
            EVALUATOR AGENT
                   |
                   v
          SIX-CRITERION RUBRIC
                   |
             PASS / FAIL
              /       \
             /         \
          PASS         FAIL
           |             |
           v             v
      SAVE LESSON    RETRY MANAGER
           |             |
           v             v
       APPROVED       FEEDBACK
        OUTPUT            |
                         v
                  LESSON GENERATOR
                    (MAX 2 RETRIES)

           PERSISTENT MEMORY
                   |
          Evaluation History
          Failure Statistics
          Improvement Rules
                   |
                   v
          FUTURE GENERATIONS
```

## Evaluation Criteria

Every generated lesson is evaluated against six mandatory criteria.

| Criterion | Description |
|---|---|
| Accuracy | Technical explanations must be accurate and not misleading. |
| Beginner Friendly | Content must be understandable to complete beginners. |
| Practical Example | Must include a realistic, step-by-step example. |
| Jargon Explained | Technical terms must be explained in simple language. |
| Topic Coverage | Must cover all required RAG concepts. |
| Logical Flow | Must follow a clear and organized structure. |

**Approval rule:** All six criteria must pass for a lesson to be approved.

## Retry Mechanism

The system uses a maximum of two retries.

| Attempt | Action |
|---|---|
| Attempt 1 | Generate and evaluate the initial lesson. |
| Attempt 2 | Regenerate using evaluator feedback if the first attempt fails. |
| Attempt 3 | Perform the final retry if the second attempt fails. |

If all three attempts fail, the lesson remains rejected and its evaluation details are saved in the rejection log.

## Persistent Learning Memory

The memory component maintains information across separate workflow executions.

It stores:

- Total evaluation count.
- Successful and failed evaluation counts.
- Failure counts for individual criteria.
- Improvement rules learned from previous failures.
- Evaluation history with timestamps and summaries.

The generator receives saved improvement rules as additional prompt context in future workflow runs.

Memory is implemented using a JSON file rather than an external database.

## Technology Stack

- **Programming Language:** Python
- **LLM:** Google Gemini API
- **AI Integration:** Google Gen AI SDK
- **Frontend:** Streamlit
- **Data Validation:** Pydantic
- **Memory Storage:** JSON
- **Testing:** Pytest
- **Environment Configuration:** Python dotenv

## Project Structure

```text
RAG-LessonForge-AI/
│
├── agents/
│   ├── __init__.py
│   ├── generator.py
│   └── evaluator.py
│
├── core/
│   ├── __init__.py
│   ├── llm_client.py
│   ├── rubric.py
│   ├── retry_manager.py
│   └── workflow.py
│
├── memory/
│   ├── memory_manager.py
│   └── learning_memory.json
│
├── prompts/
│
├── storage/
│   ├── lesson_output/
│   └── rejection_logs/
│
├── tests/
│   ├── test_memory_manager.py
│   ├── test_retry_manager.py
│   └── test_workflow.py
│
├── docs/
│
├── app.py
├── config.py
├── test_connection.py
├── test_generator.py
├── test_evaluator.py
├── test_workflow.py
├── test_failure_demo.py
├── requirements.txt
├── pytest.ini
├── .env
└── .gitignore
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd RAG-LessonForge-AI
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual repository URL.

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

Replace the placeholder with your own Gemini API key.

**Security:** Never commit your `.env` file or expose your API key publicly.

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal, normally:

```text
http://localhost:8501
```

## Running Automated Tests

Run the automated test suite:

```bash
python -m pytest -v
```

The project currently has **11 passing automated tests** covering:

- Retry manager behavior.
- Persistent memory initialization and updates.
- Improvement rule retrieval.
- Successful workflow after a retry.
- Workflow rejection after maximum retries.

The automated workflow tests use mocked generation and evaluation results, so they do not require live Gemini API calls.

## Demonstrating Failure and Recovery

The project includes a deliberate failure demonstration:

```bash
python test_failure_demo.py
```

This supplies an intentionally incomplete lesson to the workflow.

The evaluator identifies missing requirements, provides feedback, and allows the generator to produce an improved lesson.

This demonstrates the automated quality-control and retry process.

## Generated Outputs

The workflow stores its outputs in the `storage/` directory.

**Approved lesson:**

```text
storage/lesson_output/approved_lesson.md
```

**Final evaluation report:**

```text
storage/lesson_output/final_evaluation.json
```

**Rejection history:**

```text
storage/rejection_logs/rejection_log.json
```

**Persistent learning memory:**

```text
memory/learning_memory.json
```

These files provide evidence of lesson approval, evaluation decisions, rejection history, and persistent improvement rules.

## Design Decisions

- **Modular architecture:** Generation, evaluation, memory, and retry responsibilities are separated.
- **Structured evaluation:** Pydantic models validate evaluator responses.
- **Controlled retries:** The system limits regeneration to prevent unlimited API calls.
- **Persistent memory:** JSON provides a lightweight way to retain learning history across runs.
- **Automated testing:** Mocked workflow tests verify core behavior without requiring API access.

## Future Improvements

- Support additional educational topics with topic-specific rubrics.
- Add more detailed evaluation metrics.
- Introduce vector-based retrieval for grounding lessons in reference documents.
- Store memory in a database for larger-scale usage.
- Add lesson export formats such as PDF and DOCX.
- Improve monitoring and workflow observability.

## Project Objective

This project demonstrates practical implementation of Generative AI, multi-agent workflows, automated evaluation, feedback-driven regeneration, retry management, persistent memory, and software testing.

It was developed as a portfolio project for a GenAI Engineer – Content Systems assessment.

---

**Built with Python, Google Gemini, Streamlit, and Pytest.**