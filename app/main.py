from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from llama_cpp import Llama
import os

app = FastAPI()

# 설정
MODEL_PATH = os.getenv("MODEL_PATH", "app/models/EXAONE-3.5-2.4B-Instruct-Q2_K.gguf")
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048, # context window size
    n_threads=4, # number of threads
    n_gpu_layers=-1, # CPU 사용시 주석처리
    b=2, # batch size
)

# 시스템 프롬프트
DEFAULT_SYSTEM = "You are a helpful AI assistant. Answer whatever asked kindly and please answer only in Korean."

class Query(BaseModel):
    prompt: str # 사용자 질문

@app.post("/generate")
async def generate_text(query: Query):
    try:
        # 프롬프트 포맷 적용
        formatted_prompt = f"[|system|]{DEFAULT_SYSTEM}[|endofturn|]\n[|user|]{query.prompt}\n[|assistant|]"
        
        response = llm(
            formatted_prompt,
            max_tokens=256, # 답변의 최대 토큰 길이
            temperature=0.7, # temperature - 0.0 ~ 1.0, 높을수록 더 다양한 답변
            stop=["Q:", "\n"], # Stop generating just before the model would generate a new question
        )
        return {"response": response["choices"][0]["text"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}