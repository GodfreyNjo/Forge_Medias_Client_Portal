from pydantic import BaseModel
from typing import List

class Service(BaseModel):
    id: str
    name: str
    description: str
    turnaround: str
    supported_formats: List[str]

# Available services
SERVICES = {
    "transcript_cleanup": Service(
        id="transcript_cleanup",
        name="Transcript Cleanup",
        description="Professional cleaning and formatting of transcription files",
        turnaround="24-48 hours",
        supported_formats=[".txt", ".doc", ".docx", ".srt", ".vtt"]
    ),
    "captions_cleanup": Service(
        id="captions_cleanup",
        name="Captions & Subtitles Cleanup",
        description="Clean and synchronize caption files for videos",
        turnaround="24 hours",
        supported_formats=[".srt", ".vtt", ".ass", ".sub"]
    ),
    "dubbing_voiceover": Service(
        id="dubbing_voiceover",
        name="Dubbing & Voiceover",
        description="Professional voiceover services and audio dubbing",
        turnaround="48-72 hours",
        supported_formats=[".mp4", ".mov", ".avi", ".mp3", ".wav"]
    )
}
