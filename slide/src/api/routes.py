import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from src.agents.extractor import ContentExtractor
from src.agents.summarizer import Summarizer
from src.agents.slide_generator import SlideGenerator

router = APIRouter()

# Resolve absolute path to project root directories
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file for slide generation"""
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "message": "File uploaded successfully!"}

@router.get("/generate/")
async def generate_presentation():
    """Runs the AI pipeline to generate PowerPoint slides."""
    extractor = ContentExtractor(directory=UPLOAD_DIR)
    extracted_content = extractor.extract_from_directory()

    if not extracted_content:
        raise HTTPException(status_code=400, detail="No extractable documents found in uploads folder.")

    summarizer = Summarizer(model="gemini-3.5-flash-lite")
    slide_generator = SlideGenerator(output_dir=OUTPUT_DIR)

    last_saved_path = None

    for filename, text in extracted_content.items():
        if not text.strip():
            continue

        try:
            summary = summarizer.summarize_text(text)
        except RuntimeError as e:
            raise HTTPException(status_code=429, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LLM processing error: {e}")

        # Clean raw bullet markdown formatting (*, -, leading whitespace)
        raw_lines = summary.split("\n")
        summary_points = [
            line.lstrip("*-• ").strip()
            for line in raw_lines
            if line.strip() and not line.strip().startswith("#")
        ]

        title = os.path.splitext(filename)[0]
        slide_generator.create_slide_deck(title, summary_points)
        last_saved_path = os.path.join(OUTPUT_DIR, "generated_presentation.pptx")

    if not last_saved_path or not os.path.exists(last_saved_path):
        raise HTTPException(status_code=500, detail="Presentation generation failed.")

    return {
        "message": "Slides generated successfully!",
        "download_url": f"/api/download/?filename={last_saved_path}"
    }

@router.get("/download/")
async def download_presentation(filename: str):
    """Download the generated PowerPoint presentation"""
    if not os.path.exists(filename):
        raise HTTPException(status_code=404, detail="Requested presentation file not found.")

    return FileResponse(
        filename,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename="AI_Presentation.pptx"
    )