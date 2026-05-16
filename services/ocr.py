from openai import OpenAI
from dotenv import load_dotenv
import base64, json, os

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

CBC_PROMPT = """
You are a medical lab report analyzer.
Extract ALL CBC lab test values from this image and return JSON only.
Use null for any missing value.
Format:
{
    "WBC": value or null,
    "RBC": value or null,
    "HGB": value or null,
    "HCT": value or null,
    "MCV": value or null,
    "MCH": value or null,
    "MCHC": value or null,
    "PLT": value or null,
    "PDW": value or null,
    "PCT": value or null,
    "LYMp": value or null,
    "NEUTp": value or null,
    "LYMn": value or null,
    "NEUTn": value or null
}
Return JSON only, no extra text, no markdown.
"""


def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def extract_cbc_values(image_path: str) -> dict:
    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model="google/gemini-2.5-flash-image",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": CBC_PROMPT},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }}
            ]
        }]
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)
