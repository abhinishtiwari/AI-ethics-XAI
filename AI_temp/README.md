# 📘 Build a Gemini Chatbot with Counter-AI (LangChain)

This project demonstrates how to build a chatbot using **LangChain + Google Gemini**, with a **checker (Counter AI)** that validates safety, ethics, and usefulness before showing the final answer.

---

## 🧩 What You Will Build
A two-stage AI pipeline:
1. **Main AI** generates an answer.
2. **Checker AI** reviews the answer for **safe / ethical / helpful**.
3. If rejected → Main AI improves using feedback.
4. Loop until **APPROVED**.

---

## ✅ Prerequisites
- Python 3.9+
- Internet access
- Google account (for API key)

---

## 🧠 Understanding the Technology Stack

### 1️⃣ What is LangChain? (Simple Definition)

**LangChain** is a Python framework that helps you build AI-powered applications by connecting LLMs (like Gemini/GPT) with prompts, memory, tools, and workflows.

**In short:**
- **LLM** = the brain
- **LangChain** = the system that lets the brain talk to your app, tools, and data

---

### 2️⃣ How LangChain Works (Architecture)

LangChain sits between your code and the AI model.

#### 🧩 High-Level Diagram
```
Your App (Python)
      |
      v
  LangChain
   |   |   |
   |   |   +--> Memory (chat history, state)
   |   +------> Tools (APIs, files, DBs, search)
   +----------> LLM Connector (Gemini/GPT)
                     |
                     v
                  AI Model
```

#### Flow:
1. Your app sends a prompt to LangChain
2. LangChain formats messages
3. LangChain calls the LLM (Gemini/GPT)
4. Optional: LangChain calls tools
5. Result comes back to your app

---

### 3️⃣ What is langchain-google-genai (LangChain + Gemini)?

`langchain-google-genai` is a **connector package** that lets LangChain talk to Google Gemini models.

#### 🔌 Connector Diagram
```
Your Code
   |
   v
LangChain (ChatGoogleGenerativeAI)
   |
   v
Google Gemini API
```

#### What it gives you:
- `llm.invoke(prompt)` to call Gemini
- Standard message format
- Easy switching between models (e.g., `gemini-pro`, `gemini-2.0-flash`)

---

### 4️⃣ Why We Use LangChain (Practical Reasons)

#### Without LangChain:
- ❌ You manage raw API calls
- ❌ You manually format prompts
- ❌ Hard to add memory, tools, retries, pipelines

#### With LangChain:
- ✅ Easy model connection
- ✅ Easy prompt composition
- ✅ Easy multi-step pipelines (generate → review → fix)
- ✅ Easy memory (chat history)
- ✅ Easy tools (search, DB, files)

#### ✅ When to Use LangChain
- Chatbots
- AI agents
- Review pipelines (Main AI + Checker AI)
- Tool-using AI (search, DB, APIs)

#### ❌ When Not Needed
- Single one-off API call
- Very simple scripts

---

### 5️⃣ Core Building Blocks in LangChain

#### 🧱 Blocks

| Block | Description |
|-------|-------------|
| **LLM/Chat Model** | The AI brain (Gemini/GPT) |
| **Prompt** | Instructions to the model |
| **Chains** | Multi-step flows (A → B → C) |
| **Memory** | Store conversation/context |
| **Tools** | External actions (search, files, DB) |
| **Agents** | Decide which tool to use and when |

#### 🔄 How This Project Uses LangChain

In our Counter-AI chatbot:
- **LLM**: `ChatGoogleGenerativeAI` (Gemini 2.0 Flash)
- **Prompts**: `MAIN_AI_PROMPT` and `CHECKER_PROMPT`
- **Chain**: Main AI → Checker AI → (loop if rejected)
- **No Memory**: Each question is independent
- **No Tools**: Pure text-to-text processing

---

## 1️⃣ Install LangChain & Google Generative AI

Open terminal in your project folder and run:

```bash
pip install -U langchain langchain-google-genai
```

**Why?**
- `langchain`: framework to build AI workflows
- `langchain-google-genai`: Gemini connector

---

## 2️⃣ Generate Google AI API Key

1. Visit: https://aistudio.google.com/app/apikey
2. Create a new API key
3. Copy your API key

⚠️ **Security**: Never hardcode your API key in code or share it publicly. Use environment variables or `.env` files for production.

---

## 3️⃣ Connect Gemini Model in Python

```python
from langchain_google_genai import ChatGoogleGenerativeAI

# Google API Key
GOOGLE_API_KEY = "YOUR_API_KEY_HERE"

# Load Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    google_api_key=GOOGLE_API_KEY
)
```

**What this does**
- Creates a Gemini AI client with specified model
- `temperature=0.7` controls creativity (0=focused, 1=creative)
- Creates a callable AI client (`llm.invoke(prompt)`)

---

## 4️⃣ Add System Prompt (Safety Rules for Main AI)

