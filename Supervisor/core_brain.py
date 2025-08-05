import json
import os
import time
from monitor import generate_report
from log_parser import summarize_logs  # Optional call

class CoreBrain:
    def __init__(self):
        self.system_map = {}
        self.short_term_memory = []
        self.long_term_memory_path = "Data/memory_long.json"

    def perceive_system(self):
        generate_report()  # Ask monitor for status
        self.system_map = self.load_system_map()
        print("[CoreBrain] Perceived system.")

    def load_system_map(self):
        try:
            with open("Data/system_map.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def remember(self, event, important=False):
        self.short_term_memory.append(event)
        if important:
            self._commit_to_longterm(event)

    def _commit_to_longterm(self, event):
        try:
            if os.path.exists(self.long_term_memory_path):
                with open(self.long_term_memory_path, "r") as f:
                    memory = json.load(f)
            else:
                memory = []

            memory.append(event)
            with open(self.long_term_memory_path, "w") as f:
                json.dump(memory, f, indent=2)
            print("[CoreBrain] Event committed to long-term memory.")
        except Exception as e:
            print(f"[CoreBrain] Memory error: {e}")

    def act_on_trigger(self, trigger):
        print(f"[CoreBrain] Reacting to trigger: {trigger}")
        if "spawn_agent" in trigger:
            print("[CoreBrain] Would spawn new agent here.")
        elif "refactor_logic" in trigger:
            print("[CoreBrain] Would call self-improvement here.")

    def generate_system_map(self):  # ✅ Now properly inside the class
        agents_dir = "Agents"
        descriptions_file = "Data/agent_descriptions.json"
        system_map = {}

        try:
            with open(descriptions_file, "r") as f:
                descriptions = json.load(f)
        except Exception as e:
            descriptions = {}
            print(f"[CoreBrain] Couldn't load agent descriptions: {e}")

        for file in os.listdir(agents_dir):
            if file.endswith(".py") and not file.startswith("__"):
                name = file.replace(".py", "")
                system_map[name] = {
                    "path": f"{agents_dir}/{file}",
                    "description": descriptions.get(file, "No description provided."),
                    "status": "active"
                }

        with open("Data/system_map.json", "w") as f:
            json.dump(system_map, f, indent=2)

        print("[CoreBrain] System map updated.")

    def run(self):
        self.perceive_system()
        self.generate_system_map()
        self.remember({"event": "Startup", "timestamp": time.time()}, important=True)

        # Import the booking agent
        from Agents import main_booking

        self.remember({
            "event": "BookingTestStart",
            "timestamp": time.time()
        }, important=False)

        main_booking.book_appointment(
            client_id="123",
            stylist_id="456",
            datetime="2025-05-23 15:00",
            service="Fade + Beard"
        )

        self.remember({
            "event": "BookingTestEnd",
            "timestamp": time.time()
        }, important=True)

        # self.act_on_trigger("spawn_agent")  # Just for simulation

        
        
if __name__ == "__main__":
    brain = CoreBrain()
    brain.run()
        


    

