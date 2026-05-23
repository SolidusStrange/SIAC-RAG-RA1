from dotenv import load_dotenv
from pathlib import Path
import os
import requests

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path, override=True)

token = os.getenv("GITHUB_TOKEN")

print("Token cargado:", bool(token))
print("Largo:", len(token) if token else None)
print("Prefijo:", token[:4] if token else None)
print("Sufijo:", token[-4:] if token else None)

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
    "X-GitHub-Api-Version": "2022-11-28",
}

print("\nProbando GitHub normal...")
r = requests.get("https://api.github.com/user", headers=headers)
print("GitHub user status:", r.status_code)
print(r.text[:500])

print("\nProbando GitHub Models...")
payload = {
    "model": "openai/gpt-4.1-mini",
    "messages": [
        {
            "role": "user",
            "content": "Responde solo funciona."
        }
    ],
    "temperature": 0
}

r = requests.post(
    "https://models.github.ai/inference/chat/completions",
    headers={**headers, "Content-Type": "application/json"},
    json=payload
)

print("Models status:", r.status_code)
print(r.text[:1000])