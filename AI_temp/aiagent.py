
from langchain_google_genai import ChatGoogleGenerativeAI

# Google API Key
GOOGLE_API_KEY = "AIzaSyAaG5QaOsAj8hY9FxgEXV97clulcWlZQ1A"

# Load Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    google_api_key=GOOGLE_API_KEY
)

# Main AI prompt (rules)
MAIN_AI_PROMPT = """
You are a helpful, safe and respectful AI.
Do not give harmful, illegal or unethical advice.
Give clear and non-generic answers.
"""

def main_ai(user_question):
    prompt = MAIN_AI_PROMPT + f"\n\nUser Question:\n{user_question}"
    return llm.invoke(prompt).content


def run_agent():
    print("\n🤖 Simple AI Agent (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        ai_reply = main_ai(user_input)
        print("\nAI:", ai_reply, "\n")


if __name__ == "__main__":
    run_agent()