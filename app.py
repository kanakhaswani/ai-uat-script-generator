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
st.write("Upload a PDF document and Claude will summarize it.")

# Upload PDF
uploaded_file = st.file_uploader(
    "Choose a PDF",
    type=["pdf"]
)

if uploaded_file:

    st.success("✅ File uploaded!")

    text = ""

    # Read PDF
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    st.subheader("Extracted Text")

    st.text_area(
        "Document Contents",
        text,
        height=300
    )

    st.write("🤖 Calling Claude...")

    try:

        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": f"""
Summarize the following document into 5 bullet points.

{text}
"""
                }
            ]
        )

        st.success("✅ Claude responded!")

        st.subheader("Claude Summary")

        st.write(response.content[0].text)

    except Exception as e:

        st.error("Claude returned an error.")

        st.exception(e)
