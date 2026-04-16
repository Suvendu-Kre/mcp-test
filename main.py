from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from agents.main_agent import Agent
from guardrails.safety import validate_input, validate_output
from error_handling.handler import retry
from observability.monitoring import process_request
import logging

app = FastAPI()
agent = Agent()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
@process_request
async def chat_endpoint(request: ChatRequest):
    try:
        validated_input = validate_input(request.message)
        if validated_input.startswith("Error:"):
            raise HTTPException(status_code=400, detail=validated_input)

        @retry
        def run_agent():
            return agent.run(validated_input)

        response = run_agent()

        validated_output = validate_output(response)
        if validated_output.startswith("Error:"):
             raise HTTPException(status_code=500, detail=validated_output)

        return ChatResponse(response=validated_output)

    except Exception as e:
        logging.exception("Error processing chat request")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn, os
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8081)))