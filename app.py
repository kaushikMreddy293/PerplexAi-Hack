import streamlit as st
from perplexity_Client import get_perplexity_response
from db import save_message, get_chat_history

st.set_page_config(page_title="Chat with Perplexity", layout="centered")
st.title("💬 Chat with Perplexity AI")

# Load chat history from MongoDB into session
if "messages" not in st.session_state:
    st.session_state.messages = get_chat_history()  # List of {"role", "content", "citations"}

# Display past messages
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

# Chat input
if prompt := st.chat_input("Ask something..."):
    # Store and show user message
    user_msg = {"role": "user", "content": prompt}
    st.session_state.messages.append(user_msg)
    save_message(role="user", content=prompt)

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
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
    save_message(role="assistant", content=reply, citations=citations)

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
