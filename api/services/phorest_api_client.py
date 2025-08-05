"""
Phorest API Client Module
Provides integration with Phorest API for salon management operations.
Supports both real API calls and fake mode for testing.
"""

import os
import json
import random
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import asyncio
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Load configuration from environment variables
USE_FAKE_API = os.getenv("USE_FAKE_API", "true").lower() == "true"
PHOREST_API_BASE_URL = os.getenv("PHOREST_API_BASE_URL", "https://api.phorest.com/v1")
PHOREST_API_KEY = os.getenv("PHOREST_API_KEY", "your-api-key-here")
PHOREST_BUSINESS_ID = os.getenv("PHOREST_BUSINESS_ID", "your-business-id-here")

# Headers for API requests
HEADERS = {
    "Authorization": f"Bearer {PHOREST_API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Fake data for testing
FAKE_SERVICES = [
    {"id": "srv_001", "name": "Haarschnitt", "duration": 30, "price": 45.00},
    {"id": "srv_002", "name": "Färben", "duration": 90, "price": 120.00},
    {"id": "srv_003", "name": "Styling", "duration": 45, "price": 60.00}
]

FAKE_STAFF = [
    {"id": "stf_001", "name": "Maria Schmidt", "email": "maria@salon.com", "specialties": ["Haarschnitt", "Styling"]},
    {"id": "stf_002", "name": "Anna Weber", "email": "anna@salon.com", "specialties": ["Färben", "Haarschnitt"]},
    {"id": "stf_003", "name": "Sophie Müller", "email": "sophie@salon.com", "specialties": ["Styling", "Färben"]}
]

FAKE_CLIENT_NAMES = [
    "Pascal Erni", "Max Mustermann", "Erika Musterfrau", "Hans Meyer", 
    "Lisa Schmidt", "Thomas Weber", "Julia Fischer", "Michael Wagner", 
    "Sarah Becker", "Klaus Hoffmann", "Anna Schulz"
]


async def get_services() -> Dict:
    """
    Fetch available services from Phorest API or return fake data.
    
    Returns:
        Dict: Response containing success status, data, and message
    """
    try:
        if USE_FAKE_API:
            logger.info("Using fake API for get_services")
            return {
                "success": True,
                "data": {"services": FAKE_SERVICES},
                "message": "Services retrieved successfully (fake mode)"
            }
        
        # Real API call
        url = f"{PHOREST_API_BASE_URL}/business/{PHOREST_BUSINESS_ID}/services"
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "data": {"services": data.get("services", [])},
                "message": "Services retrieved successfully"
            }
        else:
            return {
                "success": False,
                "message": f"Failed to fetch services: HTTP {response.status_code}",
                "data": None
            }
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching services: {str(e)}")
        return {
            "success": False,
            "message": f"Network error while fetching services: {str(e)}",
            "data": None
        }
    except Exception as e:
        logger.error(f"Unexpected error in get_services: {str(e)}")
        return {
            "success": False,
            "message": f"Unexpected error: {str(e)}",
            "data": None
        }


async def get_staff() -> Dict:
    """
    Fetch staff members from Phorest API or return fake data.
    
    Returns:
        Dict: Response containing success status, data, and message
    """
    try:
        if USE_FAKE_API:
            logger.info("Using fake API for get_staff")
            return {
                "success": True,
                "data": {"staff": FAKE_STAFF},
                "message": "Staff retrieved successfully (fake mode)"
            }
        
        # Real API call
        url = f"{PHOREST_API_BASE_URL}/business/{PHOREST_BUSINESS_ID}/staff"
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "data": {"staff": data.get("staff", [])},
                "message": "Staff retrieved successfully"
            }
        else:
            return {
                "success": False,
                "message": f"Failed to fetch staff: HTTP {response.status_code}",
                "data": None
            }
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching staff: {str(e)}")
        return {
            "success": False,
            "message": f"Network error while fetching staff: {str(e)}",
            "data": None
        }
    except Exception as e:
        logger.error(f"Unexpected error in get_staff: {str(e)}")
        return {
            "success": False,
            "message": f"Unexpected error: {str(e)}",
            "data": None
        }


