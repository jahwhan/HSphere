import streamlit as st
import requests
from datetime import datetime, timedelta
import json
import time
from typing import Dict, List, Optional
import re

# Page Configuration - Premium Setup
st.set_page_config(
    page_title="hoai.ch | KI Terminbuchung",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# API Configuration
API_BASE_URL = "http://127.0.0.1:8000"

# Premium CSS Styling - hoai.ch Brand
def load_css():
    st.markdown("""
    <style>
        /* Import Premium Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');
        
        /* Root Variables - hoai.ch Brand Colors */
        :root {
            --primary-black: #1a1a1a;
            --accent-gold: #D4AF37;
            --soft-beige: #F5F2ED;
            --warm-gray: #6B6B6B;
            --pure-white: #FFFFFF;
            --shadow-soft: 0 2px 20px rgba(0, 0, 0, 0.08);
            --shadow-hover: 0 8px 32px rgba(0, 0, 0, 0.12);
            --transition-smooth: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        /* Global Styles */
        .stApp {
            background: linear-gradient(180deg, var(--soft-beige) 0%, var(--pure-white) 100%);
            font-family: 'Inter', sans-serif;
        }
        
        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Premium Header */
        .premium-header {
            text-align: center;
            padding: 3rem 2rem;
            margin-bottom: 2rem;
            background: var(--pure-white);
            border-radius: 20px;
            box-shadow: var(--shadow-soft);
            animation: fadeInDown 0.8s ease-out;
        }
        
        .brand-title {
            font-family: 'Playfair Display', serif;
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--primary-black);
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
        }
        
        .brand-subtitle {
            font-size: 1.1rem;
            color: var(--warm-gray);
            font-weight: 300;
            letter-spacing: 0.02em;
        }
        
        /* Chat Container - Premium Style */
        .chat-container {
            max-width: 800px;
            margin: 0 auto;
            background: var(--pure-white);
            border-radius: 24px;
            box-shadow: var(--shadow-soft);
            padding: 2rem;
            min-height: 600px;
            transition: var(--transition-smooth);
            position: relative;
            overflow: hidden;
        }
        
        .chat-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--accent-gold) 0%, var(--primary-black) 100%);
        }
        
        /* Messages - Elegant Styling */
        .stChatMessage {
            padding: 1.2rem;
            margin-bottom: 1rem;
            animation: messageSlideIn 0.4s ease-out;
        }
        
        .stChatMessage[data-testid="user-message"] {
            background: var(--primary-black);
            border-radius: 18px 18px 4px 18px;
            margin-left: 20%;
        }
        
        .stChatMessage[data-testid="assistant-message"] {
            background: var(--soft-beige);
            border-radius: 18px 18px 18px 4px;
            margin-right: 20%;
            border: 1px solid rgba(0, 0, 0, 0.05);
        }
        
        /* Input Field - Premium Style */
        .stChatInput > div {
            border-radius: 50px !important;
            border: 2px solid var(--soft-beige) !important;
            padding: 0.5rem !important;
            transition: var(--transition-smooth);
        }
        
        .stChatInput > div:focus-within {
            border-color: var(--accent-gold) !important;
            box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.1) !important;
        }
        
        /* Buttons - Luxury Style */
        .stButton > button {
            background: var(--primary-black);
            color: var(--pure-white);
            border: none;
            border-radius: 50px;
            padding: 0.8rem 2rem;
            font-weight: 500;
            letter-spacing: 0.02em;
            transition: var(--transition-smooth);
            box-shadow: var(--shadow-soft);
        }
        
        .stButton > button:hover {
            background: var(--accent-gold);
            color: var(--primary-black);
            transform: translateY(-2px);
            box-shadow: var(--shadow-hover);
        }
        
        /* Loading Animation - Premium */
        .loading-dots {
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }
        
        .loading-dots span {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--accent-gold);
            animation: dotPulse 1.4s infinite ease-in-out both;
        }
        
        .loading-dots span:nth-child(1) { animation-delay: -0.32s; }
        .loading-dots span:nth-child(2) { animation-delay: -0.16s; }
        
        /* Status Badge - Elegant */
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 0.5rem 1rem;
            background: var(--soft-beige);
            border-radius: 50px;
            font-size: 0.875rem;
            font-weight: 500;
            color: var(--primary-black);
            border: 1px solid rgba(0, 0, 0, 0.1);
        }
        
        .status-badge.success {
            background: #E8F5E9;
            color: #2E7D32;
            border-color: #4CAF50;
        }
        
        /* Progress Steps - Visual Journey */
        .progress-container {
            display: flex;
            justify-content: space-between;
            margin: 2rem 0;
            position: relative;
        }
        
        .progress-step {
            flex: 1;
            text-align: center;
            position: relative;
            z-index: 1;
        }
        
        .progress-step::before {
            content: '';
            position: absolute;
            top: 20px;
            left: 50%;
            right: -50%;
            height: 2px;
            background: var(--soft-beige);
            z-index: -1;
        }
        
        .progress-step:last-child::before {
            display: none;
        }
        
        .progress-step.active .step-circle {
            background: var(--accent-gold);
            color: var(--primary-black);
            box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.2);
        }
        
        .progress-step.completed .step-circle {
            background: var(--primary-black);
            color: var(--pure-white);
        }
        
        .step-circle {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: var(--soft-beige);
            color: var(--warm-gray);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 0.5rem;
            font-weight: 600;
            transition: var(--transition-smooth);
        }
        
        .step-label {
            font-size: 0.75rem;
            color: var(--warm-gray);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        /* Animations */
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes messageSlideIn {
            from {
                opacity: 0;
                transform: translateX(20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes dotPulse {
            0%, 80%, 100% {
                transform: scale(0);
                opacity: 0.5;
            }
            40% {
                transform: scale(1);
                opacity: 1;
            }
        }
        
        /* Mobile Optimization */
        @media (max-width: 768px) {
            .chat-container {
                margin: 1rem;
                padding: 1.5rem;
                border-radius: 20px;
            }
            
            .brand-title {
                font-size: 2rem;
            }
            
            .stChatMessage[data-testid="user-message"],
            .stChatMessage[data-testid="assistant-message"] {
                margin-left: 0;
                margin-right: 0;
            }
            
            .progress-container {
                flex-wrap: wrap;
                gap: 1rem;
            }
        }
        
        /* Premium Sidebar */
        .css-1d391kg {
            background: var(--primary-black);
            color: var(--pure-white);
        }
        
        /* Success Animation */
        .success-animation {
            animation: successPop 0.6s ease-out;
        }
        
        @keyframes successPop {
            0% { transform: scale(0.8); opacity: 0; }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); opacity: 1; }
        }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state with enhanced tracking
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
        'time': None,
        'step_number': 1
    }
if 'is_loading' not in st.session_state:
    st.session_state.is_loading = False

# Load premium CSS
load_css()

# Premium Header
st.markdown("""
<div class="premium-header">
    <h1 class="brand-title">hoai.ch Salon Experience</h1>
    <p class="brand-subtitle">KI-gestützte Terminbuchung · Premium Service</p>
</div>
""", unsafe_allow_html=True)

# Progress Indicator
def render_progress():
    steps = [
        ("1", "Name", ["name"]),
        ("2", "Service", ["service"]),
        ("3", "Stylist", ["stylist"]),
        ("4", "Datum", ["date"]),
        ("5", "Zeit", ["time"]),
        ("6", "Bestätigung", ["confirm"])
    ]
    
    current_stage = st.session_state.booking_state['stage']
    
    progress_html = '<div class="progress-container">'
    
    for num, label, stages in steps:
        is_active = current_stage in stages
        is_completed = False
        
        # Check if step is completed
        if stages[0] == 'name' and st.session_state.booking_state['client_name']:
            is_completed = True
        elif stages[0] == 'service' and st.session_state.booking_state['service']:
            is_completed = True
        elif stages[0] == 'stylist' and st.session_state.booking_state['stylist']:
            is_completed = True
        elif stages[0] == 'date' and st.session_state.booking_state['date']:
            is_completed = True
        elif stages[0] == 'time' and st.session_state.booking_state['time']:
            is_completed = True
        
        status_class = 'active' if is_active else ('completed' if is_completed else '')
        
        progress_html += f"""
        <div class="progress-step {status_class}">
            <div class="step-circle">{num}</div>
            <div class="step-label">{label}</div>
        </div>
        """
    
    progress_html += '</div>'
    st.markdown(progress_html, unsafe_allow_html=True)

# Enhanced API Functions with loading states
@st.cache_data(show_spinner=False)
def load_services_and_stylists():
    """Load services and staff with caching"""
    services = []
    stylists = []
    
    try:
        resp = requests.get(f"{API_BASE_URL}/services", timeout=5)
        resp.raise_for_status()
        services = resp.json().get("data", {}).get("services", [])
    except:
        pass
    
    try:
        resp = requests.get(f"{API_BASE_URL}/staff", timeout=5)
        resp.raise_for_status()
        stylists = resp.json().get("data", {}).get("staff", [])
    except:
        pass
    
    return services, stylists

def api_search_client(name):
    """Search for a client by name with loading animation"""
    try:
        response = requests.get(f"{API_BASE_URL}/clients/search", params={"query": name})
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('data', {}).get('clients'):
                return data['data']['clients']
        return None
    except:
        return None

def api_get_availability(staff_id, service_id, date):
    """Get available time slots with loading animation"""
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
    except:
        return None

# Premium Loading Component
def show_loading_message(message="Verarbeite Ihre Anfrage"):
    return f"""
    <div style="display: flex; align-items: center; gap: 12px; color: var(--warm-gray); font-size: 0.9rem;">
        <div class="loading-dots">
            <span></span>
            <span></span>
            <span></span>
        </div>
        {message}
    </div>
    """

# Enhanced message processing with transitions
def process_chat_input(user_input):
    """Process user input with premium UX feedback"""
    state = st.session_state.booking_state
    
    # Add slight delay for premium feel
    with st.spinner(show_loading_message()):
        time.sleep(0.5)
    
    if state['stage'] == 'name':
        clients = api_search_client(user_input)
        
        if clients and len(clients) > 0:
            client = clients[0]
            state['client_name'] = client.get('name', user_input)
            state['client_id'] = client.get('id')
            state['stage'] = 'service'
            state['step_number'] = 2
            
            services, _ = load_services_and_stylists()
            service_list = "\n".join([f"• **{service.get('name', '')}**" for service in services])
            
            return f"""
            ✨ Herzlich willkommen, **{state['client_name']}**!
            
            Ich freue mich, Sie bei hoai.ch begrüßen zu dürfen.
            
            **Welchen Service darf ich heute für Sie buchen?**
            
            {service_list}
            """
        else:
            return f"""
            😊 Entschuldigung, ich konnte keinen Kunden mit dem Namen '{user_input}' finden.
            
            **Bitte versuchen Sie es erneut** oder kontaktieren Sie uns direkt unter:
            📞 +41 XX XXX XX XX
            """
    
    elif state['stage'] == 'service':
        services, _ = load_services_and_stylists()
        service_name = None
        
        for service in services:
            if service.get('name', '').lower() in user_input.lower():
                service_name = service.get('name')
                state['service'] = service_name
                state['service_id'] = service.get('id')
                break
        
        if service_name:
            state['stage'] = 'stylist'
            state['step_number'] = 3
            
            _, stylists = load_services_and_stylists()
            stylist_list = "\n".join([f"• **{stylist.get('name', '')}**" for stylist in stylists])
            
            return f"""
            Ausgezeichnete Wahl! **{service_name}** ist einer unserer beliebtesten Services. ✨
            
            **Bei welchem unserer Experten möchten Sie Ihren Termin buchen?**
            
            {stylist_list}
            
            Alle unsere Stylisten sind hochqualifiziert und freuen sich auf Sie!
            """
        else:
            return "Bitte wählen Sie einen der angezeigten Services aus. 🎯"
    
    elif state['stage'] == 'stylist':
        _, stylists = load_services_and_stylists()
        stylist_name = None
        
        for stylist in stylists:
            if stylist.get('name', '').lower() in user_input.lower():
                stylist_name = stylist.get('name')
                state['stylist'] = stylist_name
                state['stylist_id'] = stylist.get('id')
                break
        
        if stylist_name:
            state['stage'] = 'date'
            state['step_number'] = 4
            
            dates = []
            for i in range(7):
                date = (datetime.now() + timedelta(days=i))
                formatted_date = date.strftime('%Y-%m-%d')
                weekday = date.strftime('%A')
                weekday_de = {
                    'Monday': 'Montag',
                    'Tuesday': 'Dienstag',
                    'Wednesday': 'Mittwoch',
                    'Thursday': 'Donnerstag',
                    'Friday': 'Freitag',
                    'Saturday': 'Samstag',
                    'Sunday': 'Sonntag'
                }.get(weekday, weekday)
                
                dates.append(f"• **{formatted_date}** ({weekday_de})")
            
            return f"""
            Perfekt! **{stylist_name}** ist eine ausgezeichnete Wahl. 👏
            
            **An welchem Tag passt es Ihnen am besten?**
            
            {chr(10).join(dates)}
            
            💡 Tipp: Wählen Sie einfach das Datum aus (z.B. 2024-08-05)
            """
        else:
            return "Bitte wählen Sie einen unserer Stylisten aus. 🎨"
    
    elif state['stage'] == 'date':
        try:
            date_obj = datetime.strptime(user_input, '%Y-%m-%d')
            state['date'] = user_input
            
            with st.spinner(show_loading_message("Prüfe verfügbare Termine...")):
                slots = api_get_availability(
                    state['stylist_id'],
                    state['service_id'],
                    state['date']
                )
            
            if slots:
                state['stage'] = 'time'
                state['step_number'] = 5
                
                formatted_slots = []
                for slot in slots:
                    formatted_slots.append(f"• **{slot}** Uhr")
                
                return f"""
                Wunderbar! Für den **{date_obj.strftime('%d.%m.%Y')}** haben wir folgende Zeiten verfügbar:
                
                {chr(10).join(formatted_slots)}
                
                **Welche Zeit passt Ihnen am besten?**
                """
            else:
                return """
                Leider sind an diesem Tag keine Termine mehr verfügbar. 😔
                
                **Bitte wählen Sie einen anderen Tag.**
                """
        except ValueError:
            return "Bitte geben Sie das Datum im Format YYYY-MM-DD an (z.B. 2024-08-05). 📅"
    
    elif state['stage'] == 'time':
        time_input = user_input.strip()
        
        slots = api_get_availability(
            state['stylist_id'],
            state['service_id'],
            state['date']
        )
        
        if slots and time_input in slots:
            state['time'] = time_input
            state['stage'] = 'confirm'
            state['step_number'] = 6
            
            date_obj = datetime.strptime(state['date'], '%Y-%m-%d')
            
            return f"""
            **Ihre Terminübersicht:** 📋
            
            ━━━━━━━━━━━━━━━━━━━━━━
            **Service:** {state['service']}
            **Stylist:** {state['stylist']}
            **Datum:** {date_obj.strftime('%d.%m.%Y')}
            **Uhrzeit:** {state['time']} Uhr
            ━━━━━━━━━━━━━━━━━━━━━━
            
            **Möchten Sie diesen Termin verbindlich buchen?**
            
            Antworten Sie mit **'Ja'** zum Bestätigen oder **'Nein'** zum Abbrechen.
            """
        else:
            if slots:
                return f"""
                Diese Zeit ist leider nicht verfügbar. ⏰
                
                **Bitte wählen Sie eine der verfügbaren Zeiten:**
                {chr(10).join([f"• {slot}" for slot in slots])}
                """
            else:
                return "Es sind keine Zeiten mehr verfügbar. Bitte wählen Sie einen anderen Tag."
    
    elif state['stage'] == 'confirm':
        if 'ja' in user_input.lower():
            datetime_str = f"{state['date']} {state['time']}"
            
            # Simulate booking with animation
            with st.spinner(show_loading_message("Buche Ihren Termin...")):
                time.sleep(1.5)
                
                # Here would be the actual booking API call
                # result = api_book_appointment(...)
                
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
                    'time': None,
                    'step_number': 1
                }
                
                return f"""
                <div class="success-animation">
                ✅ **Termin erfolgreich gebucht!**
                
                Wir freuen uns auf Ihren Besuch bei hoai.ch.
                
                **Sie erhalten in Kürze:**
                • 📧 Eine Bestätigungs-E-Mail
                • 📱 Eine SMS-Erinnerung 24h vorher
                
                Bei Fragen erreichen Sie uns unter:
                📞 +41 XX XXX XX XX
                
                **Bis bald!** ✨
                </div>
                """
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
                'time': None,
                'step_number': 1
            }
            return """
            Buchung abgebrochen. 
            
            **Wie kann ich Ihnen helfen?** Bitte geben Sie Ihren Namen ein, um neu zu beginnen.
            """
    
    return "Entschuldigung, ich habe Sie nicht verstanden. Bitte versuchen Sie es erneut. 🤔"

# Main Chat Interface
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    # Progress indicator
    render_progress()
    
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant" and "<div" in message["content"]:
                st.markdown(message["content"], unsafe_allow_html=True)
            else:
                st.markdown(message["content"])
    
    # Initial greeting
    if not st.session_state.messages:
        greeting = """
        Willkommen bei **hoai.ch** 🌟
        
        Ich bin Ihr persönlicher KI-Assistent und helfe Ihnen gerne bei der Terminbuchung.
        
        **Bitte geben Sie Ihren Namen ein, um zu beginnen.**
        """
        st.session_state.messages.append({"role": "assistant", "content": greeting})
        with st.chat_message("assistant"):
            st.markdown(greeting)
    
    # Chat input
    if prompt := st.chat_input("Ihre Nachricht..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Process and add response
        response = process_chat_input(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            if "<div" in response:
                st.markdown(response, unsafe_allow_html=True)
                st.balloons()  # Celebration for successful booking
            else:
                st.markdown(response)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Premium Sidebar with Status
with st.sidebar:
    st.markdown("### 🌟 hoai.ch Premium")
    st.markdown("---")
    
    # API Status with elegant indicator
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=2)
        if response.status_code == 200:
            st.markdown("""
            <div class="status-badge success">
                <span>●</span> System Online
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="status-badge">
                <span>●</span> System Offline
            </div>
            """, unsafe_allow_html=True)
    except:
        st.markdown("""
        <div class="status-badge">
            <span>●</span> System Offline
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Loaded data indicator
    services, stylists = load_services_and_stylists()
    st.markdown(f"""
    **Verfügbare Services:** {len(services)}  
    **Team-Mitglieder:** {len(stylists)}
    """)
    
    st.markdown("---")
    
    # Contact info
    st.markdown("""
    **Kontakt:**  
    📞 +41 XX XXX XX XX  
    📧 info@hoai.ch  
    🌐 [hoai.ch](https://hoai.ch)
    """)