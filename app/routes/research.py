from fastapi import APIRouter
from app.schemas.research import ResearchRequest, ResearchResponse
import sys
import os

from fastapi.responses import StreamingResponse

# Ensure the root directory is in the sys.path so we can import from pipeline.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pipeline import run_research_pipeline_stream

router = APIRouter()

@router.post("/research")
def research_topic(request: ResearchRequest):
    return StreamingResponse(
        run_research_pipeline_stream(request.topic), 
        media_type="application/x-ndjson"
    )
