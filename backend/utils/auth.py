from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import HTTPException
import secrets

security = HTTPBasic()

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "forge2024"

def verify_admin(credentials: HTTPBasicCredentials):
    """Verify admin credentials"""
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect admin credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
