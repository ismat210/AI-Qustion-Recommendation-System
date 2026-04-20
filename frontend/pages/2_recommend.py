import streamlit as st
from utils.api_client import recommend

st.title("🤖 Question Recommendation")

query = st.text_input("Enter your question")

top_k = st.slider("Number of recommendations", 1, 10, 5)

if query:
    result = recommend(query, top_k)

    if "error" in result:
        st.error(result["error"])
    else:
        st.success("Recommendations:")

        for i, r in enumerate(result.get("results", []), 1):
            st.write(f"{i}. {r}")