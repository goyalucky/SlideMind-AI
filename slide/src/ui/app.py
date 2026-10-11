import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI PowerPoint Generator", layout="centered")

st.title("AI-Based PowerPoint Slide Generator")
st.write("Upload your document (PDF, DOCX, CSV, TXT) to generate a presentation deck automatically.")

# Correct method name: file_uploader
uploaded_file = st.file_uploader(
    "Choose a document",
    type=["txt", "pdf", "docx", "csv"]
)

if uploaded_file is not None:
    st.info(f"Selected file: **{uploaded_file.name}**")

    # Upload action
    if st.button("Upload to Server"):
        with st.spinner("Uploading document..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            try:
                upload_res = requests.post(f"{BASE_URL}/upload/", files=files)
                if upload_res.status_code == 200:
                    st.success("File uploaded to server successfully!")
                    st.session_state["file_uploaded"] = True
                else:
                    st.error(f"Upload failed: {upload_res.text}")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to FastAPI backend. Ensure Uvicorn is running on port 8000.")

    # Generate slides action
    if st.button("Generate Slides"):
        with st.spinner("Analyzing content and generating PowerPoint slides..."):
            try:
                gen_res = requests.get(f"{BASE_URL}/generate/")
                if gen_res.status_code == 200:
                    st.success("Slides generated successfully!")
                    data = gen_res.json()
                    
                    # Construct download endpoint link
                    download_url = f"{BASE_URL}/download/?filename=output/generated_presentation.pptx"
                    
                    # Fetch file bytes directly for Streamlit download button
                    file_res = requests.get(download_url)
                    if file_res.status_code == 200:
                        st.download_button(
                            label="📥 Download Presentation (.pptx)",
                            data=file_res.content,
                            file_name="AI_Presentation.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                        )
                    else:
                        st.markdown(f"[Click here to download presentation]({download_url})")
                elif gen_res.status_code == 429:
                    st.warning("Google API rate limit reached. Please wait ~30 seconds before retrying.")
                else:
                    st.error(f"Slide generation failed: {gen_res.text}")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to FastAPI backend. Ensure Uvicorn is running on port 8000.")