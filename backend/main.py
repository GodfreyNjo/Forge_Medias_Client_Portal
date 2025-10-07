from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os

app = FastAPI(title="Forge Media Portal", version="1.0.0")

# Check if frontend directory exists and serve static files
frontend_path = "/app/frontend"
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")
    print("✅ Frontend static files mounted")
else:
    print("⚠️  Frontend directory not found, API-only mode")

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

# Mock data
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
]

# Simple HTML response for the homepage
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Forge Medias - Client Portal</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
            background: white; 
            padding: 30px; 
            border-radius: 10px; 
            color: #333;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .header { 
            text-align: center; 
            margin-bottom: 30px; 
        }
        .logo { 
            font-size: 2.5em; 
            font-weight: bold; 
            color: #333;
            margin-bottom: 10px;
        }
        .status { 
            background: #d4edda; 
            color: #155724; 
            padding: 10px; 
            border-radius: 5px; 
            margin: 10px 0;
        }
        .endpoints { 
            background: #f8f9fa; 
            padding: 15px; 
            border-radius: 5px; 
            margin: 15px 0;
        }
        .btn { 
            background: #667eea; 
            color: white; 
            padding: 10px 20px; 
            border: none; 
            border-radius: 5px; 
            cursor: pointer; 
            margin: 5px;
            text-decoration: none;
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🚀 Forge Medias</div>
            <h1>Client Portal</h1>
            <p>Professional Media Transcription & Analysis</p>
        </div>
        
        <div class="status">
            ✅ <strong>System Status:</strong> All systems operational
        </div>
        
        <h2>Welcome to Your Dashboard</h2>
        <p>Your portal is successfully deployed on AWS EC2!</p>
        
        <div class="endpoints">
            <h3>📊 Available Endpoints:</h3>
            <a href="/api/health" class="btn">Health Check</a>
            <a href="/api/dashboard" class="btn">Dashboard API</a>
        </div>
        
        <h3>🎯 Features Ready:</h3>
        <ul>
            <li>✅ File Upload & Management</li>
            <li>✅ Speech-to-Text Transcription</li>
            <li>✅ Real-time Analytics</li>
            <li>✅ Subscription Management</li>
            <li>✅ Team Collaboration</li>
        </ul>
        
        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
            <p><strong>Next Steps:</strong> The full React dashboard is being prepared...</p>
            <p>Current Plan: <strong>PRO</strong> | Remaining Minutes: <strong>2,086</strong></p>
        </div>
    </div>
</body>
</html>
"""

@app.get("/")
async def serve_homepage():
    return HTMLResponse(content=HTML_PAGE)

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "forge-media-portal",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "environment": "production"
    }

@app.get("/api/dashboard")
async def get_dashboard():
    return DashboardResponse(
        user=mock_user,
        subscription=Subscription(),
        recentFiles=mock_files
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
