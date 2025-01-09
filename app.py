from fastapi import FastAPI, Request
from pydantic import BaseModel
from vllm import LLM, SamplingParams

app = FastAPI()

# Initialize the vllm model
"""
파라미터 참고:
https://docs.vllm.ai/en/latest/api/params.html#sampling-params
"""
sampling_params = SamplingParams(temperature=0.7,
                                 top_k=10,
                                 top_p=0.9,
                                 repetition_penalty=1.0,
                                 max_token=200)
llm = LLM(model_name="facebook/opt-125m")

class GenerationRequest(BaseModel):
    input: str

@app.post("/generate")
async def generate(request: GenerationRequest):
    input_text = request.input

    # Perform generation using vllm
    output = llm.generate(input_text, sampling_params)

    return {"output": output}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)