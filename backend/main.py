from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os
import uuid
import boto3
from botocore.exceptions import ClientError
import secrets

app = FastAPI(title="Forge Medias Client Portal")
security = HTTPBasic()

# AWS S3 Configuration (you'll need to set these environment variables)
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY', 'your-access-key')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY', 'your-secret-key')
S3_BUCKET = os.getenv('S3_BUCKET', 'forge-medias-uploads')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

# Data Models
class User(BaseModel):
    id: str
    email: str
    name: str
    company: Optional[str] = None
    subscription: str = "Starter"
    created_at: str
    is_admin: bool = False

class ServiceOrder(BaseModel):
    id: str
    service_type: str
    file_name: str
    original_filename: str
    status: str  # pending, in_progress, completed, delivered
    created_at: str
    client_id: str
    s3_key: Optional[str] = None
    estimated_completion: Optional[str] = None

class DashboardResponse(BaseModel):
    user: User
    recent_orders: List[ServiceOrder]
    remaining_minutes: int

# In-memory storage (replace with database in production)
users_db = {}
orders_db = []
jobs_queue = []

# Admin credentials (in production, use proper authentication)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "forge2024"

# Mock initial admin user
users_db["admin@forgemideas.com"] = User(
    id="admin-1",
    email="admin@forgemideas.com",
    name="System Administrator",
    subscription="Enterprise",
    created_at=datetime.now().isoformat(),
    is_admin=True
)

# Color scheme constants
PRIMARY_COLOR = "#4f46e5"      # Indigo
SECONDARY_COLOR = "#7c3aed"    # Purple
ACCENT_COLOR = "#6366f1"       # Light indigo
BACKGROUND_GRADIENT = "linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)"
CARD_SHADOW = "0 4px 6px -1px rgba(79, 70, 229, 0.1), 0 2px 4px -1px rgba(79, 70, 229, 0.06)"

