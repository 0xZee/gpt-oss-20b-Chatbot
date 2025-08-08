# gpt-oss-20b-Chatbot
Streamlit : Chatbot App / LLM : gpt-oss-20b (via Groq API)

# 🤖 Groq Thinking Chatbot (Streamlit) - ChatGPT `gpt-oss-20`

An interactive chatbot powered by **Groq's GPT OSS / DeepSeek reasoning models**, built with Streamlit.  
This app demonstrates *thinking step-by-step before answering*, showing the model's reasoning process inside a collapsible **"Thinking..."** expander that automatically closes once the answer is ready.

---

## ✨ Features
- 🔑 **GROQ API Key support** via `secrets.toml` or sidebar input  
- 🧠 **Thinking phase** with real-time reasoning display  
- 📥 Expander auto-collapses when thinking is complete  
- 🔄 **Clear Chat Session** button in the sidebar  
- 🖱️ Choose between **`openai/gpt-oss-20b`** and **`deepseek-r1-distill-llama-70b`**  
- 💬 Maintains full chat history in session state  

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/groq-thinking-chatbot.git
   cd groq-thinking-chatbot
   ```
   
Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
Install dependencies
```

```bash
pip install -r requirements.txt
Add your Groq API Key
Create .streamlit/secrets.toml:

GROQ_API_KEY = "your_api_key_here"
```

🚀 Running the App
```bash
streamlit run chatbot_thinking.py
```

Then open your browser at http://localhost:8501.

🛠 Usage
Set your API key

If stored in secrets.toml, it’s automatically used.

Otherwise, enter it in the sidebar.

Select your model

"openai/gpt-oss-20b" (default)

"deepseek-r1-distill-llama-70b"

Start chatting

Type your question in the input box.

Watch the model “think” step-by-step.

The reasoning expander collapses when complete.

Clear chat

Use the "Clear Chat Session" button in the sidebar.

📂 Project Structure
graphql
Copy
Edit
.
├── chatbot_thinking.py    # Main Streamlit app
├── requirements.txt       # Python dependencies
└── .streamlit/
    └── secrets.toml        # API key storage (optional)

📌 Requirements
Python 3.9+

Streamlit

groq-python SDK

Install all dependencies:

```bash

pip install -r requirements.txt
```

📜 License
MIT License — feel free to use, modify, and share.

💡 Pro Tip:
If you want to deploy this app publicly, remember to set your GROQ_API_KEY securely via your deployment platform's environment secrets.
