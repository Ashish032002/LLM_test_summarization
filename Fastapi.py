from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
from typing import Optional
import time
from pathlib import Path

# Initialize FastAPI app
app = FastAPI(
    title="Text Summarization API",
    description="API for summarizing text using T5 model",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the path to frontend files
FRONTEND_DIR = Path("Frontend")
STATIC_DIR = FRONTEND_DIR / "static"

# Mount static files directory
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Load the fine-tuned model and tokenizer
model = None
tokenizer = None
try:
    model_path = "./deployed_model"
    model = T5ForConditionalGeneration.from_pretrained(model_path)
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    print("Model and tokenizer loaded successfully")
except Exception as e:
    print(f"Error loading model: {str(e)}")


class TextRequest(BaseModel):
    text: str
    max_length: Optional[int] = 150
    min_length: Optional[int] = 40
    num_beams: Optional[int] = 4


class SummaryResponse(BaseModel):
    summary: str
    processing_time: float


# Root endpoint - serve the frontend HTML
@app.get("/", response_class=HTMLResponse)
async def root():
    html_file = FRONTEND_DIR / "index.html"
    if html_file.exists():
        with open(html_file) as f:
            return f.read()
    return HTMLResponse(
        """
        <html>
            <head>
                <title>Text Summarization API</title>
            </head>
            <body>
                <h1>Welcome to the Text Summarization API</h1>
                <p>Available endpoints:</p>
                <ul>
                    <li><a href="/docs">/docs</a> - API documentation</li>
                    <li><a href="/health">/health</a> - API health check</li>
                    <li>/summarize - POST endpoint for text summarization</li>
                </ul>
            </body>
        </html>
        """,
        status_code=404
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None and tokenizer is not None
    }


# Summarization function
def summarize_text(text: str, max_length: int = 150, min_length: int = 40, num_beams: int = 4) -> str:
    if model is None or tokenizer is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    input_ids = tokenizer.encode(
        "summarize: " + text,
        return_tensors="pt",
        max_length=512,
        truncation=True
    )

    summary_ids = model.generate(
        input_ids,
        max_length=max_length,
        min_length=min_length,
        num_beams=num_beams,
        early_stopping=True
    )

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary


# Define API endpoint for text summarization
@app.post("/summarize", response_model=SummaryResponse)
async def summarize(request: TextRequest):
    start_time = time.time()

    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    summary = summarize_text(
        request.text,
        max_length=request.max_length,
        min_length=request.min_length,
        num_beams=request.num_beams
    )

    processing_time = time.time() - start_time

    return SummaryResponse(
        summary=summary,
        processing_time=processing_time
    )


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return HTMLResponse(
        """
        <h1>404 - Page Not Found</h1>
        <p>The requested page was not found. Please check the URL or visit the <a href="/">homepage</a>.</p>
        """,
        status_code=404
    )

# Optional: Add favicon endpoint to prevent browser errors
@app.get('/favicon.ico')
async def favicon():
    favicon_path = STATIC_DIR / 'favicon.ico'
    return FileResponse(favicon_path) if favicon_path.exists() else {}