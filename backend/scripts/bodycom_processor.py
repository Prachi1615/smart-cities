"""
backend/scripts/bodycam_processor.py

Summarize simulated bodycam transcripts into real-time action reports via Anthropic.
"""
import time
import requests
import os
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

API_URL = "http://localhost:8000/action_reports"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = Anthropic(api_key=ANTHROPIC_API_KEY)

def process_bodycam():
    simulated_transcripts = [
        "Officer saw two people fighting near 5th Ave.",
        "Responder found a trapped victim in a collapsed building.",
        "Suspect fleeing scene heading south on Market Street."
    ]
    idx = 0
    while True:
        transcript = simulated_transcripts[idx % len(simulated_transcripts)]
        idx += 1

        prompt = (
            f"{HUMAN_PROMPT}Summarize this into an actionable report: '{transcript}'{AI_PROMPT}"
        )
        try:
            resp = client.completions.create(
                model="claude-2", prompt=prompt, max_tokens=60
            )
            report = resp.completion.strip()
            r = requests.post(API_URL, json={"report": report})
            print(f"Posted action report '{report}' → {r.status_code}")
        except Exception as e:
            print("Error summarizing/posting bodycam report:", e)

        time.sleep(20)  # adjust interval as needed

if __name__ == "__main__":
    process_bodycam()
