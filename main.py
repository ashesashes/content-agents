from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from crewai_code import run_crewai_task

import logging 


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class TaskDescription(BaseModel):
    description: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# @app.get("/run-task")
@app.post("/run-task")

# def run_task():
#     result = run_crewai_task()
#     return {"result": result}

def run_task(task: TaskDescription):
    try:
        # logging.info("Starting run_task")
        result = run_crewai_task(task.description)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    