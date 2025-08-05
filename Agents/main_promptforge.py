import sys
import os
from HSphere.Logs.improvement_logger import log_event
from datetime import datetime

def generate_prompt(context, objective):
    prompt = f"Given the context: {context}, generate a solution to: {objective}"
    log_event("PromptForge", f"Generated prompt for objective: {objective}")
    return prompt

def analyze_prompt(prompt):
    length = len(prompt)
    complexity = "High" if length > 200 else "Medium" if length > 100 else "Low"
    log_event("PromptForge", f"Analyzed prompt: {prompt[:50]}... | Complexity: {complexity}")
    return {
        "length": length,
        "complexity": complexity,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    context = input("Enter context: ")
    objective = input("Enter objective: ")
    prompt = generate_prompt(context, objective)
    print("\nGenerated Prompt:\n", prompt)

    analysis = analyze_prompt(prompt)
    print("\nAnalysis:\n", analysis)
