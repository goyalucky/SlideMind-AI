# SlideMind-AI: Agentic Presentation Generation System 📊🤖

An intelligent, multi-agent AI system designed to transform raw documents, PDFs, and unstructured text into structured, visually engaging presentation decks (`.pptx`). 

SlideMind-AI orchestrates autonomous agents using **CrewAI**, **LlamaIndex**, and **OpenAI** to handle document parsing, semantic summarization, prompt-based visual generation, and programmatically compiled slide layouts via **python-pptx**.

---

## 🌟 Key Features

- **Multi-Agent Orchestration**: Specialized agents collaborate sequentially to extract, synthesize, visualize, and assemble slides.
- **Document Ingestion**: Extracts text, structure, and context from PDFs and documents using **PyMuPDF**, **python-docx**, and **LlamaIndex**.
- **Context-Aware Summarization**: Condenses key takeaways into presentation-ready bullet points, headers, and speaker notes.
- **Automated Visual Asset Synthesis**: Generates relevant illustrations and conceptual figures (DALL·E / Matplotlib charts).
- **Native PowerPoint Export**: Produces cleanly styled `.pptx` presentations using **python-pptx**.
- **Dual Interface**:
  - **FastAPI Backend**: Robust RESTful APIs for programmatic integration and automation.
  - **Streamlit Web UI**: Interactive user interface for uploading files and customizing slide decks.

---

## 🏗️ System Architecture & Workflow

```
[Uploaded Document / PDF]
           │
           ▼
┌─────────────────────────┐
│     Extractor Agent     │  ◄── Ingests PDF / DOCX via PyMuPDF & LlamaIndex
└──────────┬──────────────┘
           │ Structured Text / Chunks
           ▼
┌─────────────────────────┐
│    Summarizer Agent     │  ◄── Structures content into slide-by-slide concepts
└──────────┬──────────────┘
           │ Slide Blueprint & Visual Prompts
           ▼
┌─────────────────────────┐
│  Image Generator Agent  │  ◄── Generates contextual images or data charts
└──────────┬──────────────┘
           │ Assets & Layout Metadata
           ▼
┌─────────────────────────┐
│  Slide Generator Agent  │  ◄── Compiles final .pptx presentation via python-pptx
└──────────┬──────────────┘
           │
           ▼
    [.pptx File Output]
```

### Agent Roles

1. **`extractor.py` (Document Extraction Agent)**: 
   Parses raw input files (`PDF`, `DOCX`, text), extracts textual tokens, and chunks them semantically using LlamaIndex and PyMuPDF.
2. **`summarizer.py` (Content Strategy & Summarizer Agent)**: 
   Breaks down raw extracted data into distinct presentation slides, identifying titles, key bullets, speaker notes, and layout intent.
3. **`image_generator.py` (Visual Asset Agent)**: 
   Translates visual descriptions into generated imagery (OpenAI Image API) or dynamic analytical charts using Matplotlib.
4. **`slide_generator.py` (Presentation Builder Agent)**: 
   Takes structured output from the upstream agents and builds editable, stylized PowerPoint slides using `python-pptx`.

---

## 📁 Repository Structure

```text
slide/
│
├── data/                       # Sample files, test documents, or reference resumes
│   └── luckygoyal_resume.pdf
│
├── src/
│   ├── agents/                 # Multi-agent logic (CrewAI / LLM logic)
│   │   ├── extractor.py        # PDF & document extraction agent
│   │   ├── summarizer.py       # Slide narrative & bullet summarizer
│   │   ├── image_generator.py  # Image prompt creator & chart generator
│   │   └── slide_generator.py  # PPTX creation & layout assembly
│   │
│   ├── api/                    # Backend API layer
│   │   ├── main.py             # FastAPI entry point & middleware setup
│   │   └── routes.py           # API endpoints (file upload, generation triggers)
│   │
│   └── ui/                     # Frontend user interface
│       └── app.py              # Streamlit dashboard for end-user interaction
│
├── uploads/                    # Temporary storage for user-uploaded files
├── .env                        # Environment variables & API keys (ignored by git)
├── .gitignore                  # Git ignore rules
└── requirements.txt            # Python dependencies
```

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.10 or higher
- An active **Gemini API Key**

### 2. Clone the Repository

```bash
git clone https://github.com/goyalucky/SlideMind-AI.git
cd SlideMind-AI
```

### 3. Create and Activate a Virtual Environment

```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root directory and add your credentials:

```env
GEMINI_API_KEY=your_openai_api_key_here
```

---

## 💻 Running the Application

You can interact with SlideMind-AI either through the interactive **Streamlit UI** or directly via the **FastAPI REST API**.

### Option A: Launch the Streamlit Frontend

```bash
streamlit run src/ui/app.py
```
Open your browser and navigate to `http://localhost:8501`.

### Option B: Run the FastAPI Server

```bash
uvicorn src.api.main:app --reload --port 8000
```
- API Docs (Swagger UI): `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`

---

## 📦 Tech Stack

- **Frameworks & Orchestration**: [CrewAI](https://github.com/joaomdmoura/crewAI), [LlamaIndex](https://github.com/run-llama/llama_index)
- **Large Language Models**: [OpenAI GPT-4o / DALL·E](https://openai.com/)
- **Document Processing**: `PyMuPDF` (fitz), `python-docx`
- **Presentation Engine**: `python-pptx`, `matplotlib`
- **API & UI**: `FastAPI`, `Uvicorn`, `Streamlit`

---

## 🛡️ License

This project is licensed under the [MIT License](LICENSE).