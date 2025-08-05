import os
import sys
import json
import openai

# Dynamically add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

AGENTS_PATH = os.path.join(os.path.dirname(__file__))
LOG_PATH = os.path.join(os.path.dirname(__file__), "../Logs/improvement_log.json")

def log_event(category, message):
    log = []
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            try:
                log = json.load(f)
            except json.JSONDecodeError:
                pass
    log.append({"category": category, "message": message})
    with open(LOG_PATH, "w") as f:
        json.dump(log, f, indent=2)


def improve_agent():
    print("\n=== Self-Improvement Agent ===")
    print("Available agents:")
    agents = [f for f in os.listdir(AGENTS_PATH) if f.startswith("main") and f.endswith(".py") and f != os.path.basename(__file__)]
    for i, agent in enumerate(agents):
        print(f"{i+1}. {agent}")

    choice = int(input("Select agent number to improve: ")) - 1
    target_file = os.path.join(AGENTS_PATH, agents[choice])

    with open(target_file, "r") as f:
        current_code = f.read()

    prompt = input("Describe the improvement you'd like to apply: ")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a senior Python engineer who specializes in AI systems."},
                {"role": "user", "content": f"Here is the current code for {agents[choice]}:\n\n{current_code}\n\nPlease improve it based on this instruction:\n{prompt}"}
            ],
            temperature=0.3
        )
        
        new_code = response["choices"][0]["message"]["content"]
        print("\n=== Suggested Improvement ===\n")
        print(new_code)

        confirm = input("Apply this change? (yes/no): ")
        if confirm.lower() == "yes":
            with open(target_file, "w") as f:
                f.write(new_code)
            log_event("SelfImprove", f"Updated {agents[choice]} with new code.")
            print("Agent improved successfully.")
        else:
            print("No changes applied.")

    except Exception as e:
        print("Error during improvement:", e)
        log_event("SelfImprove", f"Error improving {agents[choice]}: {e}")


if __name__ == "__main__":
    improve_agent()