def search_clients(query: str, limit: int = 10) -> Dict:
    """
    Search for clients by name or other criteria.
    
    Args:
        query: Search query string
        limit: Maximum number of results to return
        
    Returns:
        Dict: Response containing success status, data, and message
    """
    try:
        if USE_FAKE_API:
            logger.info(f"Using fake API for search_clients: query='{query}'")
            # Generate fake clients based on query
            fake_clients = []
            
            # Add some test clients that will always match certain names
            test_clients = [
                {"id": "cli_001", "name": "Pascal Erni", "email": "pascal.erni@email.com", "phone": "+49 123 45678"},
                {"id": "cli_002", "name": "Max Mustermann", "email": "max.mustermann@email.com", "phone": "+49 234 56789"},
                {"id": "cli_003", "name": "Erika Musterfrau", "email": "erika.musterfrau@email.com", "phone": "+49 345 67890"},
            ]
            
            # Search in test clients first
            for client in test_clients:
                if query.lower() in client["name"].lower():
                    fake_clients.append(client)
            
            # Then search in random names
            for i, name in enumerate(FAKE_CLIENT_NAMES):
                if query.lower() in name.lower() and len(fake_clients) < limit:
                    fake_clients.append({
                        "id": f"cli_{i+100:03d}",
                        "name": name,
                        "email": f"{name.lower().replace(' ', '.')}@email.com",
                        "phone": f"+49 {random.randint(100, 999)} {random.randint(10000, 99999)}"
                    })
            
            return {
                "success": True,
                "data": {"clients": fake_clients[:limit]},
                "message": f"Found {len(fake_clients)} clients (fake mode)"
            }
        
        # Real API call
        url = f"{PHOREST_API_BASE_URL}/business/{PHOREST_BUSINESS_ID}/clients/search"
        params = {"query": query, "limit": limit}
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "data": {"clients": data.get("clients", [])},
                "message": f"Found {len(data.get('clients', []))} clients"
            }
        else:
            return {
                "success": False,
                "message": f"Failed to search clients: HTTP {response.status_code}",
                "data": None
            }
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error searching clients: {str(e)}")
        return {
            "success": False,
            "message": f"Network error while searching clients: {str(e)}",
            "data": None
        }
    except Exception as e:
        logger.error(f"Unexpected error in search_clients: {str(e)}")
        return {
            "success": False,
            "message": f"Unexpected error: {str(e)}",
            "data": None
        }


def get_client(client_id: str) -> Dict:
    """
    Fetch a specific client by ID.
    
    Args:
        client_id: The client's unique identifier
        
    Returns:
        Dict: Response containing success status, data, and message
    """
    try:
        if USE_FAKE_API:
            logger.info(f"Using fake API for get_client: id='{client_id}'")
            # Generate a fake client
            fake_client = {
                "id": client_id,
                "name": random.choice(FAKE_CLIENT_NAMES),
                "email": f"client.{client_id}@email.com",
                "phone": f"+49 {random.randint(100, 999)} {random.randint(10000, 99999)}",
                "notes": "Preferred appointment times: mornings",
                "created_at": "2024-01-15T10:30:00Z"
            }
            
            return {
                "success": True,
                "data": {"client": fake_client},
                "message": "Client retrieved successfully (fake mode)"
            }
        
        # Real API call
        url = f"{PHOREST_API_BASE_URL}/business/{PHOREST_BUSINESS_ID}/clients/{client_id}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "data": {"client": data},
                "message": "Client retrieved successfully"
            }
        elif response.status_code == 404:
            return {
                "success": False,
                "message": f"Client with ID '{client_id}' not found",
                "data": None
            }
        else:
            return {
                "success": False,
                "message": f"Failed to fetch client: HTTP {response.status_code}",
                "data": None
            }
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching client: {str(e)}")
        return {
            "success": False,
            "message": f"Network error while fetching client: {str(e)}",
            "data": None
        }
    except Exception as e:
        logger.error(f"Unexpected error in get_client: {str(e)}")
        return {
            "success": False,
            "message": f"Unexpected error: {str(e)}",
            "data": None
        }


