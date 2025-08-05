from fastapi import APIRouter, HTTPException, Query
from api.services.phorest_api_client import search_clients, get_client

router = APIRouter(tags=["clients"])

@router.get("/search")
def clients_search(query: str = Query(..., description="Suchbegriff für Name, Telefon, Email")):
    """GET /clients/search?query=..."""
    result = search_clients(query)
    if not result.get("success"):
        raise HTTPException(502, detail=result.get("message", "Phorest-API Fehler"))
    return result

@router.get("/{client_id}")
def clients_get(client_id: str):
    """GET /clients/{client_id}"""
    result = get_client(client_id)
    if not result.get("success"):
        raise HTTPException(404, detail=result.get("message", "Client nicht gefunden"))
    return result