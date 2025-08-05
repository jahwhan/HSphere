import sys
import os
import json
from datetime import datetime
from HSphere.Logs.improvement_logger import log_event

INVENTORY_FILE = "HSphere/Data/inventory.json"

def load_inventory():
    try:
        with open(INVENTORY_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_inventory(data):
    with open(INVENTORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def view_inventory():
    inventory = load_inventory()
    if not inventory:
        print("Inventory is currently empty.")
    else:
        for item in inventory:
            print(f"{item['name']} - {item['quantity']} units (last updated: {item['updated']})")

def update_inventory():
    inventory = load_inventory()
    name = input("Enter product/tool name: ").strip()
    quantity = input("Enter new quantity: ").strip()

    for item in inventory:
        if item["name"].lower() == name.lower():
            item["quantity"] = quantity
            item["updated"] = datetime.now().isoformat()
            break
    else:
        inventory.append({
            "name": name,
            "quantity": quantity,
            "updated": datetime.now().isoformat()
        })

    save_inventory(inventory)
    log_event("Inventory", f"Updated {name} to {quantity} units.")
    print(f"{name} updated successfully.")

def inventory_interface():
    print("\nInventory System â Choose an option:")
    print("1. View Inventory")
    print("2. Update Inventory")
    print("3. Exit")

    while True:
        choice = input("Enter choice: ").strip()
        if choice == "1":
            view_inventory()
        elif choice == "2":
            update_inventory()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    inventory_interface()
