# streamlit_app.py
import streamlit as st
import requests

st.title("데이터 입력 및 처리")

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
