# # streamlit_app.py
# import base64

# import streamlit as st
# import requests

# st.markdown("""
#     <style>
#     .main {
#         background-color: #f0f2f6;
#         padding: 10px;
#     }
#     .container {
#         max-width: 600px;
#         margin: auto;
#         padding: 2em;
#         border-radius: 10px;
#         background-color: #2f3147;
#         color: white;
#     }
#     .container h1 {
#         text-align: center;
#         font-size: 1.5em;
#         margin-bottom: 1em;
#     }
#     .container img {
#         display: block;
#         margin-left: auto;
#         margin-right: auto;
#         width: 50%;
#         border-radius: 50%;
#     }
#     .container p {
#         text-align: center;
#         font-size: 1em;
#         margin-bottom: 2em;
#     }
#     .stTextInput, .stSelectbox, .stTextArea, .stButton {
#         margin-bottom: 1.5em;
#     }
#     .stButton button {
#         background-color: #e91e63;
#         color: white;
#         border: none;
#         padding: 0.5em 1em;
#         border-radius: 5px;
#     }
#     </style>
# """, unsafe_allow_html=True)

# streamlit_app.py
import base64
import io

import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageOps

fastapi_url = "https://seeun.pythonanywhere.com"
st.markdown(f"""
    <style>

    .stButton button {{
        background-color: #e91e63;
        color: white;
        border: none;
        padding: 0.5em 1em;
        border-radius: 5px;
    }}
    </style>
""", unsafe_allow_html=True)

def get_image_as_base64(file_path: str, output_size: tuple) -> str:
    with Image.open(file_path) as img:
        img = img.resize(output_size)

        buffered = io.BytesIO()
        img.save(buffered, format="WEBP")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
image_path = "./dumbd_image.webp"
output_size = (400,400)
image_base64 = get_image_as_base64(image_path, output_size)



st.markdown('<div class="container">', unsafe_allow_html=True)
st.markdown('<h1>외로운 대행사의 카피라이터, 김카피</h1>', unsafe_allow_html=True)
# st.markdown(f'<img src="data:image/webp;base64,{image_base64}" alt="profile-pic">', unsafe_allow_html=True)

st.markdown(
    f"""
    <style>
    .centered {{
        display: flex;
        justify-content: center;
        align-items: center;
        # height: 100vh;
    }}
    </style>
    <div class="centered">
        <img src="data:image/webp;base64,{image_base64}" alt="centered image">
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown('<br>', unsafe_allow_html=True)
st.markdown("""
<style>
    .center-text {
        text-align: center;
        font-size: 16px;
        font-family: Arial, sans-serif;
    }
    </style>
<p class="center-text">또 왔네? 광고 카피가 그냥 자판기 버튼 누르면 나오는 줄 아는구나.. 응 실은 맞아....
<br><br>*최근 광고 카피를 학습하여 알맞은 카피를 제공합니다. 최대한 많은 정보를 제공해주세요.</p>

""", unsafe_allow_html=True)
with (st.form("input_form")):
    분류 = st.selectbox("업종 선택", ["화장품", "식품\제과", "전기전자"])
    브랜드 = st.text_input("브랜드 입력")
    스타일 = st.selectbox("스타일 선택", ["감성", "언어유희", "선언"])
    submitted = st.form_submit_button("작성")

if submitted:
    # 입력된 데이터를 JSON 형태로 생성
    input_data = {
        "분류": 분류,
        "브랜드": 브랜드,
        "스타일": 스타일
    }

    # FastAPI 서버로 데이터 전송
    response = requests.post(f"{fastapi_url}/execute", json=input_data)

    if response.status_code == 200:
        response_data = response.json()
        # st.success("응답 받음: {}".format(response_data))

        result_box = f"""
            <style>
            .result-box {{
                border: 2px solid #4CAF50;
                padding: 10px;
                border-radius: 5px;
                # background-color: #f9f9f9;
                margin-top: 20px;
                font-family: Arial, sans-serif;
            }}
            .result-title {{
                font-size: 20px;
                font-weight: bold;
                color: #4CAF50;
            }}
            .result-content {{
                margin-top: 10px;
                font-size: 20px;
            }}
            </style>
            <div class="result-box">
                <div class="result-title">카피라이팅 결과</div>
                <div class="result-content">{response_data['data']}</div>
            </div>
            """

        # 결과 폼 표시
        st.markdown(result_box, unsafe_allow_html=True)
    else:
        st.error("오류 발생: {}".format(response.status_code))