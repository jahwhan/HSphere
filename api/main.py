from fastapi import FastAPI

# Wir importieren hier direkt die APIRouter-Instanzen
from api.endpoints.clients import router as clients_router
from api.endpoints.availability import router as availability_router
from api.endpoints.booking import router as booking_router
from api.endpoints.services import router as services_router

app = FastAPI(title="HSphere Salon API")

@app.get("/", tags=["root"])
def read_root():
    return {"message": "Hello World"}

@app.get("/test", tags=["root"])
def test():
    return {"status": "API works!"}

# Router registrieren
app.include_router(clients_router, prefix="/clients", tags=["clients"])
app.include_router(availability_router, prefix="/availability", tags=["availability"])
app.include_router(booking_router, prefix="", tags=["booking"])
app.include_router(services_router, prefix="", tags=["services"])