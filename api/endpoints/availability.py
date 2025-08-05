from fastapi import APIRouter, Query
from api.services.phorest_api_client import get_available_slots

router = APIRouter()

@router.get("/")
async def check_availability(
    staff_id: str = Query(..., description="Staff member ID"),
    service_id: str = Query(..., description="Service ID"),
    date: str = Query(..., description="Date in YYYY-MM-DD format")
):
    """Check available time slots"""
    return get_available_slots(staff_id, service_id, date)