# CampusMate — Multi-Agent Academic Assistant

CampusMate is a prompt-engineering mini-project built with Python, Streamlit and the Groq API. It uses a central orchestrator and four specialist LLM agents to help students learn and revise.

## Features
- **Tutor Agent:** explains a topic at the selected learning level.
- **Planner Agent:** creates a revision schedule based on the deadline.
- **Quiz Generator Agent:** generates five MCQs and keeps the answer key for evaluation.
- **Evaluator Agent:** checks submitted answers, gives a score, explains mistakes and recommends next steps.
- **Orchestrator:** coordinates the order of agents based on the selected workflow.

## Architecture
User → Orchestrator → (Tutor / Planner / Quiz Generator) → Student answers → Evaluator → Feedback

Each specialist is a separate LLM call with its own system prompt in `prompts.py`. The orchestrator is implemented in `app.py` and coordinates the sequence.

## Requirements
- Python 3.10+
- Internet connection
- Groq API key

## Setup (Windows)
1. Extract the ZIP and open the `campusmate` folder in VS Code.
2. Open the terminal in that folder.
3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate it:
   ```bash
   venv\\Scripts\\activate
   ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Get an API key from https://console.groq.com/ and paste it into the **Groq API key** field in the app sidebar.
7. Run:
   ```bash
   streamlit run app.py
   ```
8. Streamlit will open the app in your browser (usually http://localhost:8501).

## Setup (macOS / Linux)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
Enter your Groq API key in the app sidebar.

## Suggested demo
1. Select **Complete Study Pack**.
2. Topic: `Named Entity Recognition in NLP`.
3. Level: `Intermediate`.
4. Deadline: `in 3 days`.
5. Click **Run CampusMate**.
6. Review the Tutor explanation, Planner schedule and five MCQs.
7. Answer all questions and click **Submit answers for evaluation**.

## Project structure
```text
campusmate/
├── app.py
├── agents.py
├── prompts.py
├── requirements.txt
├── .env.example
├── README.md
└── PROJECT_REPORT.md
```

## Prompt-engineering techniques demonstrated
- Role prompting: each agent receives a clearly defined role.
- Task decomposition: a broad study goal is divided into teaching, planning, quiz generation and evaluation.
- Context conditioning: prompts include topic, level and deadline.
- Output constraints: quiz agent is instructed to return a fixed JSON schema.
- Sequential orchestration: later steps use context and outputs from earlier steps.
- Evaluation and feedback: the evaluator compares student responses with the generated answer key.

## Notes and limitations
- The app requires a working Groq API key and internet connection.
- Model availability and rate limits depend on the provider. If the default model is unavailable, change the model name in the sidebar to a model currently listed in your Groq console.
- AI-generated study content can contain errors. Verify important academic facts against course material.
- This is a lightweight educational multi-agent implementation, not a fully autonomous agent framework. The orchestrator delegates to specialist agents in a controlled sequence.
