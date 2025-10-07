from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from backend.models.order import ServiceOrder
from backend.utils.s3_upload import upload_file_to_s3, generate_download_url
import backend.models.service as service_models

router = APIRouter(prefix="/api/files", tags=["files"])

# In-memory storage for orders (replace with database)
orders_db = []

@router.post("/upload")
async def upload_file(
    service_type: str = Form(...),
    file: UploadFile = File(...),
    instructions: str = Form(None)
):
    # Validate service type
    if service_type not in service_models.SERVICES:
        raise HTTPException(status_code=400, detail="Invalid service type")
    
    # Validate file type
    file_extension = file.filename.split('.')[-1].lower()
    service = service_models.SERVICES[service_type]
    
    if f".{file_extension}" not in service.supported_formats:
        raise HTTPException(
            status_code=400, 
            detail=f"File type .{file_extension} not supported for {service.name}"
        )
    
    # Create order
    new_order = ServiceOrder.create(service_type, "demo-client-1", file.filename)
    
    try:
        # Upload to S3
        upload_result = await upload_file_to_s3(file, new_order.id, file.filename)
        
        # Update order with S3 info
        new_order.s3_key = upload_result["s3_key"]
        new_order.file_size = upload_result["file_size"]
        new_order.file_type = upload_result["file_type"]
        new_order.instructions = instructions
        
        orders_db.append(new_order)
        
        return {
            "order_id": new_order.id,
            "service_type": service_type,
            "file_name": file.filename,
            "file_size": upload_result["file_size"],
            "status": "pending",
            "message": "File uploaded successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/download/{order_id}")
async def download_file(order_id: str):
    # Find order
    order = next((o for o in orders_db if o.id == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if not order.s3_key:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Generate download URL
    download_url = generate_download_url(order.s3_key)
    if not download_url:
        raise HTTPException(status_code=500, detail="Failed to generate download URL")
    
    return {
        "download_url": download_url,
        "file_name": order.original_filename,
        "expires_in": "1 hour"
    }

@router.get("/orders")
async def get_user_orders():
    return {"orders": [order.dict() for order in orders_db]}
