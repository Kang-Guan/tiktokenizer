import uvicorn
import importlib
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import os
import sys
import argparse

parser = argparse.ArgumentParser(description="Encode server")
parser.add_argument("--host", type=str, default="0.0.0.0", help="Host IP address")
parser.add_argument("--port", type=int, default=8231, help="Port number")
args = parser.parse_args()

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

@app.get('/list', response_model=List[str])
async def get_encoders():
    # return ['remote model a', 'remote model b']
    return scan_encoders()
    
@app.get("/")
async def get_homepage():
    return FileResponse("../out/index.html", media_type="text/html")

app.mount("/", StaticFiles(directory="../out"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host=args.host, port=args.port)