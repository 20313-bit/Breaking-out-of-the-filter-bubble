import streamlit as st

# 1. 페이지 기본 설정 (와이드 모드)
st.set_page_config(
    page_title="디지털 뉴스 비판적 사고 가이드",
    page_icon="📰",
    layout="wide"
)

# 2. 앱 제목 및 설명
st.title("🔍 뉴스 비판적 사고 훈련 도우미")
st.markdown("""
소셜 미디어나 디지털 뉴스를 읽을 때 무비판적으로 수용하지 않도록 돕는 앱입니다. 
아래 기사를 읽으며 **오른쪽의 비판적 사고 알림창**을 확인해 보세요.
""")

st.write("---")

# 3. 가상의 뉴스 데이터 구성 (실제 앱에서는 DB나 API 연동 가능)
news_title = "[단독] 역대급 AI 혁명, 5년 내 인간 일자리 90% 완전히 대체한다?!"
news_meta = "발행일: 2026.07.09 | 작성자: 미래경제연구팀"

# 각 문단별 텍스트와 비판적 알림 메시지 매핑
news_paragraphs = [
    {
        "id": 1,
        "text": "최근 한 연구소의 발표에 따르면, 인공지능(AI) 기술의 급격한 발전으로 인해 향후 5년 안에 현재 인류가 가진 일자리의 90%가 문자 그대로 '완전히' 사라질 것이라는 충격적인 전망이 나왔다.",
        "has_alert": True,
        "alert_type": "warning",
        "alert_title": "⚠️ 과장 및 공포 유발 (Sensationalism)",
        "alert_msg": "'90% 완전히 대체'라는 극단적인 수치는 대중의 공포심을 자극하는 표현일 수 있습니다. 해당 수치를 도출한 연구소의 신뢰도와 구체적인 통계적 근거가 있는지 확인이 필요합니다."
    },
    {
        "id": 2,
        "text": "익명을 요구한 한 IT 업계 전문가는 '이 변화에 당장 대비하지 않는 기업과 개인은 무조건 도태될 것'이라며 '지금 당장 모든 자산을 AI 관련 분야로 전환해야 한다'고 강력히 경고했다.",
        "has_alert": True,
        "alert_type": "error",
        "alert_title": "🚨 신뢰할 수 없는 출처 및 흑백논리",
        "alert_msg": "'익명의 전문가'는 책임 소재가 불분명하여 신뢰성이 떨어집니다. 또한 '대비하지 않으면 무조건 도태된다'는 식의 이분법적 주장은 전형적인 논리적 오류입니다."
    },
    {
        "id": 3,
        "text": "한편, 기술 발전에 따른 부작용을 최소화하기 위해 정부 차원의 가이드라인 마련과 사회적 안전망 구축이 시급하다는 목소리도 점차 힘을 얻고 있다.",
        "has_alert": False,
        "alert_type": "info",
        "alert_title": "✅ 비교적 객관적인 서술",
        "alert_msg": "문제를 해결하기 위한 제도적 대안을 언급하는 부분으로, 비교적 균형 잡힌 시각을 보여줍니다."
    }
]

# 4. 화면 레이아웃 분할 (좌측: 뉴스 본문 / 우측: 비판적 판단 알림창)
col1, col2 = st.columns([5, 4], gap="large")

with col1:
    st.subheader("📰 뉴스 기사 본문")
    
    # 기사 헤더
    st.error(f"### {news_title}")
    st.caption(news_meta)
    st.markdown("---")
    
    # 본문 출력 (알림이 필요한 문단은 배경색 하이라이트)
    for p in news_paragraphs:
        if p["has_alert"]:
            # HTML을 이용해 노란색 배경으로 강조
            st.markdown(
                f"""
                <div style="background-color: #fff3cd; padding: 15px; border-left: 5px solid #ffc107; border-radius: 4px; margin-bottom: 15px;">
                    <strong>[문단 {p['id']}]</strong> {p['text']}
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style="padding: 15px; margin-bottom: 15px; line-height: 1.6;">
                    <strong>[문단 {p['id']}]</strong> {p['text']}
                </div>
                """, 
                unsafe_allow_html=True
            )

with col2:
    st.subheader("💡 비판적 사고 가이드라인")
    st.write("각 문단을 읽을 때 주의해야 할 포인트입니다.")
    st.markdown("---")
    
    # 오른쪽 칸에 각 문단에 매칭되는 알림창 배치
    for p in news_paragraphs:
        if p["alert_type"] == "error":
            st.error(f"**{p['alert_title']} (문단 {p['id']})**\n\n{p['alert_msg']}")
        elif p["alert_type"] == "warning":
            st.warning(f"**{p['alert_title']} (문단 {p['id']})**\n\n{p['alert_msg']}")
        else:
            st.info(f"**{p['alert_title']} (문단 {p['id']})**\n\n{p['alert_msg']}")

# 5. 하단 팁 세션
st.write("---")
st.subheader("📌 디지털 뉴스를 볼 때 항상 스스로 던져야 할 질문")
st.markdown("""
* **출처가 명확한가?** (공신력 있는 기관, 실명 전문가 등)
* **감정적인 단어를 사용하는가?** ('충격', '경악', '무조건' 등)
* **반대 편의 의견도 공정하게 다루고 있는가?**
""")
