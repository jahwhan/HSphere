# local_booking.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))  # Zum Root-Verzeichnis
import datetime
from Data.clients_data import clients
from Data.stylists_data import stylists



def extract_booking_request(user_input):
    # Mock parser – später mit echter Intent-Engine ersetzen
    if "book" in user_input or "appointment" in user_input:
        return {
            "intent": "book_appointment",
            "stylist_name": next((s['name'] for s in stylists if s['name'].lower() in user_input.lower()), None),
            "service": "haircut" if "cut" in user_input else "beard" if "beard" in user_input else None,
            "date": extract_date(user_input),
            "time": extract_time(user_input)
        }
    return {"intent": "unknown"}


def extract_date(text):
    today = datetime.date.today()
    if "tomorrow" in text:
        return today + datetime.timedelta(days=1)
    if "today" in text:
        return today
    # Add more parsing rules here
    return None


def extract_time(text):
    if "10" in text:
        return "10:00"
    if "14" in text:
        return "14:00"
    return None


def find_alternative(stylist_name, date):
    for s in stylists:
        if s['name'] != stylist_name:
            if date in s['availability']:
                return s['name'], s['availability'][date][0]  # pick first free slot
    return None, None


def book_appointment(parsed):
    if not all([parsed['stylist_name'], parsed['service'], parsed['date'], parsed['time']]):
        return "Missing details. Please provide stylist, service, date and time."

    stylist = next((s for s in stylists if s['name'] == parsed['stylist_name']), None)
    if stylist and parsed['date'] in stylist['availability']:
        if parsed['time'] in stylist['availability'][parsed['date']]:
            # Confirm booking
            stylist['availability'][parsed['date']].remove(parsed['time'])
            return f"Appointment booked with {stylist['name']} on {parsed['date']} at {parsed['time']}."
        else:
            alt_time = stylist['availability'][parsed['date']][0] if stylist['availability'][parsed['date']] else None
            if alt_time:
                return f"{stylist['name']} is not free at that time. Available at {alt_time} instead."
            else:
                # Try finding another stylist
                alt_name, alt_time = find_alternative(stylist['name'], parsed['date'])
                if alt_name and alt_time:
                    return f"{stylist['name']} not available. But {alt_name} is free at {alt_time}. Shall I book?"
                else:
                    return "No stylist available at that time. Try another day."
    return "Stylist not found or not available that day."


def handle_user_input(user_input):
    parsed = extract_booking_request(user_input)
    if parsed['intent'] == "book_appointment":
        return book_appointment(parsed)
    return "Sorry, I didn't understand your request."


# TEST
if __name__ == "__main__":
    example_input = "I want to book a haircut with Elijah tomorrow at 14"
    print(handle_user_input(example_input))
