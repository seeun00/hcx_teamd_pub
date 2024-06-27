# streamlit_app.py
import base64

import streamlit as st
import requests

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

def get_image_as_base64(file_path: str) -> str:
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
image_path = "/Users/handohyeong/projects/dumb_d/dohyeong/dumbd_image.webp"
image_base64 = get_image_as_base64(image_path)

st.markdown('<div class="container">', unsafe_allow_html=True)
st.markdown('<h1>외로운 대행사의 카피라이터, 김카피</h1>', unsafe_allow_html=True)
st.markdown(f'<img src="data:image/webp;base64,{image_base64}" alt="profile-pic">', unsafe_allow_html=True)
st.markdown('<p>또 왔네? 광고 카피가 그냥 자판기 버튼 누르면 나오는 줄 아는구나.. 응 실은 맞아....<br><br>최근 광고 카피를 학습하여 알맞은 카피를 제공합니다. 최대한 많은 정보를 제공해주세요.</p>', unsafe_allow_html=True)
with (st.form("input_form")):
    분류 = st.selectbox("업종 선택", ["화장품", "식품\제과", "전기전자"])
    브랜드 = st.text_input("브랜드")
    스타일 = st.selectbox("선택", ["감성", "언어유희", "선언"])
    submitted = st.form_submit_button("작성")

if submitted:
    # 입력된 데이터를 JSON 형태로 생성
    input_data = {
        "분류": 분류,
        "브랜드": 브랜드,
        "스타일": 스타일
    }

    # FastAPI 서버로 데이터 전송
    response = requests.post("http://localhost:8000/execute", json=input_data)

    if response.status_code == 200:
        response_data = response.json()
        st.success("응답 받음: {}".format(response_data))

        st.write(response_data)
    else:
        st.error("오류 발생: {}".format(response.status_code))
