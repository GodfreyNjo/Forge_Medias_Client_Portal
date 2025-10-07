from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class ServiceOrder(BaseModel):
    id: str
    service_type: str
    file_name: str
    original_filename: str
    status: str
    created_at: str
    client_id: str
    s3_key: Optional[str] = None
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    instructions: Optional[str] = None

    @classmethod
    def create(cls, service_type: str, client_id: str, filename: str):
        return cls(
            id=f"ORD-{str(uuid.uuid4())[:8].upper()}",
            service_type=service_type,
            file_name=filename,
            original_filename=filename,
            status="pending",
            created_at=datetime.now().isoformat(),
            client_id=client_id
        )
