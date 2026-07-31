from anthropic import Anthropic
from dotenv import load_dotenv
import os
load_dotenv()

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)
import streamlit as st
import pdfplumber

st.set_page_config(page_title="AI UAT Script Generator")

st.title("AI UAT Script Generator")

uploaded_file = st.file_uploader(
    "Upload your BRD",
    type=["pdf"]
)

if uploaded_file:
    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text

    st.success("BRD uploaded successfully!")

    st.subheader("Extracted Text")

    st.text_area(
        "",
        text,
        height=400
    )
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=500,
    messages=[
        {
            "role": "user",
            "content": f"""
Read this Business Requirements Document and summarize it in 5 bullet points.

{text}
"""
        }
    ]
)

st.subheader("Claude Summary")
st.write(response.content[0].text)
