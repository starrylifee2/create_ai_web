import streamlit as st
from openai import OpenAI
import base64

# 사이드바에서 API 키 입력 받기
st.sidebar.title("API 설정")
api_key = st.sidebar.text_input("OpenAI API 키를 입력하세요", type="password")

# API 키가 입력되었는지 확인
if api_key:
    # OpenAI 클라이언트 초기화
    client = OpenAI(api_key=api_key)

    # Streamlit 페이지 제목 설정
    st.title("DALL-E 3 이미지 분석 및 생성기")

    # 이미지 파일 업로드 받기
    uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # 이미지 파일을 base64로 인코딩
        base64_image = base64.b64encode(uploaded_file.read()).decode('utf-8')

        # OpenAI API를 사용하여 이미지 분석
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "이미지를 자세히 분석해주세요."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )

        # 결과 출력
        st.subheader("이미지 분석 결과")
        analysis_result = response.choices[0].message.content
        st.write(analysis_result)

        # 분석된 텍스트를 바탕으로 이미지 생성
        if st.button("분석된 텍스트로 이미지 생성"):
            # OpenAI API를 사용하여 이미지 생성
            response = client.images.generate(
                model="dall-e-3",
                prompt=analysis_result,
                size="1024x1024",
                quality="standard",
                n=1,
            )

            # 생성된 이미지 URL 가져오기
            image_url = response.data[0].url

            # 이미지 출력
            st.image(image_url, caption=f"Generated Image: {analysis_result}")

    # 사용자 입력 받기
    prompt = st.text_input("이미지 생성 프롬프트를 입력하세요", "a white siamese cat")

    # 사용자에게 팔다리를 추가할 물건 선택 받기
    add_limbs = st.checkbox("물건에 팔다리를 추가하시겠습니까?")

    # 버튼을 클릭했을 때 이미지 생성
    if st.button("이미지 생성"):
        # 프롬프트 수정: 팔다리를 추가하는 경우
        if add_limbs:
            prompt += ", with arms and legs"

        # OpenAI API를 사용하여 이미지 생성
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        # 생성된 이미지 URL 가져오기
        image_url = response.data[0].url

        # 이미지 출력
        st.image(image_url, caption=f"Generated Image: {prompt}")
else:
    st.warning("API 키를 사이드바에 입력하세요.")