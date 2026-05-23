from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path, override=True)

token = os.getenv("GITHUB_TOKEN")

print("ENV path:", env_path)
print("Token cargado:", bool(token))
print("Largo token:", len(token) if token else None)
print("Prefijo:", token[:4] if token else None)
print("Sufijo:", token[-4:] if token else None)

client = OpenAI(
    api_key=token,
    base_url="https://models.github.ai/inference",
    default_headers={
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
)

response = client.chat.completions.create(
    model="openai/gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content": "Hola, responde solo 'funciona'."
        }
    ],
    temperature=0
)

print(response.choices[0].message.content)