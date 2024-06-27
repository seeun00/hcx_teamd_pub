# fastapi_app.py
import json
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

class CompletionExecutor:
    def __init__(self):
        self._host = os.getenv('API_HOST')
        self._api_key = os.getenv('API_KEY')
        self._api_key_primary_val = os.getenv('API_KEY_PRIMARY_VAL')
        self._request_id = os.getenv('REQUEST_ID')

    def execute(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'text/event-stream'
        }

        with requests.post(self._host + '/testapp/v1/tasks/a3r5nl4j/chat-completions',
                           headers=headers, json=completion_request, stream=True) as r:
            event_result_found = False
            for line in r.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if event_result_found:
                        json_part = decoded_line.split('data:', 1)[1]
                        json_data = json.loads(json_part)
                        return json_data["message"]["content"]
                    if decoded_line.startswith("event:result"):
                        event_result_found = True

class InputData(BaseModel):
    분류: str
    브랜드: str
    스타일: str

def format_fix(data):
    formatted_data = ""
    for key, value in data.items():
        formatted_data += f"{key}: {value}\n"
    return formatted_data


@app.post("/execute")
def execute(data: InputData):
    # 예시로 단순히 데이터를 반환합니다.
    # 실제 응답 처리 로직을 이곳에 작성합니다.
    response = {
        "message": "데이터가 성공적으로 처리되었습니다.",
        "received_data": data.dict()
    }
    print("received_data : " + format_fix(response['received_data']))

    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiY5hZx6dN1Tpv3ZTB8YSA6lz7UXUZlVA9R6yULgExuyf6',
        api_key_primary_val='YLRxXUhJANdAcQpY9KW9JygbX5Nf54mHHAQw1wdy',
        request_id='139867a2-d000-4add-b0bd-631c27b77604'
    )

    preset_text = [{"role": "system",
                    "content": "당신은 수년간의 경험을 가진 전문 광고 카피라이터입니다. 3가지 항목을 사용자 입력으로 받아 창의적이고 매력적인 광고 문구를 작성해주세요.\n\n\n광고 카피를 생성할 때 다음 내용을 반영하세요.\n\r\n1. 브랜드의 톤앤매너를 반영할 것\r\n2. 핵심 메시지를 효과적으로 전달할 것\r\n3. 간결하면서도 임팩트 있는 표현을 사용할 것\r\n4. 광고 문구에 브랜드명을 포함할 것\n\n\n3가지 사용자 입력은 다음과 같습니다.\n1. 분류: 브랜드의 업종 분류\n2. 브랜드: 브랜드 이름\n3. 스타일: 광고 문구의 스타일\n스타일은 다음을 의미합니다.\n- 선점 : 다른 브랜드 대비 선점\n- 기능 : 제품의 기능을 강조\n- 감성 : 제품의 감성적인 터치를 강조\r\n- 사운드 : 사운드 효과 강조\r\n- 언어유희 : 동음이의어 등 언어 유희 이용\n- 영어: 영어를 이용\n\n\n###\n분류: 화장품\n브랜드: 이니스프리\n스타일: 감성\n광고카피: 나의 제주 이야기가 스며든 피부, 이니스프리\n###\n분류: 식품/제과\n브랜드: 코카콜라\n스타일: 언어유희\n광고카피: 코카콜라와 함께 무한탄산 무한텐션\n###\n분류: 정보통신\n브랜드: G마켓\n스타일: 선점\n광고카피: 지상 최대의 선물마켓, G마켓\n###\n분류: 전기전자\n브랜드: 애플 아이폰\n스타일: 영어\n광고카피: Your New Superpower\n###\n\n"},
                   {"role": "user", "content": format_fix(response['received_data'])}]

    request_data = {
        'messages': preset_text,
        'topP': 0.8,
        'topK': 0,
        'maxTokens': 256,
        'temperature': 1.0,
        'repeatPenalty': 5.0,
        'stopBefore': ["###"],
        'includeAiFilters': True,
        'seed': 0
    }

    # print(preset_text)
    result_str = completion_executor.execute(request_data)
    print(result_str)
    print("-------------------------------------")
    print(parse_event_data(result_str))
    print("-------------------------------------")
    return response


def parse_event_data(event_data: str) -> str:
    # Split the data into lines
    lines = event_data.split('\n')
    print(lines)
    # Iterate through lines to find the line that starts with 'event:result'
    for i, line in enumerate(lines):

        if line.startswith("event:result"):
            # The next line contains the data we need
            result_line = lines[i + 1]
            # Extract the JSON part of the result_line
            json_part = result_line.split('data:', 1)[1]
            # Load the JSON data
            json_data = json.loads(json_part)
            # Return the content value
            return json_data["message"]["content"]

    return ""