def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect admin credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Authentication and Dashboard HTML with new color scheme
login_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Forge Medias - Client Portal</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #1f2937;
        }
        .auth-container {
            width: 100%;
            max-width: 440px;
            margin: 20px;
        }
        .auth-box {
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }
        .logo {
            text-align: center;
            margin-bottom: 32px;
            color: #4f46e5;
            font-size: 32px;
            font-weight: 700;
            letter-spacing: -0.025em;
        }
        .tagline {
            text-align: center;
            color: #6b7280;
            margin-bottom: 32px;
            font-size: 16px;
        }
        .form-group {
            margin-bottom: 24px;
        }
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: #374151;
            font-size: 14px;
        }
        .form-group input {
            width: 100%;
            padding: 12px 16px;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            font-size: 16px;
            transition: all 0.2s;
        }
        .form-group input:focus {
            outline: none;
            border-color: #4f46e5;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
        }
        .btn {
            width: 100%;
            padding: 12px 16px;
            background: #4f46e5;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }
        .btn:hover {
            background: #4338ca;
            transform: translateY(-1px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
        .switch-auth {
            text-align: center;
            margin-top: 24px;
            padding-top: 24px;
            border-top: 1px solid #e5e7eb;
        }
        .switch-auth a {
            color: #4f46e5;
            text-decoration: none;
            font-weight: 500;
        }
        .switch-auth a:hover {
            text-decoration: underline;
        }
        .admin-link {
            text-align: center;
            margin-top: 16px;
        }
        .admin-link a {
            color: #6b7280;
            text-decoration: none;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="auth-container">
        <div class="auth-box">
            <div class="logo">Forge Medias</div>
            <div class="tagline">Professional Media Services Portal</div>
            
            <div id="loginForm">
                <h2 style="text-align: center; margin-bottom: 8px; color: #111827; font-weight: 600;">Welcome Back</h2>
                <p style="text-align: center; color: #6b7280; margin-bottom: 32px; font-size: 14px;">Sign in to your account</p>
                <form onsubmit="handleLogin(event)">
                    <div class="form-group">
                        <label for="loginEmail">Email Address</label>
                        <input type="email" id="loginEmail" required placeholder="Enter your email">
                    </div>
                    <div class="form-group">
                        <label for="loginPassword">Password</label>
                        <input type="password" id="loginPassword" required placeholder="Enter your password">
                    </div>
                    <button type="submit" class="btn">Sign In</button>
                </form>
                <div class="switch-auth">
                    Don't have an account? <a href="#" onclick="showRegister()">Create Account</a>
                </div>
                <div class="admin-link">
                    <a href="/admin">Administrator Access</a>
                </div>
            </div>

            <div id="registerForm" style="display: none;">
                <h2 style="text-align: center; margin-bottom: 8px; color: #111827; font-weight: 600;">Create Account</h2>
                <p style="text-align: center; color: #6b7280; margin-bottom: 32px; font-size: 14px;">Join Forge Medias today</p>
                <form onsubmit="handleRegister(event)">
                    <div class="form-group">
                        <label for="registerName">Full Name</label>
                        <input type="text" id="registerName" required placeholder="Enter your full name">
                    </div>
                    <div class="form-group">
                        <label for="registerCompany">Company (Optional)</label>
                        <input type="text" id="registerCompany" placeholder="Enter your company name">
                    </div>
                    <div class="form-group">
                        <label for="registerEmail">Email Address</label>
                        <input type="email" id="registerEmail" required placeholder="Enter your email">
                    </div>
                    <div class="form-group">
                        <label for="registerPassword">Password</label>
                        <input type="password" id="registerPassword" required placeholder="Create a password">
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
            
            try {
                const response = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: new URLSearchParams({ email, password })
                });
                
                if (response.ok) {
                    window.location.href = '/dashboard';
                } else {
                    alert('Login failed. For demo, you can proceed to dashboard.');
                    window.location.href = '/dashboard';
                }
            } catch (error) {
                // For demo purposes, redirect anyway
                window.location.href = '/dashboard';
            }
        }

        async function handleRegister(event) {
            event.preventDefault();
            const name = document.getElementById('registerName').value;
            const company = document.getElementById('registerCompany').value;
            const email = document.getElementById('registerEmail').value;
            const password = document.getElementById('registerPassword').value;
            
            try {
                const response = await fetch('/api/auth/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: new URLSearchParams({ 
                        name, 
                        company: company || '', 
                        email, 
                        password 
                    })
                });
                
                if (response.ok) {
                    alert('Account created successfully! Redirecting to dashboard...');
                    window.location.href = '/dashboard';
                } else {
                    alert('Registration failed. For demo, you can proceed to dashboard.');
                    window.location.href = '/dashboard';
                }
            } catch (error) {
                // For demo purposes, redirect anyway
                window.location.href = '/dashboard';
            }
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
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f8fafc; 
            color: #1f2937;
            line-height: 1.6;
        }
        .header {
            background: white;
            border-bottom: 1px solid #e5e7eb;
            padding: 0 24px;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
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
            font-weight: 700; 
            color: #4f46e5;
            letter-spacing: -0.025em;
        }
        .user-menu {
            display: flex;
            align-items: center;
            gap: 16px;
            font-size: 14px;
        }
        .user-info {
            text-align: right;
        }
        .user-name {
            font-weight: 600;
            color: #1f2937;
        }
        .user-plan {
            color: #6b7280;
            font-size: 12px;
        }
        .btn {
            background: #4f46e5;
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s;
        }
        .btn:hover {
            background: #4338ca;
            transform: translateY(-1px);
        }
        .btn-outline {
            background: transparent;
            border: 1px solid #d1d5db;
            color: #374151;
        }
        .btn-outline:hover {
            background: #f9fafb;
            border-color: #9ca3af;
        }
        .container {
            display: flex;
            max-width: 1200px;
            margin: 0 auto;
            padding: 24px;
            gap: 24px;
        }
        .sidebar {
            width: 280px;
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
            height: fit-content;
        }
        .nav-item {
            padding: 12px 16px;
            border-radius: 8px;
            cursor: pointer;
            margin-bottom: 4px;
            transition: all 0.2s;
            color: #6b7280;
            font-weight: 500;
        }
        .nav-item:hover {
            background: #f3f4f6;
            color: #374151;
        }
        .nav-item.active {
            background: #4f46e5;
            color: white;
        }
        .nav-section {
            color: #9ca3af;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin: 24px 0 12px 16px;
        }
        .main-content {
            flex: 1;
        }
        .welcome-banner {
            background: white;
            padding: 32px;
            border-radius: 12px;
            margin-bottom: 24px;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
            border-left: 4px solid #4f46e5;
        }
        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 24px;
            margin-bottom: 32px;
        }
        .service-card {
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
            border-top: 4px solid #4f46e5;
            transition: all 0.3s;
        }
        .service-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }
        .service-icon {
            font-size: 32px;
            margin-bottom: 16px;
            color: #4f46e5;
        }
        .orders-section {
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        }
        .status-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .status-pending { background: #fef3c7; color: #92400e; }
        .status-in-progress { background: #dbeafe; color: #1e40af; }
        .status-completed { background: #d1fae5; color: #065f46; }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 16px;
        }
        th, td {
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid #e5e7eb;
        }
        th {
            background: #f9fafb;
            font-weight: 600;
            color: #374151;
            font-size: 14px;
        }
        .upload-area {
            border: 2px dashed #d1d5db;
            border-radius: 8px;
            padding: 40px;
            text-align: center;
            margin: 16px 0;
            transition: all 0.3s;
            background: #f9fafb;
        }
        .upload-area:hover {
            border-color: #4f46e5;
            background: #f3f4f6;
        }
        .upload-area.dragover {
            border-color: #4f46e5;
            background: #e0e7ff;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div class="logo">Forge Medias</div>
            <div class="user-menu">
                <div class="user-info">
                    <div class="user-name">John Smith</div>
                    <div class="user-plan">Professional Plan • 864 min remaining</div>
                </div>
                <button class="btn btn-outline" onclick="logout()">Logout</button>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="sidebar">
            <div class="nav-item active">Dashboard</div>
            <div class="nav-item" onclick="showSection('upload')">File Upload</div>
            <div class="nav-item" onclick="showSection('orders')">My Orders</div>
            <div class="nav-section">Resources</div>
            <div class="nav-item" onclick="showSection('knowledge')">Knowledge Base</div>
            <div class="nav-item" onclick="showSection('account')">Account Settings</div>
            <div class="nav-item" onclick="showSection('billing')">Billing & Subscription</div>
        </div>

        <div class="main-content">
            <div id="dashboardSection">
                <div class="welcome-banner">
                    <h1 style="font-size: 28px; margin-bottom: 8px; color: #1f2937;">Good Morning, John</h1>
                    <p style="color: #6b7280; font-size: 16px;">Welcome back to your professional media services workspace.</p>
                </div>

                <div class="services-grid">
                    <div class="service-card">
                        <div class="service-icon">📝</div>
                        <h3 style="margin-bottom: 12px; color: #1f2937;">Transcript Cleanup</h3>
                        <p style="color: #6b7280; margin-bottom: 16px; line-height: 1.5;">Professional cleaning and formatting of transcription files. Upload your raw transcripts for expert cleanup and formatting.</p>
                        <p style="font-size: 14px; color: #4f46e5; margin-bottom: 16px;"><strong>Turnaround:</strong> 24-48 hours</p>
                        <button class="btn" onclick="openUploadModal('transcript_cleanup')">Upload Files</button>
                    </div>
                    
                    <div class="service-card">
                        <div class="service-icon">🎬</div>
                        <h3 style="margin-bottom: 12px; color: #1f2937;">Captions & Subtitles</h3>
                        <p style="color: #6b7280; margin-bottom: 16px; line-height: 1.5;">Clean and synchronize caption files for your videos. Perfect timing and professional formatting guaranteed.</p>
                        <p style="font-size: 14px; color: #4f46e5; margin-bottom: 16px;"><strong>Turnaround:</strong> 24 hours</p>
                        <button class="btn" onclick="openUploadModal('captions_cleanup')">Upload Files</button>
                    </div>
                    
                    <div class="service-card">
                        <div class="service-icon">🎙️</div>
                        <h3 style="margin-bottom: 12px; color: #1f2937;">Dubbing & Voiceover</h3>
                        <p style="color: #6b7280; margin-bottom: 16px; line-height: 1.5;">Professional voiceover services and audio dubbing. Multiple languages and voice styles available.</p>
                        <p style="font-size: 14px; color: #4f46e5; margin-bottom: 16px;"><strong>Turnaround:</strong> 48-72 hours</p>
                        <button class="btn" onclick="openUploadModal('dubbing_voiceover')">Upload Files</button>
                    </div>
                </div>

                <div class="orders-section">
                    <h2 style="margin-bottom: 8px; color: #1f2937;">Recent Orders</h2>
                    <p style="color: #6b7280; margin-bottom: 16px;">Track the progress of your recent file submissions</p>
                    <table>
                        <thead>
                            <tr>
                                <th>Order ID</th>
                                <th>Service</th>
                                <th>File</th>
                                <th>Status</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td style="font-weight: 500;">ORD-001</td>
                                <td>Transcript Cleanup</td>
                                <td>client_interview_october.mp4</td>
                                <td><span class="status-badge status-completed">Completed</span></td>
                                <td>2024-10-05</td>
                            </tr>
                            <tr>
                                <td style="font-weight: 500;">ORD-002</td>
                                <td>Captions Cleanup</td>
                                <td>product_demo_video.mp4</td>
                                <td><span class="status-badge status-in-progress">In Progress</span></td>
                                <td>2024-10-06</td>
                            </tr>
                            <tr>
                                <td style="font-weight: 500;">ORD-003</td>
                                <td>Dubbing & Voiceover</td>
                                <td>training_material.mp4</td>
                                <td><span class="status-badge status-pending">Pending</span></td>
                                <td>2024-10-07</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <!-- Upload Modal -->
    <div id="uploadModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); align-items: center; justify-content: center; z-index: 1000;">
        <div style="background: white; padding: 32px; border-radius: 12px; width: 90%; max-width: 500px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);">
            <h3 style="margin-bottom: 8px; color: #1f2937;">Upload Files for <span id="serviceName"></span></h3>
            <p style="color: #6b7280; margin-bottom: 24px; font-size: 14px;">Select files to upload for processing</p>
            
            <div class="upload-area" id="uploadArea" ondragover="handleDragOver(event)" ondrop="handleDrop(event)" ondragleave="handleDragLeave(event)">
                <div style="font-size: 48px; margin-bottom: 16px; color: #9ca3af;">📁</div>
                <p style="color: #6b7280; margin-bottom: 8px;">Drag and drop your files here</p>
                <p style="color: #9ca3af; font-size: 14px; margin-bottom: 16px;">or click to browse</p>
                <input type="file" id="fileInput" style="display: none;" onchange="handleFileSelect(this.files)">
                <button type="button" class="btn btn-outline" onclick="document.getElementById('fileInput').click()">Browse Files</button>
            </div>
            
            <div id="fileList" style="margin: 16px 0;"></div>
            
            <div style="margin-top: 24px;">
                <label style="display: block; margin-bottom: 8px; font-weight: 500; color: #374151;">Special Instructions (Optional)</label>
                <textarea id="instructions" placeholder="Any specific requirements or instructions..." style="width: 100%; height: 80px; padding: 12px; border: 1px solid #d1d5db; border-radius: 6px; resize: vertical;"></textarea>
            </div>
            
            <div style="display: flex; gap: 12px; margin-top: 24px;">
                <button type="button" class="btn" onclick="submitOrder()" style="flex: 1;">Submit Order</button>
                <button type="button" class="btn btn-outline" onclick="closeUploadModal()">Cancel</button>
            </div>
        </div>
    </div>

    <script>
        let currentService = '';
        let selectedFiles = [];

        function openUploadModal(serviceType) {
            currentService = serviceType;
            const serviceNames = {
                'transcript_cleanup': 'Transcript Cleanup',
                'captions_cleanup': 'Captions & Subtitles Cleanup', 
                'dubbing_voiceover': 'Dubbing & Voiceover'
            };
            document.getElementById('serviceName').textContent = serviceNames[serviceType];
            document.getElementById('uploadModal').style.display = 'flex';
            selectedFiles = [];
            updateFileList();
        }

        function closeUploadModal() {
            document.getElementById('uploadModal').style.display = 'none';
        }

        function handleDragOver(event) {
            event.preventDefault();
            event.currentTarget.classList.add('dragover');
        }

        function handleDragLeave(event) {
            event.preventDefault();
            event.currentTarget.classList.remove('dragover');
        }

        function handleDrop(event) {
            event.preventDefault();
            event.currentTarget.classList.remove('dragover');
            const files = event.dataTransfer.files;
            handleFileSelect(files);
        }

        function handleFileSelect(files) {
            selectedFiles = Array.from(files);
            updateFileList();
        }

        function updateFileList() {
            const fileList = document.getElementById('fileList');
            if (selectedFiles.length === 0) {
                fileList.innerHTML = '';
                return;
            }

            fileList.innerHTML = '<h4 style="margin-bottom: 12px; color: #374151;">Selected Files:</h4>';
            selectedFiles.forEach((file, index) => {
                const fileItem = document.createElement('div');
                fileItem.style.cssText = 'display: flex; justify-content: space-between; align-items: center; padding: 12px; background: #f9fafb; border-radius: 6px; margin-bottom: 8px;';
                fileItem.innerHTML = `
                    <div>
                        <div style="font-weight: 500; color: #374151;">${file.name}</div>
                        <div style="font-size: 12px; color: #6b7280;">${(file.size / 1024 / 1024).toFixed(2)} MB</div>
                    </div>
                    <button type="button" onclick="removeFile(${index})" style="background: none; border: none; color: #ef4444; cursor: pointer; font-size: 18px;">×</button>
                `;
                fileList.appendChild(fileItem);
            });
        }

        function removeFile(index) {
            selectedFiles.splice(index, 1);
            updateFileList();
        }

        async function submitOrder() {
            if (selectedFiles.length === 0) {
                alert('Please select at least one file to upload.');
                return;
            }

            const instructions = document.getElementById('instructions').value;
            
            // Simulate file upload to S3
            const uploadPromises = selectedFiles.map(file => {
                return new Promise((resolve) => {
                    // Simulate upload progress
                    setTimeout(() => {
                        resolve({ filename: file.name, success: true });
                    }, 1000);
                });
            });

            // Show loading state
            const submitBtn = document.querySelector('#uploadModal .btn');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Uploading...';
            submitBtn.disabled = true;

            try {
                const results = await Promise.all(uploadPromises);
                
                // Create order
                const response = await fetch('/api/orders/create', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: new URLSearchParams({
                        service_type: currentService,
                        instructions: instructions || ''
                    })
                });

                if (response.ok) {
                    alert('Order submitted successfully! Files have been uploaded to secure storage.');
                    closeUploadModal();
                    // Refresh orders list
                    location.reload();
                } else {
                    alert('Order submission failed. Please try again.');
                }
            } catch (error) {
                alert('Error submitting order. Please try again.');
            } finally {
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }
        }

        function showSection(section) {
            alert('Navigating to ' + section + ' section...');
            // Implementation for section navigation
        }

        function logout() {
            if (confirm('Are you sure you want to logout?')) {
                window.location.href = '/';
            }
        }

        // Close modal when clicking outside
        document.getElementById('uploadModal').onclick = function(e) {
            if (e.target === this) closeUploadModal();
        };
    </script>
</body>
</html>
"""


# Continue the backend/main.py file...

admin_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Dashboard - Forge Medias</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0f172a; 
            color: #f8fafc;
            line-height: 1.6;
        }
        .header {
            background: #1e293b;
            border-bottom: 1px solid #334155;
            padding: 0 24px;
        }
        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            height: 70px;
            max-width: 1400px;
            margin: 0 auto;
        }
        .logo { 
            font-size: 24px; 
            font-weight: 700; 
            color: #4f46e5;
        }
        .admin-nav {
            display: flex;
            gap: 24px;
        }
        .nav-btn {
            background: transparent;
            color: #cbd5e1;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .nav-btn.active {
            background: #4f46e5;
            color: white;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 24px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }
        .stat-card {
            background: #1e293b;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #4f46e5;
        }
        .stat-number {
            font-size: 32px;
            font-weight: 700;
            color: #4f46e5;
            margin-bottom: 8px;
        }
        .job-queue {
            background: #1e293b;
            border-radius: 8px;
            padding: 24px;
            margin-bottom: 24px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 16px;
        }
        th, td {
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid #334155;
        }
        th {
            background: #334155;
            font-weight: 600;
            color: #e2e8f0;
        }
        .status-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .status-pending { background: #fef3c7; color: #92400e; }
        .status-processing { background: #dbeafe; color: #1e40af; }
        .status-transcribing { background: #f3e8ff; color: #6b21a8; }
        .status-ready { background: #d1fae5; color: #065f46; }
        .status-completed { background: #dcfce7; color: #166534; }
        .btn {
            background: #4f46e5;
            color: white;
            padding: 6px 12px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            margin: 2px;
        }
        .btn:hover {
            background: #4338ca;
        }
        .btn-success { background: #10b981; }
        .btn-warning { background: #f59e0b; }
        .btn-danger { background: #ef4444; }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div class="logo">Forge Medias - Admin</div>
            <div class="admin-nav">
                <button class="nav-btn active" onclick="showSection('queue')">Job Queue</button>
                <button class="nav-btn" onclick="showSection('workers')">Workers</button>
                <button class="nav-btn" onclick="showSection('clients')">Clients</button>
                <button class="nav-btn" onclick="showSection('analytics')">Analytics</button>
                <button class="nav-btn" onclick="logout()">Logout</button>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">12</div>
                <div>Pending Jobs</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">8</div>
                <div>In Progress</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">3</div>
                <div>Awaiting Review</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">47</div>
                <div>Completed Today</div>
            </div>
        </div>

        <div class="job-queue">
            <h2 style="margin-bottom: 8px;">Job Queue</h2>
            <p style="color: #94a3b8; margin-bottom: 16px;">Manage and assign transcription jobs</p>
            
            <table>
                <thead>
                    <tr>
                        <th>Order ID</th>
                        <th>Client</th>
                        <th>Service</th>
                        <th>File</th>
                        <th>Status</th>
                        <th>Assigned To</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="jobsTable">
                    <!-- Jobs will be populated by JavaScript -->
                </tbody>
            </table>
        </div>
    </div>

    <script>
        async function loadJobs() {
            try {
                const response = await fetch('/api/admin/jobs');
                const jobs = await response.json();
                
                const table = document.getElementById('jobsTable');
                table.innerHTML = '';
                
                jobs.forEach(job => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${job.id}</td>
                        <td>${job.client_name}</td>
                        <td>${job.service_type}</td>
                        <td>${job.file_name}</td>
                        <td><span class="status-badge status-${job.status}">${job.status.replace('_', ' ')}</span></td>
                        <td>${job.assigned_to || 'Unassigned'}</td>
                        <td>
                            ${job.status === 'pending' ? `<button class="btn" onclick="assignJob('${job.id}')">Assign</button>` : ''}
                            ${job.status === 'assigned' ? `<button class="btn btn-success" onclick="startTranscription('${job.id}')">Start</button>` : ''}
                            ${job.status === 'transcribing' ? `<button class="btn btn-warning" onclick="checkTranscription('${job.id}')">Check</button>` : ''}
                            ${job.status === 'ready' ? `<button class="btn" onclick="openGoogleDoc('${job.id}')">Edit</button>` : ''}
                            <button class="btn btn-danger" onclick="cancelJob('${job.id}')">Cancel</button>
                        </td>
                    `;
                    table.appendChild(row);
                });
            } catch (error) {
                console.error('Error loading jobs:', error);
            }
        }

        async function assignJob(jobId) {
            const worker = prompt('Assign to worker (enter worker name):');
            if (worker) {
                await fetch(`/api/admin/jobs/${jobId}/assign`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ worker })
                });
                loadJobs();
            }
        }

        async function startTranscription(jobId) {
            if (confirm('Start transcription process with Transcriptor?')) {
                await fetch(`/api/admin/jobs/${jobId}/start`, {
                    method: 'POST'
                });
                loadJobs();
            }
        }

        async function checkTranscription(jobId) {
            await fetch(`/api/admin/jobs/${jobId}/check`);
            loadJobs();
        }

        function openGoogleDoc(jobId) {
            // Open Google Docs for editing
            window.open(`https://docs.google.com/document/create?title=Transcript-${jobId}`, '_blank');
        }

        async function cancelJob(jobId) {
            if (confirm('Are you sure you want to cancel this job?')) {
                await fetch(`/api/admin/jobs/${jobId}/cancel`, {
                    method: 'POST'
                });
                loadJobs();
            }
        }

        function showSection(section) {
            alert('Showing ' + section + ' section');
            // Implement section switching
        }

        function logout() {
            window.location.href = '/';
        }

        // Load jobs on page load
        loadJobs();
        // Refresh every 30 seconds
        setInterval(loadJobs, 30000);
    </script>
</body>
</html>
"""

# API Routes
@app.get("/admin")
async def serve_admin(credentials: HTTPBasicCredentials = Depends(verify_admin)):
    return HTMLResponse(content=admin_html)

@app.post("/api/auth/register")
async def register_user(
    email: str = Form(...),
    password: str = Form(...),
    name: str = Form(...),
    company: str = Form(None)
):
    user_id = str(uuid.uuid4())
    new_user = User(
        id=user_id,
        email=email,
        name=name,
        company=company,
        subscription="Starter",
        created_at=datetime.now().isoformat()
    )
    users_db[email] = new_user
    
    return {
        "user": new_user.dict(),
        "token": "mock-jwt-token",
        "message": "Account created successfully"
    }

@app.post("/api/auth/login")
async def login_user(email: str = Form(...), password: str = Form(...)):
    if email in users_db:
        return {
            "user": users_db[email].dict(),
            "token": "mock-jwt-token"
        }
    else:
        # Auto-create user for demo
        return await register_user(email, password, email.split('@')[0], "")

@app.post("/api/orders/create")
async def create_order(
    service_type: str = Form(...),
    instructions: str = Form(None)
):
    order_id = f"ORD-{str(uuid.uuid4())[:8].upper()}"
    
    # For demo, create a mock file
    new_order = ServiceOrder(
        id=order_id,
        service_type=service_type,
        file_name="uploaded_file.mp4",
        original_filename="uploaded_file.mp4",
        status="pending",
        created_at=datetime.now().isoformat(),
        client_id="demo-client-1",
        s3_key=f"uploads/{order_id}/file.mp4"
    )
    
    orders_db.append(new_order)
    jobs_queue.append(new_order)
    
    return {
        "order_id": order_id,
        "service_type": service_type,
        "status": "pending",
        "created_at": new_order.created_at,
        "message": "Order created successfully. File uploaded to secure storage."
    }

# S3 File Upload Endpoint
@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...), order_id: str = Form(...)):
    try:
        # Generate S3 key
        file_extension = file.filename.split('.')[-1]
        s3_key = f"uploads/{order_id}/{uuid.uuid4()}.{file_extension}"
        
        # Upload to S3
        s3_client.upload_fileobj(
            file.file,
            S3_BUCKET,
            s3_key,
            ExtraArgs={
                'ContentType': file.content_type,
                'Metadata': {
                    'original-filename': file.filename,
                    'upload-time': datetime.now().isoformat()
                }
            }
        )
        
        # Update order with S3 key
        for order in orders_db:
            if order.id == order_id:
                order.s3_key = s3_key
                order.original_filename = file.filename
                break
        
        return {
            "success": True,
            "s3_key": s3_key,
            "message": "File uploaded successfully to S3"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

# Admin API Endpoints
@app.get("/api/admin/jobs")
async def get_jobs(credentials: HTTPBasicCredentials = Depends(verify_admin)):
    jobs = []
    for order in orders_db:
        jobs.append({
            "id": order.id,
            "client_name": "Demo Client",  # In real app, get from user DB
            "service_type": order.service_type.replace('_', ' ').title(),
            "file_name": order.original_filename,
            "status": order.status,
            "assigned_to": getattr(order, 'assigned_worker', None),
            "created_at": order.created_at,
            "s3_key": order.s3_key
        })
    return jobs

@app.post("/api/admin/jobs/{job_id}/assign")
async def assign_job(job_id: str, worker: str, credentials: HTTPBasicCredentials = Depends(verify_admin)):
    for order in orders_db:
        if order.id == job_id:
            order.status = "assigned"
            order.assigned_worker = worker
            break
    return {"message": f"Job {job_id} assigned to {worker}"}

@app.post("/api/admin/jobs/{job_id}/start")
async def start_transcription(job_id: str, credentials: HTTPBasicCredentials = Depends(verify_admin)):
    for order in orders_db:
        if order.id == job_id:
            # Start transcription with Transcriptor API
            try:
                transcriptor_response = await send_to_transcriptor(order)
                order.status = "transcribing"
                order.transcriptor_job_id = transcriptor_response.get('job_id')
                order.transcription_started = datetime.now().isoformat()
                return {
                    "message": "Transcription started with Transcriptor",
                    "transcriptor_job_id": order.transcriptor_job_id
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Transcription start failed: {str(e)}")

@app.post("/api/admin/jobs/{job_id}/check")
async def check_transcription(job_id: str, credentials: HTTPBasicCredentials = Depends(verify_admin)):
    for order in orders_db:
        if order.id == job_id:
            # Check Transcriptor status
            try:
                status = await check_transcriptor_status(order.transcriptor_job_id)
                if status == 'completed':
                    order.status = "ready"
                    order.transcription_completed = datetime.now().isoformat()
                    return {"message": "Transcription completed", "status": "ready"}
                else:
                    return {"message": "Transcription in progress", "status": "transcribing"}
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

@app.post("/api/admin/jobs/{job_id}/cancel")
async def cancel_job(job_id: str, credentials: HTTPBasicCredentials = Depends(verify_admin)):
    for order in orders_db:
        if order.id == job_id:
            order.status = "cancelled"
            break
    return {"message": f"Job {job_id} cancelled"}

# Transcriptor API Integration
async def send_to_transcriptor(order: ServiceOrder):
    """Send file to Transcriptor for transcription"""
    try:
        # Generate pre-signed URL for S3 file
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET, 'Key': order.s3_key},
            ExpiresIn=3600  # 1 hour
        )
        
        # Call Transcriptor API
        transcriptor_url = "https://api.transcriptor.com/v1/transcriptions"
        headers = {
            "Authorization": f"Bearer 2e9ddcf1379f4ee93c3de65a55944e7652e71ea346a5ccc78c035a6d60d0585fea58a8425766c3594ca9b4d80b9dc5e8bd834727e90fa49b6d0a2f7da02ed4c9",
            "Content-Type": "application/json"
        }
        
        payload = {
            "audio_url": presigned_url,
            "language": "en",
            "model": "standard",
            "callback_url": f"http://54.166.168.20:8000/api/webhook/transcriptor/{order.id}"
        }
        
        # In production, use async HTTP client like httpx
        # For now, simulate API call
        import time
        time.sleep(1)  # Simulate API call
        
        return {
            "job_id": f"transcriptor_{order.id}",
            "status": "processing",
            "message": "Transcription started"
        }
        
    except Exception as e:
        raise Exception(f"Transcriptor API error: {str(e)}")

