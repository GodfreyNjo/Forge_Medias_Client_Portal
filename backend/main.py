from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os
import uuid

app = FastAPI(title="Forge Medias Client Portal", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class User(BaseModel):
    id: str
    email: str
    name: str
    company: Optional[str] = None
    subscription: str = "Starter"
    created_at: str

class ServiceOrder(BaseModel):
    id: str
    service_type: str  # transcript_cleanup, captions_cleanup, dubbing_voiceover
    file_name: str
    status: str  # pending, in_progress, completed, delivered
    created_at: str
    estimated_completion: Optional[str] = None

class SubscriptionPlan(BaseModel):
    id: str
    name: str
    price: float
    features: List[str]
    monthly_minutes: int

class DashboardResponse(BaseModel):
    user: User
    recent_orders: List[ServiceOrder]
    subscription: SubscriptionPlan
    remaining_minutes: int

# Mock data
mock_user = User(
    id="1",
    email="client@example.com",
    name="John Smith",
    company="Tech Solutions Inc",
    subscription="Professional",
    created_at="2024-10-01"
)

mock_orders = [
    ServiceOrder(
        id="ORD-001",
        service_type="transcript_cleanup",
        file_name="client_interview_october.mp4",
        status="completed",
        created_at="2024-10-05"
    ),
    ServiceOrder(
        id="ORD-002", 
        service_type="captions_cleanup",
        file_name="product_demo_video.mp4",
        status="in_progress",
        created_at="2024-10-06",
        estimated_completion="2024-10-08"
    ),
    ServiceOrder(
        id="ORD-003",
        service_type="dubbing_voiceover", 
        file_name="training_material.mp4",
        status="pending",
        created_at="2024-10-07"
    )
]

subscription_plans = {
    "starter": SubscriptionPlan(
        id="starter",
        name="Starter",
        price=49.99,
        features=["5 hours monthly", "Basic support", "Standard turnaround"],
        monthly_minutes=300
    ),
    "professional": SubscriptionPlan(
        id="professional", 
        name="Professional",
        price=99.99,
        features=["20 hours monthly", "Priority support", "Fast turnaround", "API access"],
        monthly_minutes=1200
    ),
    "enterprise": SubscriptionPlan(
        id="enterprise",
        name="Enterprise", 
        price=199.99,
        features=["Unlimited hours", "24/7 support", "Instant turnaround", "Full API access"],
        monthly_minutes=0
    )
}

# Authentication endpoints
@app.post("/api/auth/register")
async def register_user(email: str = Form(...), password: str = Form(...), name: str = Form(...), company: str = Form(None)):
    return {
        "user": {
            "id": str(uuid.uuid4()),
            "email": email,
            "name": name,
            "company": company,
            "subscription": "Starter",
            "created_at": datetime.now().isoformat()
        },
        "token": "mock-jwt-token"
    }

@app.post("/api/auth/login")
async def login_user(email: str = Form(...), password: str = Form(...)):
    return {
        "user": mock_user.dict(),
        "token": "mock-jwt-token"
    }

# Service endpoints
@app.get("/api/services")
async def get_services():
    return {
        "services": [
            {
                "id": "transcript_cleanup",
                "name": "Transcript Cleanup",
                "description": "Professional cleaning and formatting of transcription files",
                "turnaround": "24-48 hours",
                "supported_formats": [".txt", ".doc", ".docx", ".srt", ".vtt"]
            },
            {
                "id": "captions_cleanup", 
                "name": "Captions & Subtitles Cleanup",
                "description": "Clean and synchronize caption files for videos",
                "turnaround": "24 hours", 
                "supported_formats": [".srt", ".vtt", ".ass", ".sub"]
            },
            {
                "id": "dubbing_voiceover",
                "name": "Dubbing & Voiceover",
                "description": "Professional voiceover services and audio dubbing",
                "turnaround": "48-72 hours",
                "supported_formats": [".mp4", ".mov", ".avi", ".mp3", ".wav"]
            }
        ]
    }

@app.post("/api/orders/create")
async def create_order(
    service_type: str = Form(...),
    file: UploadFile = File(...),
    instructions: str = Form(None)
):
    order_id = f"ORD-{str(uuid.uuid4())[:8].upper()}"
    
    return {
        "order_id": order_id,
        "service_type": service_type,
        "file_name": file.filename,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "message": "Order created successfully"
    }

@app.get("/api/orders")
async def get_user_orders():
    return {"orders": mock_orders}

@app.get("/api/dashboard")
async def get_dashboard():
    return DashboardResponse(
        user=mock_user,
        recent_orders=mock_orders,
        subscription=subscription_plans["professional"],
        remaining_minutes=864
    )

@app.get("/api/subscription/plans")
async def get_subscription_plans():
    return {"plans": subscription_plans}

@app.post("/api/subscription/upgrade")
async def upgrade_subscription(plan_id: str = Form(...)):
    return {
        "message": f"Subscription upgraded to {plan_id}",
        "success": True,
        "redirect_url": "/payment/checkout"
    }

# Knowledge Base endpoints
@app.get("/api/knowledge-base")
async def get_knowledge_base():
    return {
        "categories": [
            {
                "id": "getting_started",
                "name": "Getting Started",
                "articles": [
                    {"id": "gs1", "title": "How to upload your first file", "url": "/kb/upload-guide"},
                    {"id": "gs2", "title": "Supported file formats", "url": "/kb/supported-formats"},
                    {"id": "gs3", "title": "Understanding turnaround times", "url": "/kb/turnaround"}
                ]
            },
            {
                "id": "services",
                "name": "Services",
                "articles": [
                    {"id": "sv1", "title": "Transcript cleanup best practices", "url": "/kb/transcript-guide"},
                    {"id": "sv2", "title": "Caption formatting standards", "url": "/kb/caption-standards"},
                    {"id": "sv3", "title": "Voiceover requirements", "url": "/kb/voiceover-requirements"}
                ]
            },
            {
                "id": "billing",
                "name": "Billing & Subscription",
                "articles": [
                    {"id": "bl1", "title": "Understanding your subscription", "url": "/kb/subscription-guide"},
                    {"id": "bl2", "title": "How to upgrade your plan", "url": "/kb/upgrade-guide"},
                    {"id": "bl3", "title": "Billing and payment methods", "url": "/kb/billing-info"}
                ]
            }
        ]
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "forge-medias-portal",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/")
async def serve_homepage():
    return HTMLResponse(content=generate_homepage())

def generate_homepage():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Forge Medias - Client Portal</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f8f9fa; 
            color: #333;
            line-height: 1.6;
        }
        .auth-container {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
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
            color: #555;
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
            margin-bottom: 15px;
        }
        .btn-secondary {
            background: #6c757d;
        }
        .switch-auth {
            text-align: center;
            margin-top: 20px;
        }
        .switch-auth a {
            color: #1e3c72;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="auth-container">
        <div class="auth-box">
            <div class="logo">Forge Medias</div>
            
            <div id="loginForm">
                <h2 style="text-align: center; margin-bottom: 30px; color: #333;">Client Login</h2>
                <form onsubmit="handleLogin(event)">
                    <div class="form-group">
                        <label>Email Address</label>
                        <input type="email" id="loginEmail" required>
                    </div>
                    <div class="form-group">
                        <label>Password</label>
                        <input type="password" id="loginPassword" required>
                    </div>
                    <button type="submit" class="btn">Sign In</button>
                </form>
                <div class="switch-auth">
                    Don't have an account? <a href="#" onclick="showRegister()">Create Account</a>
                </div>
            </div>

            <div id="registerForm" style="display: none;">
                <h2 style="text-align: center; margin-bottom: 30px; color: #333;">Create Account</h2>
                <form onsubmit="handleRegister(event)">
                    <div class="form-group">
                        <label>Full Name</label>
                        <input type="text" id="registerName" required>
                    </div>
                    <div class="form-group">
                        <label>Company (Optional)</label>
                        <input type="text" id="registerCompany">
                    </div>
                    <div class="form-group">
                        <label>Email Address</label>
                        <input type="email" id="registerEmail" required>
                    </div>
                    <div class="form-group">
                        <label>Password</label>
                        <input type="password" id="registerPassword" required>
                    </div>
                    <button type="submit" class="btn">Create Account</button>
                </form>
                <div class="switch-auth">
                    Already have an account? <a href="#" onclick="showLogin()">Sign In</a>
                </div>
            </div>
        </div>
    </div>

    <script>
        function showRegister() {
            document.getElementById('loginForm').style.display = 'none';
            document.getElementById('registerForm').style.display = 'block';
        }

        function showLogin() {
            document.getElementById('registerForm').style.display = 'none';
            document.getElementById('loginForm').style.display = 'block';
        }

        async function handleLogin(event) {
            event.preventDefault();
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;
            
            // For demo - redirect to dashboard
            window.location.href = '/dashboard.html';
        }

        async function handleRegister(event) {
            event.preventDefault();
            const name = document.getElementById('registerName').value;
            const company = document.getElementById('registerCompany').value;
            const email = document.getElementById('registerEmail').value;
            const password = document.getElementById('registerPassword').value;
            
            // For demo - redirect to dashboard
            window.location.href = '/dashboard.html';
        }
    </script>
</body>
</html>
"""
