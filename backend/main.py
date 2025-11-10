from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from scrape.parseStudentDegree_DeepSeekop import parse_degreeworks_pdf
from scrape.ai import create_agent_with_degreeworks, run_agent, validate_and_clean_json_response
from langchain_core.messages import HumanMessage, AIMessage
import os
import uuid
import json
import time

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session storage (use Redis or database in production)
sessions = {}

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.post("/api/pdf")
async def process_pdf(
    file: UploadFile = File(...), 
    prompt: str = Form(...), 
    is_long_planning_mode: bool = Form(...)
):
    """Process PDF, create agent, and return initial response"""
    try:
        # Create pdfs directory if it doesn't exist
        os.makedirs("./pdfs", exist_ok=True)
        
        # Save uploaded file
        file_path = f"./pdfs/{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Parse PDF
        parsed_degreeworks = parse_degreeworks_pdf(file_path)
        
        # Create session ID
        session_id = str(uuid.uuid4())
        
        # Set reasoning effort based on mode
        reasoning_effort = "medium" if is_long_planning_mode else "low"
        
        # Create agent with parsed degreeworks
        agent = create_agent_with_degreeworks(parsed_degreeworks, reasoning_effort)
        
        # Initialize conversation history
        history = []
        
        # Run agent with initial prompt
        agent_result = run_agent(prompt, history, agent)
        response = agent_result["message"]
        time_taken = agent_result.get("time_taken", 0)
        
        # Log raw response for debugging
        print(f"Raw agent response: {response.content[:500]}...")
        
        validated_response = validate_and_clean_json_response(response)
        
        # Update history
        history.append(HumanMessage(content=prompt))
        history.append(validated_response)
        
        # Store session
        sessions[session_id] = {
            "agent": agent,
            "history": history,
            "parsed_degreeworks": parsed_degreeworks,
            "reasoning_effort": reasoning_effort
        }
        
        # Parse response content - it should already be valid JSON from validation
        try:
            response_data = json.loads(validated_response.content)
        except json.JSONDecodeError:
            # Fallback if somehow not JSON
            response_data = {"text": validated_response.content, "recommended_courses": []}
        
        # Ensure response has the expected structure
        if "recommended_courses" not in response_data:
            response_data["recommended_courses"] = []
        if "text" not in response_data:
            response_data["text"] = "Response generated successfully."
        
        return {
            "session_id": session_id,
            "response": response_data,
            "message": "PDF processed and initial response generated",
            "time_taken": round(time_taken, 2)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@app.post("/api/chat")
async def chat(
    session_id: str = Form(...),
    message: str = Form(...)
):
    """Continue conversation with existing session"""
    try:
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = sessions[session_id]
        agent = session["agent"]
        history = session["history"]
        
        # Run agent with new message
        agent_result = run_agent(message, history, agent)
        response = agent_result["message"]
        time_taken = agent_result.get("time_taken", 0)
        
        validated_response = validate_and_clean_json_response(response)
        
        # Update history
        history.append(HumanMessage(content=message))
        history.append(validated_response)
        
        # Parse response content
        try:
            response_data = json.loads(validated_response.content)
        except json.JSONDecodeError:
            response_data = {"text": validated_response.content, "recommended_courses": []}
        
        return {
            "response": response_data,
            "message": "Response generated",
            "time_taken": round(time_taken, 2)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)