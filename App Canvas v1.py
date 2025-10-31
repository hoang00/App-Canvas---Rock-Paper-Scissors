"""
Benchling App Canvas: Rock‑Paper‑Scissors example (FastAPI)
-----------------------------------------------------------------
This single-file example shows a minimal interactive Benchling App Canvas
that renders three buttons (Rock, Paper, Scissors). When a user clicks a
button, the app computes a result vs. a random AI choice and PATCHes the
canvas to show the outcome, along with new buttons to play again.

It is intentionally tiny so you can lift it into your own environment
(or adapt the patterns from https://github.com/benchling/app-examples-python).

🧩 Blocks used: BUTTON + MARKDOWN (kept simple on purpose).

📦 Requires: fastapi, uvicorn, httpx, pydantic
    pip install fastapi uvicorn httpx pydantic

🔐 Env vars you must set (e.g., in a .env file or your host’s secret store):
    BENCHLING_BASE_URL=https://{your-tenant}.benchling.com
    BENCHLING_ACCESS_TOKEN=...   # Bearer token for your Benchling *app* install

⚙️ Webhook URL to configure in your Benchling app:  POST {public_base}/webhook

📝 Manifest sketch (YAML) for your app (save separately and upload when creating from a manifest):

    name: Rock Paper Scissors
    description: Tiny demo app that renders an interactive App Canvas with three buttons.
    features:
      - name: RPS Canvas
        id: rps_canvas
        type: CANVAS
        locations:
          - ENTRY
          - ENTRY_TEMPLATE
          - APP_HOMEPAGE
    subscriptions:
      deliveryMethod: WEBHOOK
      messages:
        - type: v2.canvas.created
        - type: v2.canvas.userInteracted

The flow mirrors the “App Canvas Diagram”: Benchling UI → (webhook -> /webhook)
→ our app decides what to render → calls Benchling Canvas API to CREATE/PATCH →
user sees live updates.
"""

import os
import random
from enum import Enum
from typing import Dict, List, Optional

import httpx
from fastapi import FastAPI, Request
from pydantic import BaseModel

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
    # Include resourceId when provided (ASSAY_RUN/App Homepage canvases)
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
    """Return three BUTTON blocks with distinct IDs so clicks trigger webhooks."""
    return [
        {"id": "btn_rock", "type": "BUTTON", "text": CHOICE_LABEL[Choice.ROCK]},
        {"id": "btn_paper", "type": "BUTTON", "text": CHOICE_LABEL[Choice.PAPER]},
        {"id": "btn_scissors", "type": "BUTTON", "text": CHOICE_LABEL[Choice.SCISSORS]},
    ]


def rps_header_md() -> Dict:
    return {
        "id": "md_header",
        "type": "MARKDOWN",
        "value": "### Rock‑Paper‑Scissors\nPick one of the moves below. The app will counter with a random choice.",
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
# Webhook payload models (subset of fields we use)
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
# FastAPI app
# -------------------------------
app = FastAPI(title="Benchling RPS App Canvas")

@app.get("/")
async def root():
    return {"status": "ok", "name": "benchling-rps-app"}

@app.post("/webhook")
async def webhook(req: Request):
    """
    Handles: v2.canvas.created and v2.canvas.userInteracted
    NOTE: For production, verify webhook signatures per Benchling docs.
    """
    body = await req.json()
    event = WebhookEnvelope(**body)
    msg = event.message

    if msg.type == "v2.canvas.created":
        # Create the initial canvas for the feature/location where user inserted it
        blocks = initial_blocks()
        await create_canvas(blocks, feature_id=msg.featureId or "", resource_id=msg.resourceId)
        return {"ok": True}

    if msg.type == "v2.canvas.userInteracted":
        # Determine which move the user clicked from the buttonId
        mapping = {
            "btn_rock": Choice.ROCK,
            "btn_paper": Choice.PAPER,
            "btn_scissors": Choice.SCISSORS,
        }
        if msg.buttonId not in mapping or not msg.canvasId:
            return {"ok": True}
        result = RPSGame.play(mapping[msg.buttonId])
        await update_canvas(msg.canvasId, result_blocks(result))
        return {"ok": True}

    # Acknowledge other webhook types to keep UI snappy
    return {"ok": True, "ignored": msg.type}

# -------------------------------
# Local dev runner
# -------------------------------
# Run with:  uvicorn app:app --reload --port 8080
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)
