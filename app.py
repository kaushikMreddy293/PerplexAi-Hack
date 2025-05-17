import streamlit as st
from perplexity_Client import get_perplexity_response

st.set_page_config(page_title="Ask Perplexity", layout="centered")

st.title("🤖 Ask Perplexity AI")

user_query = st.text_input("Enter your question")

if st.button("Ask") and user_query.strip() != "":
    with st.spinner("Thinking..."):
        result = get_perplexity_response(user_query)
        st.markdown("### 📋 Response:")
        st.write(result["response"])

        citations = result.get("citations", [])
        if citations:
            st.markdown("### 🔗 References:")
            for i, link in enumerate(citations, 1):
                st.markdown(f"[{i}]({link})")
