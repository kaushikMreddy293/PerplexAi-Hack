import streamlit as st
from perplexity_Client import get_perplexity_response

st.set_page_config(page_title="Chat with Perplexity", layout="centered")
st.title("💬 Chat with Perplexity AI")

if "messages" not in st.session_state:
    st.session_state.messages = []  # list of {"role", "content", "citations"}

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

# New user input
if prompt := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        result = get_perplexity_response(prompt)
        reply = result["response"]
        citations = result["citations"]

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply,
        "citations": citations
    })

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
