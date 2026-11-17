# CampusMate: A Multi-Agent Academic Assistant

## 1. Abstract
CampusMate is a multi-agent AI academic assistant designed to support students in learning and exam preparation. It uses a central orchestrator to coordinate four specialist agents: Tutor, Study Planner, Quiz Generator and Evaluator. Each agent is powered by a large language model and guided by a role-specific system prompt. The application is developed using Python and Streamlit, with the Groq API providing LLM access.

## 2. Problem Statement
Students often use separate tools to understand concepts, prepare revision schedules, practice questions and assess their understanding. Switching between these tasks can make preparation less organized. CampusMate brings these activities into one interface and coordinates them through a multi-agent workflow.

## 3. Objectives
- Explain academic concepts at different learning levels.
- Generate practical study plans based on a deadline.
- Create topic-specific multiple-choice questions.
- Evaluate student responses and provide targeted feedback.
- Demonstrate role prompting, task decomposition, structured output and agent orchestration.

## 4. Proposed System
The user enters a topic and selects a workflow. The Orchestrator routes the request to one or more specialist agents. The Tutor produces an explanation, the Planner creates a schedule, and the Quiz Generator creates MCQs with an answer key. After the student submits answers, the Evaluator compares them with the answer key and returns a score and recommendations.

## 5. Agent Roles
| Agent | Responsibility | Prompt strategy |
|---|---|---|
| Orchestrator | Coordinates specialist agents and workflow order | Task routing and sequencing |
| Tutor | Explains concepts | Role prompting and structured explanation |
| Planner | Builds revision schedule | Context conditioning and constraint-based output |
| Quiz Generator | Creates MCQs | Strict JSON output schema |
| Evaluator | Scores answers and identifies gaps | Rubric/answer-key-based evaluation |

## 6. Technology Stack
- Python
- Streamlit
- OpenAI Python SDK configured for the Groq-compatible API
- Groq-hosted language model

## 7. Prompt Engineering Methodology
Each specialist receives a distinct system prompt that specifies its identity, objective, response structure and constraints. User context such as topic, learning level and deadline is passed as a separate user message. The Quiz Generator is instructed to return valid JSON so the application can parse questions and answer keys reliably. The Evaluator receives the generated answer key and submitted answers to produce targeted feedback.

## 8. Workflow
1. User enters topic, level and optional deadline.
2. Orchestrator identifies the selected workflow.
3. Orchestrator calls the relevant specialist agent(s).
4. The application displays the generated learning material.
5. Student submits quiz answers.
6. Evaluator checks answers and returns performance feedback.

## 9. Expected Results
CampusMate should provide a topic explanation, a structured revision plan, a five-question MCQ quiz and personalized evaluation feedback. The exact output varies with the selected topic and language model response.

## 10. Advantages
- Multiple specialized roles instead of one generic prompt.
- Clear separation of responsibilities.
- Reusable prompts that can be tuned independently.
- Structured quiz output that can be consumed by application code.
- Simple interface accessible through a web browser.

## 11. Limitations and Future Scope
The current prototype depends on an internet connection and an external LLM API. It does not yet retrieve content from a student's lecture notes or verify facts against a trusted academic knowledge base. Future improvements could include PDF/notes upload, course-specific retrieval augmented generation (RAG), progress tracking, adaptive difficulty and support for additional model providers.

## 12. Conclusion
CampusMate demonstrates how prompt engineering and multi-agent task decomposition can be combined to build a practical academic assistant. By assigning teaching, planning, quiz creation and evaluation to specialist agents, the system produces a more organized study workflow and showcases core concepts of multi-agent AI systems.

## 13. Demonstration Evidence
Add screenshots of:
1. CampusMate home page and agent overview.
2. Tutor Agent explanation.
3. Planner Agent schedule.
4. Quiz Generator questions.
5. Evaluator Agent feedback after quiz submission.

## 14. Test Case
**Input:** Topic = Named Entity Recognition in NLP; Level = Intermediate; Deadline = in 3 days.

**Expected output:** A clear explanation of NER, a three-day revision plan, five MCQs and a score with feedback after answers are submitted.
