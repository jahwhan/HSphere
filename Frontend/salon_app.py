import streamlit as st
import requests
from datetime import datetime, timedelta
import json

# API Base URL
API_BASE_URL = "http://127.0.0.1:8000"

@st.cache_data(show_spinner=False)
def load_services_and_stylists():
    """Load services and staff from API with caching"""
    services = []
    stylists = []
    
    try:
        # Load services
        resp = requests.get(f"{API_BASE_URL}/services", timeout=5)
        resp.raise_for_status()
        services_data = resp.json()
        services = services_data.get("data", {}).get("services", [])
    except Exception as e:
        st.warning(f"Fehler beim Laden der Services: {str(e)}")
    
    try:
        # Load staff
        resp = requests.get(f"{API_BASE_URL}/staff", timeout=5)
        resp.raise_for_status()
        staff_data = resp.json()
        stylists = staff_data.get("data", {}).get("staff", [])
    except Exception as e:
        st.warning(f"Fehler beim Laden der Stylisten: {str(e)}")
    
    return services, stylists

# Load data from API
services, stylists = load_services_and_stylists()

# Create mappings from API data
service_map = {service.get('name', ''): service.get('id', '') for service in services}
stylist_map = {stylist.get('name', ''): stylist.get('id', '') for stylist in stylists}

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'booking_state' not in st.session_state:
    st.session_state.booking_state = {
        'stage': 'name',
        'client_name': None,
        'client_id': None,
        'service': None,
        'service_id': None,
        'stylist': None,
        'stylist_id': None,
        'date': None,
        'time': None
    }

# API Functions
def api_search_client(name):
    """Search for a client by name"""
    try:
        response = requests.get(f"{API_BASE_URL}/clients/search", params={"query": name})
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('data', {}).get('clients'):
                return data['data']['clients']
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"API-Fehler: {str(e)}")
        return None

