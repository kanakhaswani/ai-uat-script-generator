import streamlit as st

st.set_page_config(page_title="AI UAT Script Generator")

st.title("AI UAT Script Generator")

st.write("Upload a Business Requirements Document (BRD) to generate UAT test cases.")

uploaded_file = st.file_uploader(
    "Choose a BRD file",
    type=["pdf", "docx"]
)

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")
