from fastapi import FastAPI
from pydantic import BaseModel
from agents import AgentProcessor
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
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
    query: str

@app.get("/")
def read_root():
    return {"message": "E-commerce Agent API is running"}

@app.post("/query")
def process_query(query: Query):
    return agent.process_query(query.query)

# For testing the API directly
@app.get("/test/{test_query}")
def test_query(test_query: str):
    return agent.process_query(test_query) 