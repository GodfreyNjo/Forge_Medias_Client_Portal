from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class User(BaseModel):
    id: str
    email: str
    name: str
    company: Optional[str] = None
    subscription: str = "Starter"
    created_at: str
    is_admin: bool = False

    @classmethod
    def create(cls, email: str, name: str, company: str = None):
        return cls(
            id=str(uuid.uuid4()),
            email=email,
            name=name,
            company=company,
            subscription="Starter",
            created_at=datetime.now().isoformat(),
            is_admin=False
        )