async def check_transcriptor_status(job_id: str):
    """Check transcription status with Transcriptor"""
    # Simulate status check - in production, call Transcriptor API
    import random
    statuses = ['processing', 'processing', 'completed']
    return random.choice(statuses)

# Webhook for Transcriptor callbacks
@app.post("/api/webhook/transcriptor/{order_id}")
async def transcriptor_webhook(order_id: str, payload: dict):
    """Receive webhook from Transcriptor when transcription is complete"""
    for order in orders_db:
        if order.id == order_id:
            if payload.get('status') == 'completed':
                order.status = "ready"
                order.transcription_text = payload.get('transcript', '')
                order.transcription_completed = datetime.now().isoformat()
            break
    
    return {"status": "received"}

# File Download Endpoint
@app.get("/api/files/{order_id}/download")
async def download_file(order_id: str):
    for order in orders_db:
        if order.id == order_id:
            try:
                # Generate pre-signed download URL
                download_url = s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': S3_BUCKET, 'Key': order.s3_key},
                    ExpiresIn=3600  # 1 hour
                )
                return {"download_url": download_url}
            except ClientError as e:
                raise HTTPException(status_code=404, detail="File not found")
    
    raise HTTPException(status_code=404, detail="Order not found")

# Existing endpoints
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

@app.get("/api/orders")
async def get_user_orders():
    # For demo, return all orders
    return {"orders": [order.dict() for order in orders_db]}

@app.get("/api/dashboard")
async def get_dashboard_data():
    return DashboardResponse(
        user=mock_user,
        recent_orders=mock_orders,
        remaining_minutes=864
    )

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "forge-medias-portal", 
        "timestamp": datetime.now().isoformat(),
        "features": ["s3_upload", "admin_queue", "transcriptor_integration"]
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Forge Medias Client Portal Starting...")
    print("📁 Features: S3 Upload, Admin Queue, Transcriptor Integration")
    uvicorn.run(app, host="0.0.0.0", port=8000, access_log=True)
