import os, shutil
from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from pathlib import Path
from src.models.model import Whisper

router = APIRouter()
wp = Whisper()

root_dir = str(Path.cwd())

# Pydantic model for the response
class TranscriptResponse(BaseModel):
    transcript: str


@router.post("/transcribe/", response_model=TranscriptResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    """
    This endpoint is used to perform transcription service based on the audio file using open source whisper model

    Args:
        UploadFile (File, required): _description_. 
        - Acceptable Audio file formats are wav, mpeg, mp4, flac, mp3. wav format is recommended
        
    """
    # Check if the file format is supported
    if file.content_type not in ["audio/wav", "audio/wave", "audio/mpeg", "audio/mp3", "audio/flac", "audio/x-flac"]:
        print(file.content_type)
        raise HTTPException(status_code=400, detail="Unsupported file format. Supported file formats are wav, mp3, and flac")
    
    file_contents = await file.read()  # Read the content of the uploaded file

    transcript = wp.process_transcribing(
        file_name=file.filename,
        file_contents=file_contents  # Pass the byte content
    )

    return TranscriptResponse(transcript=transcript)