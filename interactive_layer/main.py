from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .service import InteractiveService
from .config import API_HOST, API_PORT, CHAT_PATH
import uvicorn

app = FastAPI(title="News Intelligence Interaction Layer")
service = InteractiveService()

class QuestionRequest(BaseModel):
    user_input: str

@app.get("/")
def read_root():
    return {"status": "success", "message": "Interaction Layer API is running"}

@app.post(CHAT_PATH)
async def chat(request: QuestionRequest):
    """
    智能问答接口
    """
    if not request.user_input:
        raise HTTPException(status_code=400, detail="user_input cannot be empty")
    
    try:
        answer = service.ask(request.user_input)
        return {"answer": answer}
    except Exception as e:
        print(f"Chat API Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def run():
    print(f"正在启动交互层服务器: http://{API_HOST}:{API_PORT}")
    uvicorn.run(app, host=API_HOST, port=API_PORT)

if __name__ == "__main__":
    run()