def get_available_slots(staff_id: str, service_id: str, date: str) -> Dict:
    """
    Get available appointment slots for a specific staff member and service on a given date.
    
    Args:
        staff_id: The staff member's ID
        service_id: The service ID
        date: Date in YYYY-MM-DD format
        
    Returns:
        Dict: Response containing success status, data, and message
    """
    try:
        if USE_FAKE_API:
            logger.info(f"Using fake API for get_available_slots: staff={staff_id}, service={service_id}, date={date}")
            
            # Use a deterministic seed based on the input parameters
            # This ensures the same slots are returned for the same query
            seed_string = f"{staff_id}-{service_id}-{date}"
            seed_value = sum(ord(c) for c in seed_string)
            random.seed(seed_value)
            
            # Generate fake time slots
            base_times = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", 
                         "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", 
                         "16:00", "16:30", "17:00", "17:30"]
            
            # Remove some slots to simulate bookings (but consistently)
            num_available = random.randint(6, 12)
            available_slots = random.sample(base_times, k=num_available)
            available_slots.sort()
            
            # Reset random seed to avoid affecting other random operations
            random.seed()
            
            return {
                "success": True,
                "data": {"availableSlots": available_slots},
                "message": f"Found {len(available_slots)} available slots (fake mode)"
            }
            
            return {
                "success": True,
                "data": {"availableSlots": available_slots},
                "message": f"Found {len(available_slots)} available slots (fake mode)"
            }
        
        # Real API call
        url = f"{PHOREST_API_BASE_URL}/business/{PHOREST_BUSINESS_ID}/availability"
        params = {
            "staff_id": staff_id,
            "service_id": service_id,
            "date": date
        }
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            slots = data.get("availableSlots", [])
            return {
                "success": True,
                "data": {"availableSlots": slots},
                "message": f"Found {len(slots)} available slots"
            }
        else:
            return {
                "success": False,
                "message": f"Failed to fetch availability: HTTP {response.status_code}",
                "data": None
            }
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching availability: {str(e)}")
        return {
            "success": False,
            "message": f"Network error while fetching availability: {str(e)}",
            "data": None
        }
    except Exception as e:
        logger.error(f"Unexpected error in get_available_slots: {str(e)}")
        return {
            "success": False,
            "message": f"Unexpected error: {str(e)}",
            "data": None
        }


async def create_appointment(appointment_data: Dict) -> Dict:
    """
    Create a new appointment.
    
    Args:
        appointment_data: Dictionary containing appointment details:
            - clientId: Client ID
            - staffId: Staff member ID
            - serviceId: Service ID
            - startTime: Appointment start time (ISO format)
            
    Returns:
        Dict: Response containing success status, data, and message
    """
    try:
        if USE_FAKE_API:
            logger.info(f"Using fake API for create_appointment: {appointment_data}")
            # Simulate appointment creation
            appointment_id = f"apt_{random.randint(1000, 9999)}"
            fake_appointment = {
                "id": appointment_id,
                "clientId": appointment_data.get("clientId"),
                "staffId": appointment_data.get("staffId"),
                "serviceId": appointment_data.get("serviceId"),
                "startTime": appointment_data.get("startTime"),
                "status": "confirmed",
                "createdAt": datetime.now().isoformat() + "Z"
            }
            
            return {
                "success": True,
                "data": {"appointment": fake_appointment},
                "message": f"Appointment {appointment_id} created successfully (fake mode)"
            }
        
        # Real API call
        url = f"{PHOREST_API_BASE_URL}/business/{PHOREST_BUSINESS_ID}/appointments"
        response = requests.post(url, headers=HEADERS, json=appointment_data, timeout=10)
        
        if response.status_code in [200, 201]:
            data = response.json()
            appointment_id = data.get("id", "unknown")
            return {
                "success": True,
                "data": {"appointment": data},
                "message": f"Appointment {appointment_id} created successfully"
            }
        elif response.status_code == 409:
            return {
                "success": False,
                "message": "Time slot is no longer available",
                "data": None
            }
        else:
            error_msg = response.json().get("message", "Unknown error") if response.text else f"HTTP {response.status_code}"
            return {
                "success": False,
                "message": f"Failed to create appointment: {error_msg}",
                "data": None
            }
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating appointment: {str(e)}")
        return {
            "success": False,
            "message": f"Network error while creating appointment: {str(e)}",
            "data": None
        }
    except Exception as e:
        logger.error(f"Unexpected error in create_appointment: {str(e)}")
        return {
            "success": False,
            "message": f"Unexpected error: {str(e)}",
            "data": None
        }


# Helper function to test the client
async def test_client():
    """Test function to verify the API client is working"""
    print(f"Testing Phorest API Client (Fake Mode: {USE_FAKE_API})")
    
    # Test get_services
    services = await get_services()
    print(f"\nServices: {json.dumps(services, indent=2)}")
    
    # Test get_staff
    staff = await get_staff()
    print(f"\nStaff: {json.dumps(staff, indent=2)}")
    
    # Test search_clients
    clients = search_clients("Max", limit=5)
    print(f"\nClient Search: {json.dumps(clients, indent=2)}")
    
    # Test get_available_slots
    slots = get_available_slots("stf_001", "srv_001", "2025-07-15")
    print(f"\nAvailable Slots: {json.dumps(slots, indent=2)}")


if __name__ == "__main__":
    # Run test if module is executed directly
    asyncio.run(test_client())