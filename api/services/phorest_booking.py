# Agents/phorest_booking.py

"""
Wrapper-Funktionen zur Buchung von Terminen über die Phorest API
— unterstützt echten und Fake-Modus über phorest_api.py
"""

from Agents.phorest_api import (
    get_client,
    search_clients,
    get_client_appointments,
    create_appointment,
    get_available_slots
)

def book_appointment(client_id: str, stylist_id: str, datetime_str: str, service_id: str):
    """
    Führt Buchung über die Phorest API durch, mit vorheriger Verfügbarkeitsprüfung.
    :param client_id: ID des Kunden
    :param stylist_id: ID des Stylists
    :param datetime_str: ISO-Format (z. B. '2025-06-22T15:00:00')
    :param service_id: ID der Dienstleistung
    :return: Erfolgs- oder Fehler-Response (dict)
    """
    # Verfügbare Slots abrufen
    availability = get_available_slots(stylist_id, service_id, datetime_str[:10])
    
    if not availability.get("success"):
        return {
            "success": False,
            "message": "Fehler bei der Verfügbarkeitsabfrage."
        }
    
    slots = availability["data"].get("availableSlots", [])
    time_part = datetime_str[11:16]  # Uhrzeit extrahieren
    
    if time_part not in slots:
        return {
            "success": False,
            "message": f"Kein freier Slot um {time_part} Uhr."
        }

    # Termin erstellen
    appointment_data = {
        "clientId": client_id,
        "staffId": stylist_id,
        "serviceId": service_id,
        "startTime": datetime_str,
        "notes": "Gebucht via HOAI"
    }

    result = create_appointment(appointment_data)
    return result
