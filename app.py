import streamlit as st
from perplexity_Client import get_perplexity_response
from db import (
    save_message, get_chat_history, start_new_chat,
    get_all_chats, update_chat_title
)

st.set_page_config(page_title="Chat with Perplexity", layout="centered")
st.title("💬 Chat with Perplexity AI")

# Show all chat sessions in sidebar
st.sidebar.title("📂 Chat History")

all_chats = get_all_chats()
chat_titles = {chat["title"]: chat["chat_id"] for chat in all_chats}

# Select chat session safely
selected_title = None
selected_chat_id = None

if chat_titles:
    selected_title = st.sidebar.selectbox("Select a chat", options=list(chat_titles.keys()))
    selected_chat_id = chat_titles.get(selected_title)

    # If the selected chat is not the current one, load it
    if selected_chat_id and selected_chat_id != st.session_state.get("chat_id"):
        st.session_state.chat_id = selected_chat_id
        st.session_state.messages = get_chat_history(selected_chat_id)
        st.experimental_rerun()

    # Rename current chat
    if selected_chat_id == st.session_state.get("chat_id"):
        new_title = st.sidebar.text_input("Rename this chat:", value=selected_title)
        if new_title != selected_title:
            update_chat_title(st.session_state.chat_id, new_title)
            st.experimental_rerun()
else:
    st.sidebar.info("No chats yet. Start a new one by sending a message.")

# If no chat started yet, create one
if "chat_id" not in st.session_state:
    st.session_state.chat_id = start_new_chat()

# Load messages for current chat_id if not loaded yet
if "messages" not in st.session_state:
    st.session_state.messages = get_chat_history(st.session_state.chat_id)

# Display all messages in current chat
for msg in st.session_state.messages:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("citations"):
            st.markdown("🔗 **References:**")
            for i, link in enumerate(msg["citations"], 1):
                link = link.strip()
                if link.startswith("http"):
                    st.markdown(f"{i}. <a href='{link}' target='_blank'>{link}</a>", unsafe_allow_html=True)
                else:
                    st.markdown(f"{i}. {link}")

# Chat input field
if prompt := st.chat_input("Ask something..."):
    # Save user message
    user_msg = {"role": "user", "content": prompt}
    st.session_state.messages.append(user_msg)
    save_message(role="user", content=prompt, chat_id=st.session_state.chat_id)

    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response
    with st.spinner("Thinking..."):
        result = get_perplexity_response(prompt)
        reply = result["response"]
        citations = result["citations"]

    assistant_msg = {
        "role": "assistant",
        "content": reply,
        "citations": citations
    }

    st.session_state.messages.append(assistant_msg)
    save_message(role="assistant", content=reply, citations=citations, chat_id=st.session_state.chat_id)

    with st.chat_message("assistant"):
        st.markdown(reply)
        if citations:
            st.markdown("🔗 **References:**")
            for i, link in enumerate(citations, 1):
                link = link.strip()
                if link.startswith("http"):
                    st.markdown(f"{i}. <a href='{link}' target='_blank'>{link}</a>", unsafe_allow_html=True)
                else:
                    st.markdown(f"{i}. {link}")
