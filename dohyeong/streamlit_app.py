# streamlit_app.py
import streamlit as st
import requests

st.title("데이터 입력 및 처리")

with st.form("input_form"):
    브랜드명 = st.text_input("브랜드명")
    업종_선택 = st.selectbox("업종 선택", ["value1", "value2", "value3"])
    선택 = st.selectbox("선택", ["value1", "value2", "value3"])
    브랜드_소개 = st.text_area("브랜드 소개")
    submitted = st.form_submit_button("작성")

if submitted:
    # 입력된 데이터를 JSON 형태로 생성
    input_data = {
        "브랜드명": 브랜드명,
        "업종_선택": 업종_선택,
        "선택": 선택,
        "브랜드_소개": 브랜드_소개
    }

    # FastAPI 서버로 데이터 전송
    response = requests.post("http://localhost:8000/execute", json=input_data)

    if response.status_code == 200:
        response_data = response.json()
        st.success("응답 받음: {}".format(response_data))
    else:
        st.error("오류 발생: {}".format(response.status_code))
