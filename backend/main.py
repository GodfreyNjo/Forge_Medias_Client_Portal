from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os

app = FastAPI(title="Forge Medias Client Portal")

# Data Models
class User(BaseModel):
    id: str
    email: str
    name: str
    company: Optional[str] = None
    subscription: str = "Starter"

class ServiceOrder(BaseModel):
    id: str
    service_type: str
    file_name: str
    status: str
    created_at: str

class DashboardResponse(BaseModel):
    user: User
    recent_orders: List[ServiceOrder]
    remaining_minutes: int

# Mock data
mock_user = User(
    id="1",
    email="client@example.com",
    name="John Smith",
    company="Tech Solutions Inc",
    subscription="Professional"
)

mock_orders = [
    ServiceOrder(
        id="ORD-001",
        service_type="transcript_cleanup",
        file_name="client_interview.mp4",
        status="completed",
        created_at="2024-10-05"
    ),
    ServiceOrder(
        id="ORD-002", 
        service_type="captions_cleanup",
        file_name="product_demo.mp4",
        status="in_progress",
        created_at="2024-10-06"
    )
]

# Authentication and Dashboard HTML
login_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Forge Medias - Client Portal</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .auth-box {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 400px;
        }
        .logo {
            text-align: center;
            margin-bottom: 30px;
            color: #1e3c72;
            font-size: 28px;
            font-weight: bold;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 500;
        }
        .form-group input {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        .btn {
            width: 100%;
            padding: 12px;
            background: #1e3c72;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="auth-box">
        <div class="logo">Forge Medias</div>
        <h2 style="text-align: center; margin-bottom: 30px;">Client Login</h2>
        <form onsubmit="handleLogin(event)">
            <div class="form-group">
                <label>Email Address</label>
                <input type="email" id="loginEmail" required>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" id="loginPassword" required>
            </div>
            <button type="submit" class="btn">Sign In to Dashboard</button>
        </form>
        <div style="text-align: center; margin-top: 20px;">
            <a href="#" onclick="alert('Use any credentials for demo')" style="color: #1e3c72;">Create Account</a>
        </div>
    </div>
    <script>
        function handleLogin(event) {
            event.preventDefault();
            window.location.href = '/dashboard';
        }
    </script>
</body>
</html>
"""

dashboard_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard - Forge Medias</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: #f8f9fa; 
            margin: 0;
            color: #333;
        }
        .header {
            background: white;
            border-bottom: 1px solid #e0e0e0;
            padding: 0 20px;
        }
        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            height: 70px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .logo { 
            font-size: 24px; 
            font-weight: bold; 
            color: #1e3c72; 
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .welcome-banner {
            background: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .service-card {
            background: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #1e3c72;
        }
        .btn {
            background: #1e3c72;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div class="logo">Forge Medias</div>
            <div>Welcome, John Smith | <button class="btn" onclick="logout()">Logout</button></div>
        </div>
    </div>

    <div class="container">
        <div class="welcome-banner">
            <h1>Welcome to Your Media Services Dashboard</h1>
            <p>Professional transcript cleanup, captions, and voiceover services.</p>
            <p><strong>Plan:</strong> Professional | <strong>Remaining Minutes:</strong> 864</p>
        </div>

        <div class="services-grid">
            <div class="service-card">
                <h3>Transcript Cleanup</h3>
                <p>Professional cleaning and formatting of transcription files. Upload your raw transcripts for expert cleanup.</p>
                <p><strong>Turnaround:</strong> 24-48 hours</p>
                <button class="btn" onclick="uploadFile('transcript')">Upload Transcript Files</button>
            </div>
            
            <div class="service-card">
                <h3>Captions & Subtitles Cleanup</h3>
                <p>Clean and synchronize caption files for your videos. Perfect timing and formatting guaranteed.</p>
                <p><strong>Turnaround:</strong> 24 hours</p>
                <button class="btn" onclick="uploadFile('captions')">Upload Caption Files</button>
            </div>
            
            <div class="service-card">
                <h3>Dubbing & Voiceover</h3>
                <p>Professional voiceover services and audio dubbing. Multiple languages available.</p>
                <p><strong>Turnaround:</strong> 48-72 hours</p>
                <button class="btn" onclick="uploadFile('voiceover')">Upload Audio/Video Files</button>
            </div>
        </div>

        <div style="background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h2>Recent Orders</h2>
            <div id="ordersList">
                <p>ORD-001: Transcript Cleanup (Completed)</p>
                <p>ORD-002: Captions Cleanup (In Progress)</p>
            </div>
        </div>
    </div>

    <script>
        function uploadFile(service) {
            alert('File upload for ' + service + ' service would start here. Ready for integration.');
        }

        function logout() {
            if (confirm('Are you sure you want to logout?')) {
                window.location.href = '/';
            }
        }
    </script>
</body>
</html>
"""

@app.get("/")
async def serve_login():
    return HTMLResponse(content=login_html)

@app.get("/dashboard")
async def serve_dashboard():
    return HTMLResponse(content=dashboard_html)

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "forge-medias-portal", 
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/services")
async def get_services():
    return {
        "services": [
            {
                "id": "transcript_cleanup",
                "name": "Transcript Cleanup",
                "description": "Professional cleaning and formatting of transcription files",
                "turnaround": "24-48 hours"
            },
            {
                "id": "captions_cleanup", 
                "name": "Captions & Subtitles Cleanup",
                "description": "Clean and synchronize caption files for videos",
                "turnaround": "24 hours"
            },
            {
                "id": "dubbing_voiceover",
                "name": "Dubbing & Voiceover", 
                "description": "Professional voiceover services and audio dubbing",
                "turnaround": "48-72 hours"
            }
        ]
    }

@app.get("/api/orders")
async def get_orders():
    return {"orders": mock_orders}

@app.get("/api/dashboard")
async def get_dashboard_data():
    return DashboardResponse(
        user=mock_user,
        recent_orders=mock_orders,
        remaining_minutes=864
    )

if __name__ == "__main__":
    import uvicorn
    print("🚀 Forge Medias Client Portal Starting...")
    uvicorn.run(app, host="0.0.0.0", port=8000, access_log=True)