```python
MAIN_AI_PROMPT = """
You are a helpful, safe and respectful AI.
Do not give harmful, illegal or unethical advice.
Give clear and non-generic answers.
"""
```

**Purpose**: Defines the AI behavior to be safe, ethical, and useful.

---

## 5️⃣ Create Function to Send User Question to Model

```python
def main_ai(user_question, feedback=None):
    prompt = MAIN_AI_PROMPT

    if feedback:
        prompt += f"\nThe checker rejected your last answer because:\n{feedback}\nFix your answer.\n"

    prompt += f"\nUser Question:\n{user_question}"

    return llm.invoke(prompt).content
```

**Logic**
- Always includes safety rules
- If checker rejected last output, includes feedback to improve
- Sends prompt to Gemini and returns response text

---

## 6️⃣ Create Checker (Counter AI) Prompt

```python
CHECKER_PROMPT = """
You are an ethics and quality checker AI.

Check the AI answer:
- Is it ethical?
- Is it safe?
- Is it helpful (not generic)?

If good, reply only: APPROVED
If bad, reply: REJECTED: <short reason>
"""
```

**Purpose**: Enforces a strict pass/fail decision based on safety and quality criteria.

---

## 7️⃣ Create Second Function to Review Chatbot Reply

```python
def counter_ai(ai_answer):
    prompt = CHECKER_PROMPT + f"\n\nAI Answer:\n{ai_answer}"
    return llm.invoke(prompt).content.strip()
```

**Logic**
- Feeds Main AI's output into the checker rules
- Returns `APPROVED` or `REJECTED: reason`

---

## 8️⃣ Take User Input → Generate → Validate → Loop

```python
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
```

**Flow**
- Reads user input in a loop
- Generates answer from Main AI
- Validates with Checker AI
- If rejected, retries with feedback
- Continues until approved
- Type 'exit' to quit

---

## 🚀 How to Run

1. Ensure you have installed the required packages:
```bash
pip install -U langchain langchain-google-genai
```

2. Add your Google API key to the code

3. Run the application:
```bash
python app.py
```

4. Start chatting with the AI!

---

## 9️⃣ Example Run

```
🤖 Simple AI Agent with Counter AI (type 'exit' to quit)

You: What is machine learning?

Main AI: Machine learning is a subset of artificial intelligence...

Checker AI: APPROVED

---

You: How to break into someone's account?

Main AI: I cannot provide assistance with illegal activities...

Checker AI: APPROVED
```

---

## 📁 Project Structure

```
AI_temp/
├── app.py              # Main application with Counter AI
├── aiagent.py          # Simplified version without Counter AI
└── README.md           # This file
```

---

## 🔐 Best Practices

### Security
- **Never commit API keys** to version control
- Use `.env` files with `python-dotenv` for production:
  ```python
  from dotenv import load_dotenv
  import os
  
  load_dotenv()
  GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
  ```
- Add `.env` to your `.gitignore` file

### Code Quality
- Add retry limits to prevent infinite loops
- Log approvals/rejections for auditing
- Use different prompts for Main AI and Checker AI
- Handle API errors gracefully

### Performance
- Consider caching approved responses
- Monitor API usage and costs
- Implement rate limiting if needed

---

## 🧠 Summary
- You built a **self-correcting AI pipeline**
- One AI generates, another validates
- Feedback loop enforces safety and quality
- This pattern is used in production AI systems for content moderation

---

## 🛠️ Optional Extensions

### Easy
- Add conversation history to maintain context
- Save approved answers to CSV for analysis
- Add timestamps to responses

### Medium
- Implement confidence scoring
- Add multiple checker criteria (grammar, facts, tone)
- Create a simple Flask/Streamlit web interface
- Add logging with different levels (INFO, WARNING, ERROR)

### Advanced
- Integrate fact-checking API in checker
- Add semantic similarity checking
- Implement A/B testing between different prompts
- Build a dashboard to visualize approval rates
- Add user feedback collection
- Implement RAG (Retrieval Augmented Generation) for domain-specific knowledge

---

## 🐛 Troubleshooting

### API Key Errors
- Ensure your API key is valid and active
- Check if you've enabled the Generative AI API in Google Cloud Console

### Import Errors
- Verify all packages are installed: `pip list | grep langchain`
- Try reinstalling: `pip install --force-reinstall langchain-google-genai`

### Rate Limiting
- Google AI has rate limits on free tier
- Add delays between requests if needed
- Consider upgrading to paid tier for production use

---

## 📚 Resources
- [LangChain Documentation](https://python.langchain.com/)
- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API Documentation](https://ai.google.dev/docs)

---

## 📝 License
This project is for educational purposes. Modify and use as needed.

---

## 🤝 Contributing
Feel free to fork this project and add your own improvements!

Suggested areas:
- Better prompt engineering
- Additional safety checks
- Multi-language support
- Voice integration
