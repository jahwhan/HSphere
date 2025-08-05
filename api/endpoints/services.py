from fastapi import APIRouter
from api.services.phorest_api_client import get_services

router = APIRouter()

@router.get("/services")
async def get_services_endpoint():
    """Get all available services"""
    return await get_services()

@router.get("/staff")
async def get_staff_endpoint():
    """Get all staff members"""
    from api.services.phorest_api_client import get_staff
    return await get_staff()