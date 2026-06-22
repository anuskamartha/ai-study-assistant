import streamlit as st
from google import genai
from pypdf import PdfReader
from PIL import Image

# Replace this with your actual Gemini API key
API_KEY = "PASTE_YOUR_API_KEY_HERE"

client = genai.Client(api_key=API_KEY)

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI Study Assistant")
st.write("Upload PDFs, images, or ask questions.")

uploaded_pdf = st.file_uploader(
    "📄 Upload a PDF",
    type=["pdf"]
)

uploaded_image = st.file_uploader(
    "🖼️ Upload an image",
    type=["png", "jpg", "jpeg"]
)

question = st.text_input(
    "❓ Ask a question"
)

pdf_text = ""
image = None

if uploaded_pdf is not None:
    try:
        reader = PdfReader(uploaded_pdf)

        for page in reader.pages:
            text = page.extract_text()
            if text:
                pdf_text += text + "\n"

        st.success("PDF uploaded successfully.")

    except Exception as e:
        st.error(f"Could not read PDF: {e}")

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded image", use_container_width=True)

if st.button("Submit"):

    try:

        if uploaded_image is not None:

            prompt = question if question else "Describe this image in detail."

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    prompt,
                    image
                ]
            )

        else:

            prompt = f"""
You are an AI Study Assistant.

Use the PDF content below to answer the user's question.

Generate:

1. A concise summary
2. 5 flashcards
3. 5 multiple-choice questions with answers
4. Important revision questions

PDF Content:
{pdf_text}

User Question:
{question}
"""

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

        st.subheader("Answer")
        st.write(response.text)

    except Exception as e:
        st.error(f"Error: {e}")
