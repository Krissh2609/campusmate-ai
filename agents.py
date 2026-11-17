import json
import re
from openai import OpenAI
from prompts import TUTOR_PROMPT, PLANNER_PROMPT, QUIZ_PROMPT, EVALUATOR_PROMPT

class CampusMateAgents:
    """Specialist LLM agents coordinated by a lightweight orchestrator."""

    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        self.model = model

    def _ask(self, system_prompt: str, user_prompt: str, temperature: float = 0.4) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()

    def tutor(self, topic: str, level: str) -> str:
        return self._ask(TUTOR_PROMPT, f"Teach this topic: {topic}\nStudent level: {level}")

    def planner(self, topic: str, deadline: str, level: str) -> str:
        return self._ask(
            PLANNER_PROMPT,
            f"Topic: {topic}\nDeadline: {deadline}\nStudent level: {level}"
        )

    def quiz(self, topic: str, level: str) -> dict:
        raw = self._ask(
            QUIZ_PROMPT,
            f"Create 5 multiple-choice questions about: {topic}\nStudent level: {level}\nReturn valid JSON only.",
            temperature=0.2
        )
        try:
            data = self._extract_json(raw)
        except ValueError:
            repaired = self._ask(
                "You are a JSON formatter. Return ONLY valid JSON with a top-level questions array. "
                "Each question must contain question, options (four strings), answer, and explanation. "
                "No Markdown fences or commentary.",
                f"Repair this quiz into the required JSON structure, preserving its meaning:\\n{raw}",
                temperature=0.0
            )
            data = self._extract_json(repaired)
        questions = data.get("questions", [])
        clean = []
        for q in questions[:5]:
            if not isinstance(q, dict):
                continue
            options = q.get("options", [])
            if isinstance(options, list) and len(options) >= 2:
                clean.append({
                    "question": str(q.get("question", "")),
                    "options": [str(x) for x in options],
                    "answer": str(q.get("answer", "")),
                    "explanation": str(q.get("explanation", ""))
                })
        data["questions"] = clean
        data["markdown"] = self._quiz_markdown(clean)
        return data

    def evaluate(self, quiz: dict, answers: dict, topic: str) -> str:
        compact = []
        for i, q in enumerate(quiz.get("questions", [])):
            compact.append({
                "question": q.get("question"),
                "options": q.get("options"),
                "correct_answer": q.get("answer"),
                "explanation": q.get("explanation"),
                "student_answer": answers.get(str(i))
            })
        return self._ask(
            EVALUATOR_PROMPT,
            f"Topic: {topic}\nEvaluate these responses:\n{json.dumps(compact, ensure_ascii=False)}",
            temperature=0.2
        )

    @staticmethod
    def _extract_json(raw: str) -> dict:
        cleaned = raw.strip()
        cleaned = re.sub(r"^```(?:json)?\\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\\s*```$", "", cleaned)
        try:
            data = json.loads(cleaned)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start < 0 or end <= start:
            raise ValueError("Quiz response was not valid JSON. Please try generating the quiz again.")
        try:
            data = json.loads(cleaned[start:end + 1])
        except json.JSONDecodeError as exc:
            raise ValueError("Quiz response was not valid JSON. Please try generating the quiz again.") from exc
        if not isinstance(data, dict):
            raise ValueError("Quiz response must be a JSON object.")
        return data

    @staticmethod
    def _quiz_markdown(questions: list) -> str:
        if not questions:
            return "The quiz could not be formatted. Please generate it again."
        lines = []
        for i, q in enumerate(questions, 1):
            lines.append(f"**Q{i}. {q['question']}**")
            lines.extend([f"- {opt}" for opt in q["options"]])
            lines.append("")
        return "\n".join(lines)
