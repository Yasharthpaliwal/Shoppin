from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents import AgentProcessor
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any

app = FastAPI(title="E-commerce Agent API")
agent = AgentProcessor()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo purposes. In production, specify origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    text: str

@app.get("/")
async def root():
    return {"message": "E-commerce Agent API is running"}

@app.post("/process_query")
async def process_query(query: Query) -> Dict[str, Any]:
    try:
        response = await agent.process_query(query.text)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# For testing the API directly
@app.get("/test/{test_query}")
def test_query(test_query: str):
    return agent.process_query(test_query) 
