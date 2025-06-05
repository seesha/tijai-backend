from fastapi import FastAPI
from pydantic import BaseModel
import base64
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class ChartRequest(BaseModel):
    image: str

@app.post("/analyze")
async def analyze_chart(request: ChartRequest):
    image_data = base64.b64decode(request.image.split(",")[1])
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze this trading chart and return trend, entry, stop loss, target, support/resistance, patterns, and explanation."},
                    {"type": "image_url", "image_url": {"url": "data:image/png;base64," + request.image.split(",")[1]}}
                ]
            }
        ]
    )
    reply = response.choices[0].message.content
    return {"analysis": reply}
