import uvicorn
import importlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import sys

ENCODER_PATH = './encoders'

# 加入 encoders 路径
sys.path.insert(0, ENCODER_PATH)

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


# encode 参数
class Inputs(BaseModel):
    encoder: str
    text: str

def scan_encoders():
    encoders = []
    scan_root = ENCODER_PATH
    for name in os.listdir(scan_root):
        full_path = os.path.join(scan_root, name)
        init_file = os.path.join(full_path, '__init__.py')
        if(os.path.isdir(full_path) and os.path.exists(init_file)):
            encoders.append(name)
    return encoders

def call_encoder(encoder_name:str, text:str):
    try:
        module = importlib.import_module(encoder_name)
        encode_func = getattr(module, 'encode')
        return encode_func(text)
    except (ImportError, AttributeError) as e:
        print(f"Error: {e}")
        raise

@app.post("/encode", response_model=List[Segment])
async def get_encode_result(input: Inputs):
    return call_encoder(input.encoder, input.text)
    # return [
    #     {
    #         'text':f'encoder is:{input.encoder} and {len(input.text)} texts',
    #         'tokens':[{'id':123, 'idx':0}]
    #     },
    #     {
    #         'text':f'encoder is:{input.encoder} and {len(input.text)} texts',
    #         'tokens':[{'id':345, 'idx':1}]
    #     }
    # ]

@app.get('/list', response_model=List[str])
async def get_encoders():
    # return ['remote model a', 'remote model b']
    return scan_encoders()
    
if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8231)