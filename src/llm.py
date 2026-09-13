import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# ==========================================
# ENVIRONMENT / API KEY
# ==========================================

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise RuntimeError(
        "GOOGLE_API_KEY is not set. Add it to your .env file "
        "(locally) or to Streamlit Secrets (when deployed on "
        "Streamlit Cloud) before starting the app."
    )

# ==========================================
# MODEL
# ==========================================
# NOTE: "gemini-3.1-flash-lite" (the old default) is not a valid
# model name and was causing every explanation call to fail.
# "gemini-2.5-flash" is a real, current, fast/cheap model.

llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    google_api_key=GOOGLE_API_KEY,
    temperature=0.3
)


# ==========================================
# GENERATE EXPLANATION
# ==========================================
# IMPORTANT: this function's signature must match exactly how
# app.py calls it:
#
#     explanation = generate_explanation(user, program)
#
# `user`    -> the dict built in app.py from the form inputs
# `program` -> one program dict returned inside a match from
#              find_matching_programs() in src/eligibility.py
#              (keys: program_name, category, organization,
#              province, description, documents,
#              application_steps, official_url, etc.)

def generate_explanation(user, program):
    """
    Build a short, grounded AI explanation of why `program`
    may be relevant to `user`, using only fields already
    produced by eligibility.py. No RAG / ChromaDB needed.
    """

    prompt = f"""
You are HaqDarmand AI, a decision-support assistant that helps
people in Pakistan understand scholarships, financial assistance,
and health-support programs.

Explain in 3-5 short sentences why the program below may be
relevant to this user, based ONLY on the information given.

RULES:
1. Do not invent eligibility rules, documents, or benefits that
   are not present in the information below.
2. Never state a final/official eligibility decision - use
   "potentially eligible" or "may be eligible".
3. Mention 1-2 concrete reasons (age, province, education, income,
   student status) drawn from the data below.
4. Remind the user to confirm details on the official source.
5. Keep the tone simple, friendly, and easy to understand.
6. If the user's question context is in Urdu, you may still
   respond in English unless asked otherwise - app.py currently
   only calls this function for the explanation panel, not chat.

USER INFORMATION
-----------------
Age: {user.get("age")}
Province: {user.get("province")}
Education: {user.get("education")}
Student status: {user.get("student_status")}
Monthly household income (PKR): {user.get("income")}
Family size: {user.get("family_size")}

PROGRAM INFORMATION
--------------------
Name: {program.get("program_name")}
Category: {program.get("category")}
Organization: {program.get("organization")}
Province: {program.get("province")}
Description: {program.get("description")}
Required documents: {program.get("documents")}
Application steps: {program.get("application_steps")}
"""

    try:
        response = llm.invoke(prompt)
    except Exception as error:
        print(f"[LLM ERROR] Gemini call failed: {error}")
        raise RuntimeError("Gemini call failed") from error

    content = response.content

    # Gemini/LangChain sometimes returns a plain string...
    if isinstance(content, str):
        return content

    # ...and sometimes a list of content blocks.
    if isinstance(content, list):
        text_parts = []

        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text = item.get("text", "")
                if text:
                    text_parts.append(text)

        if text_parts:
            return "\n".join(text_parts)

    return str(content)
