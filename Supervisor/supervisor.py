print("HSphere Supervisor Booted. Awaiting agent commands...")
import os
import sys
from HSphere.Agents import main_booking, main_inventory, main_selfimprove, main_promptforge
from HSphere.Logs.improvement_logger import log_event
from HSphere.Agents import main_booking
from HSphere.Logs.improvement_logger import log_event

def route_command(command):
    if command == "book_appointment":
        log_event("Supervisor", "Routing to booking agent")
        main_booking.book()
    else:
        log_event("Supervisor", f"Unknown command: {command}")
        print("Command not recognized.")

if __name__ == "__main__":
    print("HSphere Supervisor Online.")
    cmd = input("Enter command for Supervisor: ")
    route_command(cmd)
def display_menu():
    print("\n=== HSphere Supervisor System ===")
    print("1. Book appointment")
    print("2. Manage inventory")
    print("3. Self-improve system")
    print("4. Forge prompt tools")
    print("5. Run external script")
    print("0. Exit")

def route_choice(choice):
    if choice == "1":
        log_event("Supervisor", "Routing to booking agent")
        main_booking.book()
    elif choice == "2":
        log_event("Supervisor", "Routing to inventory agent")
        main_inventory.manage_inventory()
    elif choice == "3":
        log_event("Supervisor", "Routing to self-improvement agent")
        main_selfimprove.self_improve()
    elif choice == "4":
        log_event("Supervisor", "Routing to prompt-forging agent")
        main_promptforge.forge_prompt_tool()
    elif choice == "5":
        log_event("Supervisor", "Routing to script agent")
        main_script.execute_script()
    elif choice == "0":
        print("Exiting HSphere Supervisor.")
        sys.exit()
    else:
        print("Invalid choice.")

def run_supervisor():
    while True:
        display_menu()
        choice = input("Enter command: ").strip()
        route_choice(choice)

if __name__ == "__main__":
    run_supervisor()
