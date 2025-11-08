"""
Benchling App Canvas: Rock-Paper-Scissors (FastAPI)
---------------------------------------------------
Minimal interactive App Canvas demo:
- Renders three buttons (Rock / Paper / Scissors)
- Handles user clicks via webhooks
- PATCHes the canvas with the result and lets you play again

Requirements (install in your venv):
    pip install fastapi uvicorn httpx pydantic python-dotenv

Environment variables (e.g., in .env):
    BENCHLING_BASE_URL=https://<your-tenant>.benchling.com
    BENCHLING_ACCESS_TOKEN=<your app install token>

Webhook URL in Benchling app settings:
    https://<your-tunnel>.trycloudflare.com/webhook
"""

import os
import random
from enum import Enum
from typing import Dict, List, Optional

from dotenv import load_dotenv
load_dotenv()  # loads .env next to this file (or current working dir)

import httpx
from fastapi import FastAPI, Request
from pydantic import BaseModel

# -------------------------------
# FastAPI app (create first!)
# -------------------------------
app = FastAPI(title="Benchling RPS App Canvas")

# -------------------------------
# Domain model: Rock / Paper / Scissors
# -------------------------------
class Choice(str, Enum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"

CHOICE_LABEL = {
    Choice.ROCK: "🪨 Rock",
    Choice.PAPER: "📄 Paper",
    Choice.SCISSORS: "✂️ Scissors",
}

class RPSResult(str, Enum):
    WIN = "win"
    LOSE = "lose"
    DRAW = "draw"

class RPSGame:
    @staticmethod
    def play(user: Choice) -> Dict[str, str]:
        ai = random.choice([Choice.ROCK, Choice.PAPER, Choice.SCISSORS])
        outcome = RPSResult.DRAW
        if user != ai:
            if (
                (user == Choice.ROCK and ai == Choice.SCISSORS)
                or (user == Choice.PAPER and ai == Choice.ROCK)
                or (user == Choice.SCISSORS and ai == Choice.PAPER)
            ):
                outcome = RPSResult.WIN
            else:
                outcome = RPSResult.LOSE
        return {"user": user.value, "ai": ai.value, "outcome": outcome.value}

# -------------------------------
# Benchling API helpers
# -------------------------------
BENCHLING_BASE_URL = os.environ.get("BENCHLING_BASE_URL", "").rstrip("/")
ACCESS_TOKEN = os.environ.get("BENCHLING_ACCESS_TOKEN", "")

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
}

API_CREATE_CANVAS = "/api/v2/app-canvases"
API_UPDATE_CANVAS = "/api/v2/app-canvases/{canvas_id}"

async def create_canvas(blocks: List[Dict], feature_id: str, resource_id: Optional[str] = None) -> Dict:
    url = f"{BENCHLING_BASE_URL}{API_CREATE_CANVAS}"
    payload: Dict = {"blocks": blocks, "enabled": True, "featureId": feature_id}
    if resource_id:
        payload["resourceId"] = resource_id
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(url, headers=HEADERS, json=payload)
        r.raise_for_status()
        return r.json()

async def update_canvas(canvas_id: str, blocks: List[Dict]) -> Dict:
    url = f"{BENCHLING_BASE_URL}{API_UPDATE_CANVAS.format(canvas_id=canvas_id)}"
    payload = {"blocks": blocks, "enabled": True}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.patch(url, headers=HEADERS, json=payload)
        r.raise_for_status()
        return r.json()

# -------------------------------
# Canvas UI factories (BLOCK JSON)
# -------------------------------
def rps_choice_buttons() -> List[Dict]:
    return [
        {"id": "btn_rock", "type": "BUTTON", "text": CHOICE_LABEL[Choice.ROCK]},
        {"id": "btn_paper", "type": "BUTTON", "text": CHOICE_LABEL[Choice.PAPER]},
        {"id": "btn_scissors", "type": "BUTTON", "text": CHOICE_LABEL[Choice.SCISSORS]},
    ]

def rps_header_md() -> Dict:
    return {
        "id": "md_header",
        "type": "MARKDOWN",
        "value": "### Rock-Paper-Scissors\nPick a move below. The app will counter with a random choice.",
    }

def rps_result_md(result: Dict[str, str]) -> Dict:
    outcome = result["outcome"].upper()
    md = (
        f"**You:** `{result['user']}`\n\n"
        f"**AI:** `{result['ai']}`\n\n"
        f"### Result: **{outcome}**\n\n"
        f"_Click a button to play again._"
    )
    return {"id": "md_result", "type": "MARKDOWN", "value": md}

def initial_blocks() -> List[Dict]:
    return [rps_header_md(), *rps_choice_buttons()]

def result_blocks(result: Dict[str, str]) -> List[Dict]:
    return [rps_header_md(), rps_result_md(result), *rps_choice_buttons()]

# -------------------------------
# Webhook payload models (subset)
# -------------------------------
class AppInfo(BaseModel):
    id: str

class Message(BaseModel):
    type: str
    featureId: Optional[str] = None
    resourceId: Optional[str] = None
    canvasId: Optional[str] = None
    buttonId: Optional[str] = None

class WebhookEnvelope(BaseModel):
    version: str
    baseURL: str
    tenantId: str
    app: AppInfo
    message: Message

# -------------------------------
# Routes
# -------------------------------
@app.get("/")
async def root():
    return {"status": "ok", "name": "benchling-rps-app"}

# Primary webhook path — set this in Benchling:
#   https://<your-tunnel>.trycloudflare.com/webhook
@app.post("/webhook")
async def webhook(req: Request):
    body = await req.json()
    event = WebhookEnvelope(**body)
    msg = event.message

    if msg.type == "v2.canvas.created":
        await create_canvas(initial_blocks(), feature_id=msg.featureId or "", resource_id=msg.resourceId)
        return {"ok": True}

    if msg.type == "v2.canvas.userInteracted":
        mapping = {"btn_rock": Choice.ROCK, "btn_paper": Choice.PAPER, "btn_scissors": Choice.SCISSORS}
        if msg.buttonId not in mapping or not msg.canvasId:
            return {"ok": True}
        result = RPSGame.play(mapping[msg.buttonId])
        await update_canvas(msg.canvasId, result_blocks(result))
        return {"ok": True}

    return {"ok": True, "ignored": msg.type}

# Fallback path so older configs that post to /webhook/canvas still work
@app.post("/webhook/canvas")
async def webhook_canvas(req: Request):
    return await webhook(req)

# -------------------------------
# Local dev runner
# -------------------------------
if __name__ == "__main__":
    import uvicorn
    # If your filename has spaces, we pass the app object directly:
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
