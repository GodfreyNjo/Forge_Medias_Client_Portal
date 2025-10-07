from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import os
from datetime import datetime

app = FastAPI(title="Forge Media Portal API", version="1.0.0")

# Serve frontend static files
app.mount("/", StaticFiles(directory="frontend/.next", html=True), name="static")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, you might want to restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    id: str
    email: str
    handle: Optional[str] = None
    name: Optional[str] = None

class Subscription(BaseModel):
    planType: str = "PRO"
    monthlyMinutes: int = 5000
    usedMinutes: int = 2914
    remainingMinutes: int = 2086

class File(BaseModel):
    id: str
    fileName: str
    uploadedAt: str
    status: str

class DashboardResponse(BaseModel):
    user: User
    subscription: Subscription
    recentFiles: List[File]

# Enhanced mock data
mock_user = User(
    id="1",
    email="godfrey@example.com", 
    handle="@shadcn",
    name="Godfrey"
)

mock_files = [
    File(
        id="fdca669ab2b1628868d8c6d0e630eda1e7O0Gzqj-mp4",
        fileName="client_meeting_recording.mp4",
        uploadedAt="07/10/2025",
        status="Transcription"
    ),
    File(
        id="daedf9fc2f347d901b642fd857133ea9RZqhUgDf-mp4",
        fileName="product_demo_video.mp4", 
        uploadedAt="07/10/2025",
        status="Completed"
    ),
    File(
        id="2f614c69d6b1a20451bb7496066930cfIaucCP9y-mp4",
        fileName="team_interview_session.mp4",
        uploadedAt="07/10/2025",
        status="Processing"
    ),
]

@app.get("/")
async def root():
    return {"message": "Forge Media Portal - Full Stack Application"}

@app.get("/api/dashboard")
async def get_dashboard():
    return DashboardResponse(
        user=mock_user,
        subscription=Subscription(),
        recentFiles=mock_files
    )

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "forge-media-api",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
