# fastapi_app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class InputData(BaseModel):
    브랜드명: str
    업종_선택: str
    선택: str
    브랜드_소개: str

@app.post("/execute")
def execute(data: InputData):
    # 예시로 단순히 데이터를 반환합니다.
    # 실제 응답 처리 로직을 이곳에 작성합니다.
    response = {
        "message": "데이터가 성공적으로 처리되었습니다.",
        "received_data": data.dict()
    }
    return response
