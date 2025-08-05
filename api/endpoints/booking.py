from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.services.phorest_api_client import create_appointment

router = APIRouter()

class BookingRequest(BaseModel):
    client_id: str
    stylist_id: str
    datetime_str: str
    service_id: str

@router.post("/book_appointment")
async def make_booking(req: BookingRequest):
    """Book an appointment using the Phorest API"""
    # Transform to Phorest format
    phorest_payload = {
        "clientId": req.client_id,
        "staffId": req.stylist_id,
        "startTime": req.datetime_str,
        "serviceId": req.service_id
    }
    
    # Call Phorest API
    result = await create_appointment(phorest_payload)
    
    # Handle error
    if not result.get("success", False):
        error_message = result.get("message", "Unknown error occurred")
        raise HTTPException(status_code=502, detail=f"Booking failed: {error_message}")
    
    return {
        "success": True,
        "message": result.get("message", "Appointment booked successfully"),
        "data": result.get("data", {})
    }