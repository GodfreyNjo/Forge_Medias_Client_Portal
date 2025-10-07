from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI(title="Forge Media Portal API", version="1.0.0")

# Get allowed origins from environment
frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "https://forge-media-frontend.onrender.com"],
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

mock_user = User(
    id="1",
    email="godfrey@example.com", 
    handle="@shadcn",
    name="Godfrey"
)

mock_files = [
    File(
        id="fdca669ab2b1628868d8c6d0e630eda1e7O0Gzqj-mp4",
        fileName="meeting_recording.mp4",
        uploadedAt="07/10/2025",
        status="Transcription"
    ),
    File(
        id="daedf9fc2f347d901b642fd857133ea9RZqhUgDf-mp4",
        fileName="client_call.mp4", 
        uploadedAt="07/10/2025",
        status="Transcription"
    ),
]

@app.get("/")
async def root():
    return {"message": "Forge Media Portal API - Live!"}

@app.get("/api/dashboard")
async def get_dashboard():
    return DashboardResponse(
        user=mock_user,
        subscription=Subscription(),
        recentFiles=mock_files
    )

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "forge-media-api"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