def api_get_availability(staff_id, service_id, date):
    """Get available time slots"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/availability",
            params={
                "staff_id": staff_id,
                "service_id": service_id,
                "date": date
            }
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('data', {}).get('availableSlots'):
                return data['data']['availableSlots']
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"API-Fehler: {str(e)}")
        return None

def process_chat_input(user_input):
    """Process user input based on current booking stage"""
    state = st.session_state.booking_state
    
    if state['stage'] == 'name':
        # Search for client
        clients = api_search_client(user_input)
        
        if clients and len(clients) > 0:
            # Take the first matching client
            client = clients[0]
            state['client_name'] = client.get('name', user_input)
            state['client_id'] = client.get('id')
            state['stage'] = 'service'
            
            service_list = "\n".join([f"- {service.get('name', '')}" for service in services])
            return f"Hallo {state['client_name']}! Welchen Service möchten Sie buchen?\n\n" + \
                   f"Verfügbare Services:\n{service_list}"
        else:
            return f"Entschuldigung, ich konnte keinen Kunden mit dem Namen '{user_input}' finden. " + \
                   "Bitte versuchen Sie es erneut oder wenden Sie sich an die Rezeption."
    
    elif state['stage'] == 'service':
        # Check if service exists
        service_name = None
        for service in services:
            if service.get('name', '').lower() in user_input.lower():
                service_name = service.get('name')
                state['service'] = service_name
                state['service_id'] = service.get('id')
                break
        
        if service_name:
            state['stage'] = 'stylist'
            stylist_list = "\n".join([f"- {stylist.get('name', '')}" for stylist in stylists])
            return f"Perfekt! Sie möchten einen Termin für {service_name}.\n\n" + \
                   f"Bei welchem Stylisten möchten Sie buchen?\n{stylist_list}"
        else:
            service_list = "\n".join([f"- {service.get('name', '')}" for service in services])
            return f"Dieser Service ist nicht verfügbar. Bitte wählen Sie aus:\n{service_list}"
    
    elif state['stage'] == 'stylist':
        # Check if stylist exists
        stylist_name = None
        for stylist in stylists:
            if stylist.get('name', '').lower() in user_input.lower():
                stylist_name = stylist.get('name')
                state['stylist'] = stylist_name
                state['stylist_id'] = stylist.get('id')
                break
        
        if stylist_name:
            state['stage'] = 'date'
            # Show next 7 days starting from today
            today = datetime.now()
            dates = []
            for i in range(7):
                date = (today + timedelta(days=i)).strftime('%Y-%m-%d')
                dates.append(date)
            
            return f"Ausgezeichnet! {stylist_name} freut sich auf Sie.\n\n" + \
                   "An welchem Tag möchten Sie kommen?\n" + \
                   "\n".join([f"- {date}" for date in dates])
        else:
            stylist_list = "\n".join([f"- {stylist.get('name', '')}" for stylist in stylists])
            return f"Dieser Stylist ist nicht verfügbar. Bitte wählen Sie:\n{stylist_list}"
    
    elif state['stage'] == 'date':
        # Validate date format
        try:
            date_obj = datetime.strptime(user_input, '%Y-%m-%d')
            state['date'] = user_input
            
            # Get available slots from API
            slots = api_get_availability(
                state['stylist_id'],
                state['service_id'],
                state['date']
            )
            
            if slots:
                state['stage'] = 'time'
                return f"Verfügbare Zeiten am {state['date']}:\n\n" + \
                       "\n".join([f"- {slot}" for slot in slots])
            else:
                return f"Leider sind am {state['date']} keine Termine verfügbar. " + \
                       "Bitte wählen Sie einen anderen Tag."
        except ValueError:
            return "Bitte geben Sie das Datum im Format YYYY-MM-DD an (z.B. 2024-12-20)."
    
    elif state['stage'] == 'time':
        # Validate time format
        time_input = user_input.strip()
        
        # Get available slots again to validate
        slots = api_get_availability(
            state['stylist_id'],
            state['service_id'],
            state['date']
        )
        
        if slots and time_input in slots:
            state['time'] = time_input
            state['stage'] = 'confirm'
            
            return f"Möchten Sie folgenden Termin buchen?\n\n" + \
                   f"**Service:** {state['service']}\n" + \
                   f"**Stylist:** {state['stylist']}\n" + \
                   f"**Datum:** {state['date']}\n" + \
                   f"**Uhrzeit:** {state['time']}\n\n" + \
                   "Antworten Sie mit 'Ja' zum Bestätigen oder 'Nein' zum Abbrechen."
        else:
            # Don't show the time they entered, just show available times
            if slots:
                return f"Bitte wählen Sie eine der verfügbaren Zeiten:\n" + \
                       "\n".join([f"- {slot}" for slot in slots])
            else:
                return "Leider sind keine Termine mehr verfügbar. Bitte wählen Sie einen anderen Tag."
    
    elif state['stage'] == 'confirm':
        if 'ja' in user_input.lower():
            # Create proper datetime string (not ISO format with Z)
            datetime_str = f"{state['date']} {state['time']}"
            
            # Prepare payload for booking
            payload = {
                "client_id": state['client_id'],
                "stylist_id": state['stylist_id'],
                "datetime_str": datetime_str,
                "service_id": state['service_id']
            }
            
            try:
                # Make the actual booking request
                resp = requests.post(
                    f"{API_BASE_URL}/book_appointment",
                    json=payload,
                    timeout=10
                )
                resp.raise_for_status()
                result = resp.json()
                
                if result.get('success'):
                    # Show balloons for successful booking
                    st.balloons()
                    
                    # Reset state for next booking
                    st.session_state.booking_state = {
                        'stage': 'name',
                        'client_name': None,
                        'client_id': None,
                        'service': None,
                        'service_id': None,
                        'stylist': None,
                        'stylist_id': None,
                        'date': None,
                        'time': None
                    }
                    
                    return f"✅ Termin erfolgreich gebucht!\n\n" + \
                           f"{result.get('message', 'Ihre Buchung wurde bestätigt.')}\n\n" + \
                           "Vielen Dank! Für eine neue Buchung geben Sie bitte Ihren Namen ein."
                else:
                    error_msg = result.get('message', 'Buchung fehlgeschlagen')
                    return f"❌ Buchung fehlgeschlagen: {error_msg}\n\n" + \
                           "Bitte versuchen Sie es erneut oder wenden Sie sich an die Rezeption."
                           
            except requests.exceptions.HTTPError as e:
                return f"❌ HTTP-Fehler bei der Buchung: {str(e)}\n\n" + \
                       "Bitte versuchen Sie es erneut oder wenden Sie sich an die Rezeption."
            except requests.exceptions.RequestException as e:
                return f"❌ Verbindungsfehler: {str(e)}\n\n" + \
                       "Bitte überprüfen Sie Ihre Internetverbindung."
            except Exception as e:
                return f"❌ Unerwarteter Fehler: {str(e)}\n\n" + \
                       "Bitte versuchen Sie es erneut oder wenden Sie sich an die Rezeption."
        else:
            # Reset state
            st.session_state.booking_state = {
                'stage': 'name',
                'client_name': None,
                'client_id': None,
                'service': None,
                'service_id': None,
                'stylist': None,
                'stylist_id': None,
                'date': None,
                'time': None
            }
            return "Buchung abgebrochen. Wie kann ich Ihnen helfen? Bitte geben Sie Ihren Namen ein."
    
    return "Entschuldigung, ich habe Sie nicht verstanden. Bitte versuchen Sie es erneut."

# Streamlit UI
st.title("🌟 Willkommen zum Salon Elegant")
st.markdown("### Terminbuchung Chat-Assistent")

# API Status Check
with st.sidebar:
    st.header("API Status")
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=2)
        if response.status_code == 200:
            st.success("✅ API verbunden")
        else:
            st.error("❌ API nicht erreichbar")
    except:
        st.error("❌ API nicht erreichbar")
    
    st.divider()
    
    # Show loaded data
    st.subheader("Geladene Daten")
    st.info(f"Services: {len(services)}\nStylisten: {len(stylists)}")
    
    st.divider()
    st.caption("Stellen Sie sicher, dass das Backend läuft:")
    st.code("uvicorn api.main:app --reload", language="bash")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Show initial greeting if no messages
if not st.session_state.messages:
    greeting = "Willkommen beim Salon Elegant! 💇‍♀️\n\nIch helfe Ihnen gerne bei der Terminbuchung. Bitte geben Sie Ihren Namen ein, um zu beginnen."
    st.session_state.messages.append({"role": "assistant", "content": greeting})
    with st.chat_message("assistant"):
        st.markdown(greeting)

# Chat input
if prompt := st.chat_input("Ihre Nachricht..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Process input and get response
    response = process_chat_input(prompt)
    
    # Add assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# Footer
st.divider()
st.caption("Salon Elegant - Ihre Schönheit ist unsere Leidenschaft")