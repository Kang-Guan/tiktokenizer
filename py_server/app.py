import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 返回类型
class _Token(BaseModel):
    id: int
    idx: int

class Segment(BaseModel):
    text: str
    tokens: List[_Token]

# 传入类型
class Inputs(BaseModel):
    encoder: str
    text: str

# 创建新的待办事项
@app.post("/encode", response_model=List[Segment])
def get_encode_result(input: Inputs):
    return [
        {
            'text':f'encoder is:{input.encoder} and {len(input.text)} texts',
            'tokens':[{'id':123, 'idx':0}]
        },
        {
            'text':f'encoder is:{input.encoder} and {len(input.text)} texts',
            'tokens':[{'id':345, 'idx':1}]
        }
    ]
    
if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8231)