import os
import streamlit as st
from dotenv import load_dotenv
from agents import CampusMateAgents

load_dotenv()
st.set_page_config(page_title="CampusMate | AI Study Assistant", page_icon="🎓", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 2rem; max-width: 1150px;}
.hero {padding: 1.4rem 1.6rem; border-radius: 18px; background: linear-gradient(120deg,#10243b,#1d4e70); color: white; margin-bottom: 1.2rem;}
.hero h1 {font-size: 2.2rem; margin: 0 0 .35rem 0;}
.hero p {color: #d7e8f5; margin: 0;}
.agent-card {padding: 1rem; border: 1px solid rgba(128,128,128,.25); border-radius: 14px; min-height: 112px;}
.small-muted {color: #8995a3; font-size: .9rem;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>🎓 CampusMate</h1>
  <p>Your multi-agent academic assistant — learn concepts, plan revision, practice questions, and improve through feedback.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Configuration")
    default_api_key = os.getenv("GROQ_API_KEY", "")
    try:
        default_api_key = default_api_key or st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        pass
    api_key = st.text_input("Groq API key", value=default_api_key, type="password", help="Get a free Groq API key from console.groq.com")
    model = st.text_input("Model", value="openai/gpt-oss-20b")
    st.caption("Your API key is used only for requests from this app and is not saved.")
    st.divider()
    st.markdown("**Agent team**")
    st.markdown("- 🧭 Orchestrator")
    st.markdown("- 📘 Tutor Agent")
    st.markdown("- 🗓️ Planner Agent")
    st.markdown("- 📝 Quiz Generator")
    st.markdown("- 🎯 Evaluator Agent")

st.subheader("Meet your agents")
cols = st.columns(4)
cards = [
    ("📘 Tutor", "Explains difficult topics in simple, structured language."),
    ("🗓️ Planner", "Turns your deadline and available time into a revision plan."),
    ("📝 Quiz Generator", "Creates MCQs to test understanding."),
    ("🎯 Evaluator", "Checks answers and recommends what to revise next.")
]
for col, (title, desc) in zip(cols, cards):
    with col:
        st.markdown(f'<div class="agent-card"><b>{title}</b><p class="small-muted">{desc}</p></div>', unsafe_allow_html=True)

st.divider()
mode = st.radio(
    "Choose a workflow",
    ["Complete Study Pack", "Explain a Topic", "Create a Study Plan", "Generate a Quiz"],
    horizontal=True
)
topic = st.text_input("What topic do you want to study?", placeholder="e.g., Named Entity Recognition in NLP")
context_col1, context_col2 = st.columns(2)
with context_col1:
    level = st.selectbox("Your level", ["Beginner", "Intermediate", "Advanced"])
with context_col2:
    deadline = st.text_input("Exam / deadline (optional)", placeholder="e.g., in 3 days")

if "study_pack" not in st.session_state:
    st.session_state.study_pack = None
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""

run = st.button("🚀 Run CampusMate", type="primary", use_container_width=True)

if run:
    if not api_key:
        st.error("Add your Groq API key in the sidebar first.")
    elif not topic.strip():
        st.warning("Enter a topic to get started.")
    else:
        try:
            agents = CampusMateAgents(api_key=api_key, model=model.strip() or "llama-3.3-70b-versatile")
            st.session_state.last_topic = topic.strip()
            st.session_state.quiz_data = None
            if mode == "Complete Study Pack":
                with st.spinner("Orchestrator is coordinating the agent team..."):
                    st.info("Step 1/3 · Tutor Agent is preparing your explanation.")
                    explanation = agents.tutor(topic, level)
                    st.info("Step 2/3 · Planner Agent is building your revision plan.")
                    plan = agents.planner(topic, deadline or "Not specified", level)
                    st.info("Step 3/3 · Quiz Generator is creating practice questions.")
                    quiz = agents.quiz(topic, level)
                st.session_state.study_pack = {"topic": topic, "explanation": explanation, "plan": plan, "quiz": quiz}
                st.session_state.quiz_data = quiz
            elif mode == "Explain a Topic":
                with st.spinner("Tutor Agent is thinking..."):
                    st.session_state.study_pack = {"topic": topic, "explanation": agents.tutor(topic, level)}
            elif mode == "Create a Study Plan":
                with st.spinner("Planner Agent is building your plan..."):
                    st.session_state.study_pack = {"topic": topic, "plan": agents.planner(topic, deadline or "Not specified", level)}
            else:
                with st.spinner("Quiz Generator is creating your quiz..."):
                    quiz = agents.quiz(topic, level)
                    st.session_state.study_pack = {"topic": topic, "quiz": quiz}
                    st.session_state.quiz_data = quiz
            st.success("Your agents have completed the task.")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.caption("Check your API key, internet connection, and model name.")

pack = st.session_state.study_pack
if pack:
    st.divider()
    st.header(f"📚 Your CampusMate results: {pack['topic']}")
    if "explanation" in pack:
        with st.expander("📘 Tutor Agent — Concept explanation", expanded=True):
            st.markdown(pack["explanation"])
    if "plan" in pack:
        with st.expander("🗓️ Planner Agent — Study plan", expanded=True):
            st.markdown(pack["plan"])
    if "quiz" in pack:
        with st.expander("📝 Quiz Generator — Practice quiz", expanded=True):
            quiz = pack["quiz"]
            st.markdown(quiz.get("markdown", "Quiz generated, but could not format the questions."))
            if quiz.get("questions"):
                st.session_state.quiz_data = quiz

quiz_data = st.session_state.quiz_data
if quiz_data and quiz_data.get("questions"):
    st.divider()
    st.header("🎯 Test yourself")
    st.write("Select one answer for each question, then ask the Evaluator Agent to assess your responses.")
    with st.form("quiz_form"):
        answers = {}
        for i, q in enumerate(quiz_data["questions"]):
            st.markdown(f"**Q{i+1}. {q.get('question','')}**")
            opts = q.get("options", [])
            answers[str(i)] = st.radio("Choose an answer", opts, key=f"answer_{i}", index=None, label_visibility="collapsed")
        submitted = st.form_submit_button("Submit answers for evaluation", type="primary")
    if submitted:
        if any(v is None for v in answers.values()):
            st.warning("Please answer every question before submitting.")
        else:
            try:
                agents = CampusMateAgents(api_key=api_key, model=model.strip() or "llama-3.3-70b-versatile")
                with st.spinner("Evaluator Agent is reviewing your answers..."):
                    evaluation = agents.evaluate(quiz_data, answers, st.session_state.last_topic)
                st.subheader("Evaluator Agent feedback")
                st.markdown(evaluation)
            except Exception as e:
                st.error(f"Evaluation failed: {e}")

st.divider()
with st.expander("ℹ️ How this multi-agent system works"):
    st.markdown("""
    1. **Orchestrator:** Receives the user's request and routes it to the appropriate specialist(s).
    2. **Tutor Agent:** Uses a teaching-focused prompt to explain the topic.
    3. **Planner Agent:** Uses the topic, level, and deadline to create a practical plan.
    4. **Quiz Generator:** Creates MCQs with answer keys and explanations.
    5. **Evaluator Agent:** Compares submitted answers with the answer key and gives targeted feedback.

    Each specialist is a separate LLM call with its own role-specific system prompt. The agents share the same topic and workflow context, while the orchestrator controls the sequence.
    """)
st.caption("CampusMate · Prompt Engineering mini-project · Built with Python, Streamlit and Groq")
