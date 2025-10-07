from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from datetime import datetime
import os

# Import routes
from backend.routes import auth, files, services, admin

app = FastAPI(title="Forge Medias Client Portal", version="1.0.0")

# Include routers
app.include_router(auth.router)
app.include_router(files.router)
app.include_router(services.router)
app.include_router(admin.router)

@app.get("/")
async def root():
    return {"message": "Forge Medias API", "status": "running", "timestamp": datetime.now().isoformat()}

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "forge-medias-portal",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Forge Medias Modular Portal Starting...")
    print("📁 Features: File Upload/Download, S3 Integration, Admin Panel")
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Serve test interface
@app.get("/test")
async def serve_test_interface():
    with open("frontend/test_interface.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

# Serve upload component
@app.get("/upload-component")
async def serve_upload_component():
    with open("frontend/components/upload.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

# Serve test interface
@app.get("/test")
async def serve_test_interface():
    with open("frontend/test_interface.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

# Serve upload component
@app.get("/upload-component")
async def serve_upload_component():
    with open("frontend/components/upload.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)
