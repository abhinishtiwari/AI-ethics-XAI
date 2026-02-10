
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

# Counter AI prompt
CHECKER_PROMPT = """
You are an ethics and quality checker AI.

Check the AI answer:
- Is it ethical?
- Is it safe?
- Is it helpful (not generic)?

If good, reply only: APPROVED
If bad, reply: REJECTED: <short reason>
"""

def main_ai(user_question, feedback=None):
    prompt = MAIN_AI_PROMPT

    if feedback:
        prompt += f"\nThe checker rejected your last answer because:\n{feedback}\nFix your answer.\n"

    prompt += f"\nUser Question:\n{user_question}"

    return llm.invoke(prompt).content


def counter_ai(ai_answer):
    prompt = CHECKER_PROMPT + f"\n\nAI Answer:\n{ai_answer}"
    return llm.invoke(prompt).content.strip()


def run_agent():
    print("\n🤖 Simple AI Agent with Counter AI (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        feedback = None
        attempt = 1

        while True:
            # print(f"\n🧠 Main AI Attempt {attempt}")
            ai_reply = main_ai(user_input, feedback)
            print("\nMain AI:", ai_reply)

            verdict = counter_ai(ai_reply)
            print("Checker AI:", verdict)

            if "APPROVED" in verdict:
                # print("\n✅ Final Answer Approved\n")
                break
            else:
                feedback = verdict
                attempt += 1
                print("🔁 Regenerating a better answer...\n")


if __name__ == "__main__":
    run_agent()