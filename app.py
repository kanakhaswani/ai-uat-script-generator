from anthropic import Anthropic
from dotenv import load_dotenv
import os
import streamlit as st
import pdfplumber

# Load environment variables
load_dotenv()

# Create Claude client
client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# Streamlit page settings
st.set_page_config(page_title="AI UAT Script Generator")

st.title("AI UAT Script Generator")
st.write("Upload a Business Requirements Document (BRD) to generate UAT test cases.")

# File uploader
uploaded_file = st.file_uploader(
    "Choose a BRD file",
    type=["pdf"]
)

# Process uploaded file
if uploaded_file:

    text = ""

    # Read PDF
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    st.success("BRD uploaded successfully!")

    st.subheader("Extracted Text")
    st.text_area(
        "Document Contents",
        text,
        height=300
    )

    # Ask Claude to summarize
    with st.spinner("Claude is reading your BRD..."):

        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": f"""
You are a Business Analyst.

Read the following Business Requirements Document.

Summarize it into 5 concise bullet points.

{text}
"""
                }
            ]
        )

    st.subheader("Claude Summary")
    st.write(response.content[0].text)
