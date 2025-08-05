import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

try:
    from Data.clients_data import clients
    print("SUCCESS! First client:", clients[0])
except Exception as e:
    print("ERROR:", e)
    print("Current Python path:", sys.path)