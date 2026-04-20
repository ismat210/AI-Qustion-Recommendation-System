import streamlit as st
from utils.api_client import upload_file

st.title("📤 Upload File")

file = st.file_uploader("Upload PDF / DOCX / Image")

if file:
    result = upload_file(file)

    if "error" in result:
        st.error(result["error"])
    else:
        st.success("File processed successfully 🚀")

        st.json({
            "file": result.get("file"),
            "questions_extracted": result.get("questions_extracted")
        })