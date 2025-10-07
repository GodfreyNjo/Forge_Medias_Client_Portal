from fastapi import APIRouter
import backend.models.service as service_models

router = APIRouter(prefix="/api/services", tags=["services"])

@router.get("")
async def get_services():
    services_list = [service.dict() for service in service_models.SERVICES.values()]
    return {"services": services_list}

@router.get("/{service_id}")
async def get_service(service_id: str):
    if service_id not in service_models.SERVICES:
        return {"error": "Service not found"}
    return service_models.SERVICES[service_id].dict()
