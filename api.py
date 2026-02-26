from fastapi import FastAPI
from pydantic import BaseModel
from chat_style_agent.agent import adapt_one

app = FastAPI()

class RewriteRequest(BaseModel):
    text: str
    country: str
    age: str
    scene: str


@app.post("/rewrite")
def rewrite(req: RewriteRequest):
    result = adapt_one(
        text=req.text,
        country=req.country,
        age=req.age,
        scene=req.scene,
    )
    return result