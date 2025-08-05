# HSphere System Blueprint

## Overview
The HSphere is a closed, real-world simulated environment that trains and evolves intelligent systems. It serves as a training ground for agents (e.g. booking, inventory, prompt engineers) and is governed by a central Supervisor System.

---

## Structure

### **Agents/**
Agents are individual intelligent systems handling specific responsibilities.

- `main_booking.py` — Handles client bookings and appointment logic.
- `main_inventory.py` — Manages inventory (products, tools, usage).
- `main_promptforge.py` — Crafts and formats internal prompt requests.
- `main_selfimprove.py` — Self-evolves agents based on developer or system prompts.

### **Data/**
Shared local storage used by all agents.

- `clients.json` — Synthetic client profiles.
- `stylists.json` — Synthetic stylist profiles.
- `inventory.json` — Stock information (if needed).
- `services.json` — Service definitions (optional).

### **Logs/**
System logs and improvement records.

- `backups/` — Backups of `main.py` and other critical logic snapshots.
- `improvement_log.json` — Stores every code prompt + output revision.

### **Supervisor/**
The orchestrator of the HSphere.

- `supervisor.py` — Oversees the execution flow, agent routing, and prompt validation.

---

## Logic Flow

1. **Initialization**  
   - Supervisor loads all agents and validates data.
   - Environment is seeded with synthetic clients, stylists, and bookings.

2. **Execution Loop**  
   - Agents are run either in sequence or conditionally.
   - Logs are updated.
   - Prompts are forwarded to the Self-Improving Agent if evolution is requested.

3. **Self-Evolution**  
   - `main_selfimprove.py` reads improvement prompts.
   - Queries OpenAI for refined logic.
   - Writes code output, logs changes, and creates backups.

---

## Synthetic Roles

| Role            | Description                              | Data Source / Control     |
|------------------|------------------------------------------|----------------------------|
| Client Agent     | Simulates a client requesting services   | `clients.json`             |
| Stylist Agent    | Simulates stylist preferences/availability | `stylists.json`          |
| Prompt Agent     | Crafts prompts for evolution or upgrades | `Logs/improvement_log.json` |
| Booking Agent    | Handles appointments and availability    | `main_booking.py`          |
| Self-Improve     | Evolves system code from prompts         | `main_selfimprove.py`      |
| Supervisor       | Oversees agent coordination & rules      | `supervisor.py`            |

---

## Design Principles

- **Closed-Loop Environment**  
  No external systems unless explicitly authorized by Supervisor.

- **Prompt-Driven Intelligence**  
  Code evolves only through structured prompt reasoning.

- **Modular Evolution**  
  Agents can be versioned, swapped, improved, or retired independently.

- **Self-Coding + Self-Reflection**  
  System not only executes — it writes and evaluates its own logic.

- **Logs Are Sacred**  
  Every decision, backup, and improvement is traceable and restorable.

---

## Vision
The HSphere is more than a simulation. It is a living, breathing digital ecosystem designed to mimic the evolution of synthetic intelligence in the real world — modular, adaptable, and entirely prompt-driven.

---