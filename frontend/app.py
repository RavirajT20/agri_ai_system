import streamlit as st
import requests

BACKEND_URL = "http://backend:8000"

st.title("🌾 Agri AI System")

# ---- BUTTONS ----
mode = st.radio("Select Mode", ["Education Bot", "Triage Agent"])

# =========================
# 🎓 EDUCATION BOT UI
# =========================
if mode == "Education Bot":
    st.header("🌱 Agriculture Learning Bot")

    # Generate Question
    if "question_data" not in st.session_state:
        if st.button("Generate Question"):
            res = requests.get(f"{BACKEND_URL}/education/question")
            st.session_state.question_data = res.json()

    # Display Question
    if "question_data" in st.session_state:
        q = st.session_state.question_data

        st.subheader(f"📌 Topic: {q['topic']}")
        st.write(f"❓ {q['question']}")

        user_answer = st.text_area("Your Answer")

        # Submit Answer
        if st.button("Submit Answer"):
            res = requests.post(
                f"{BACKEND_URL}/education/evaluate",
                json={
                    "topic": q["topic"],
                    "fact": q["fact"],
                    "user_answer": user_answer
                }
            )

            result = res.json()

            # ✅ Structured Output UI
            st.subheader("📊 Result")

            st.metric("Score", f"{result['score']} / 10")

            # Optional feedback color
            if result["score"] >= 7:
                st.success("Good job! 👍")
            else:
                st.error("Needs improvement ⚠️")

            st.write(f"✅ Correct Answer: {result['correct_answer']}")
            st.write(f"🧠 Explanation: {result['explanation']}")
            st.write(f"📈 Improvement: {result['improvement']}")

            

# =========================
# 🚨 TRIAGE AGENT UI
# =========================
elif mode == "Triage Agent":
    st.header("🚨 Message Triage System")

    message = st.text_area("Enter Message")

    if st.button("Analyze"):
        res = requests.post(
            f"{BACKEND_URL}/triage/triage",
            json={"message": message}
        )

        result = res.json()

        # =========================
        # 📊 CLEAN CLASSIFICATION
        # =========================
        st.subheader("📊 Classification")

        raw_text = result.get("classification", "").lower()

        # Clean extraction
        intent = "Informational"
        urgency = "Low"

        if "high" in raw_text:
            urgency = "High"
        elif "medium" in raw_text:
            urgency = "Medium"

        if "complaint" in raw_text or "issue" in raw_text:
            intent = "Issue"
        elif "advice" in raw_text:
            intent = "Advisory"

        col1, col2 = st.columns(2)
        col1.metric("Intent", intent)
        col2.metric("Urgency", urgency)

        st.subheader("✉️ Suggested Actions")

        draft = result.get("draft_response", "")

        import re

        # Remove email-style text (Dear, Regards, etc.)
        draft = re.sub(r"Dear.*?,", "", draft, flags=re.DOTALL)
        draft = re.sub(r"Best regards.*", "", draft, flags=re.DOTALL)

        # Remove markdown (** etc.)
        draft = re.sub(r"\*\*", "", draft)

        # Extract bullet/numbered points
        points = re.findall(r"\d+\.\s+(.*)", draft)

        # If no numbered points found → split by lines
        if not points:
            points = [line.strip() for line in draft.split("\n") if len(line.strip()) > 20]

        # Display clean bullet points
        for p in points:
            st.write(f"• {p}")
            # =========================
        # 🚦 PRIORITY INDICATOR
        # =========================
        if urgency == "High":
            st.error("🚨 High Priority")
        elif urgency == "Medium":
            st.warning("⚠️ Medium Priority")
        else:
            st.success("✅ Low Priority")