import re
import streamlit as st
from groq import Groq

# ------------------ PAGE CONFIG ------------------ #
st.set_page_config(page_title="Groq Thinking Chatbot", layout="wide")

# ------------------ SIDEBAR ------------------ #

with st.container():
    st.sidebar.write("🔗 github.com/0xZee - 2025")
    st.sidebar.caption("""
    🔑 GROQ API Key support via secrets.toml or sidebar input
    🧠 Thinking phase with real-time reasoning display
    📥 Expander auto-collapses when thinking is complete
    🔄 Clear Chat Session button in the sidebar
    🖱️ Websearch feature toggle
    💬 Maintains full chat history in session state
    """)
    st.sidebar.divider()

st.sidebar.write("🔐 Groq API Key")

# GROQ API Key handling
if "GROQ_API_KEY" in st.secrets and st.secrets["GROQ_API_KEY"]:
    st.sidebar.success("Using API key from secrets.toml ✅")
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
else:
    GROQ_API_KEY = st.sidebar.text_input("Enter your GROQ API Key", type="password")
    if GROQ_API_KEY:
        st.sidebar.info("Using API key from input")

# Websearch checkbox
use_websearch = st.sidebar.checkbox("Enable Websearch feature", value=False)

# ✅ Clear chat button
if st.sidebar.button("🌀 New Chat Session", use_container_width=True, type='primary'):
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a helpful assistant. Think step-by-step before answering."}
    ]
    st.sidebar.success("Chat session cleared!")

# ------------------ HELPERS ------------------ #
def format_reasoning_response(thinking_content: str) -> str:
    return (
        thinking_content.replace("<think>\n\n</think>", "")
        .replace("<think>", "")
        .replace("</think>", "")
    )

def display_message(message: dict):
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        if role == "assistant":
            display_assistant_message(message["content"])
        else:
            st.markdown(message["content"])

def display_assistant_message(content: str):
    pattern = r"<think>(.*?)</think>"
    think_match = re.search(pattern, content, re.DOTALL)
    if think_match:
        think_content = think_match.group(0)
        response_content = content.replace(think_content, "")
        think_content = format_reasoning_response(think_content)
        with st.expander("Thinking details", expanded=False):
            st.markdown(think_content)
        st.markdown(response_content)
    else:
        st.markdown(content)

def display_chat_history():
    for msg in st.session_state["messages"]:
        if msg["role"] != "system":
            display_message(msg)

# ------------------ STREAMING ------------------ #
def process_thinking_phase(stream):
    thinking_content = ""
    expander_placeholder = st.empty()
    with expander_placeholder.expander("Thinking...", expanded=True):
        think_box = st.empty()
        for chunk in stream:
            delta = chunk.choices[0].delta.content if chunk.choices[0].delta else ""
            if delta:
                thinking_content += delta
                think_box.markdown(format_reasoning_response(thinking_content))
                if "</think>" in delta:
                    break
    with expander_placeholder.expander("☑️ Thinking complete !", expanded=False):
        st.markdown(format_reasoning_response(thinking_content))
    return thinking_content

def process_response_phase(stream):
    response_placeholder = st.empty()
    response_content = ""
    for chunk in stream:
        delta = chunk.choices[0].delta.content if chunk.choices[0].delta else ""
        if delta:
            response_content += delta
            response_placeholder.markdown(response_content)
    return response_content

# ------------------ MODEL CALL ------------------ #
@st.cache_resource
def get_groq_client():
    return Groq(api_key=GROQ_API_KEY)

def stream_chat_completion(messages):
    client = get_groq_client()
    if use_websearch:
        # Websearch enabled - force tool and special call
        return client.chat.completions.create(
            messages=messages,
            model="openai/gpt-oss-20b",
            temperature=1,
            max_completion_tokens=2048,
            top_p=1,
            stream=True,
            stop=None,
            tool_choice="required",
            tools=[{"type": "browser_search"}],
        )
    else:
        # Regular assistant mode
        return client.chat.completions.create(
            messages=messages,
            model="openai/gpt-oss-20b",
            stream=True,
        )

# ------------------ CHAT HANDLER ------------------ #
def handle_user_input():
    if user_input := st.chat_input("Type your message here..."):
        st.session_state["messages"].append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            stream = stream_chat_completion(st.session_state["messages"])
            thinking_content = process_thinking_phase(stream)

            stream = stream_chat_completion(st.session_state["messages"])
            response_content = process_response_phase(stream)

            st.session_state["messages"].append(
                {"role": "assistant", "content": thinking_content + response_content}
            )

# ------------------ MAIN ------------------ #
def main():
    st.subheader("☰ Reasoning AI ☰ :orange[ChatGPT GPT-OSS]", divider='orange')
    display_chat_history()
    handle_user_input()

if __name__ == "__main__":
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "system", "content": "You are a helpful assistant. Think step-by-step before answering."}
        ]
    main()
