from langchain_groq import ChatGroq

from app.config import GROQ_API_KEY


if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing from the .env file.")


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=GROQ_API_KEY,
    temperature=0.2,
    max_tokens=1200,
)

# from langchain_google_genai import ChatGoogleGenerativeAI

# from app.config import GEMINI_API_KEY


# if not GEMINI_API_KEY:
#     raise ValueError("GEMINI_API_KEY is missing from the .env file.")


# llm = ChatGoogleGenerativeAI(
#     model="gemini-3.8-flash",
#     google_api_key=GEMINI_API_KEY,
#     temperature=0.2,
#     max_tokens=300,
# )