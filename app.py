import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# 1. 페이지 설정
st.set_page_config(
    page_title="실시간 뉴스 비판적 사고 가이드",
    page_icon="🔍",
    layout="wide"
)

# 2. 웹 크롤링 함수 (URL에서 뉴스 본문 추출)
def fetch_news_content(url):
    try:
        # 봇(Bot)으로 오인받아 차단되는 것을 방지하기 위한 헤더 설정
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code != 200:
            return None, None, f"뉴스를 불러오는데 실패했습니다. (에러 코드: {response.status_code})"
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 제목 추출 시도
        title = "제목을 찾을 수 없음"
        if soup.find('h1'):
            title = soup.find('h1').get_text().strip()
        elif soup.find('title'):
            title = soup.find('title').get_text().strip()
            
        # 본문 문단 추출 (<p> 태그 기준)
        paragraphs = []
        p_tags = soup.find_all('p')
        
        for p in p_tags:
            text = p.get_text().strip()
            # 너무 짧은 문장이나 광고성 문구(Copyright 등)는 제외
            if len(text) > 30 and not text.startswith("Copyright") and not text.startswith("▶"):
                # 기자 이메일이나 무의미한 공백 제거 규칙 추가 가능
                paragraphs.append(text)
                
        if not paragraphs:
            return None, None, "기사 본문을 추출하지 못했습니다. 다른 뉴스 사이트 링크를 시도해 주세요."
            
        return title, paragraphs, None
        
    except Exception as e:
        return None, None, f"오류가 발생했습니다: {str(e)}"

# 3. 알고리즘 기반 비판적 요소 분석 함수 (키워드 매칭)
def analyze_text(text):
    alerts = []
    
    # 규칙 1: 익명 출처 검사
    if any(w in text for w in ["익명", "관계자", "측근", "소식통", "한 전문가는"]):
        alerts.append({
            "type": "error",
            "title": "🚨 출처 불분명 (익명 소식통)",
            "msg": "'익명의 관계자'나 '소식통'을 인용한 보도는 책임 소재가 불분명합니다. 주장의 신뢰성을 뒷받침할 구체적인 공공 데이터나 공식 입장이 있는지 교차 검증이 필요합니다."
        })
        
    # 규칙 2: 자극적/감정적 표현 검사
    if any(w in text for w in ["충격", "경악", "발칵", "단독", "세계 최초", "발칵", "멘붕"]):
        alerts.append({
            "type": "warning",
            "title": "⚠️ 자극적인 단어 (감정 유발 광고성 보도)",
            "msg": "'충격', '단독' 등의 표현은 독자의 시선을 끌기 위한 클릭베이트(Clickbait)일 확률이 높습니다. 주관적인 감정 표현을 걷어내고 드라이한 사실(Fact)만 남겨두고 보세요."
        })
        
    # 규칙 3: 극단적 서술 (흑백논리) 검사
    if any(w in text for w in ["무조건", "절대", "완전히", "전부", "하나도"]):
        alerts.append({
            "type": "warning",
            "title": "⚠️ 극단적 어휘 (복잡성 일반화)",
            "msg": "세상사에는 다양한 인과관계가 얽혀 있습니다. '무조건', '완전히'와 같은 이분법적 단어는 사안을 지나치게 단순화하거나 과장했을 가능성이 큽니다."
        })
        
    # 규칙 4: 추측성 보도 검사
    if any(w in text for w in ["~카더라", "전망된다", "추측된다", "알려졌다", "예상된다"]):
        alerts.append({
            "type": "info",
            "title": "ℹ️ 확정되지 않은 사실 (추측 보도)",
            "msg": "이 문단은 확정된 사실이 아니라 미래 예측이나 소문을 다루고 있습니다. 공식 발표가 나기 전까지는 하나의 가설로만 받아들이는 것이 좋습니다."
        })
        
    return alerts


# --- UI 레이아웃 구현 ---

st.title("🔍 실시간 뉴스 비판적 사고 가이드 앱")
st.markdown("원하는 뉴스 기사의 전체 링크(URL)를 입력하면 본문을 분석해 비판적 판단이 필요한 구간을 알려줍니다.")

# URL 입력창
target_url = st.text_input("뉴스 URL을 입력하세요:", placeholder="https://example-news.com/article/12345")

if target_url:
    with st.spinner("뉴스를 긁어와 분석하는 중입니다..."):
        title, paragraphs, error = fetch_news_content(target_url)
        
    if error:
        st.error(error)
    else:
        st.success("뉴스 분석 완료!")
        st.markdown(f"### 📰 분석된 기사: {title}")
        st.write("---")
        
        # 화면을 좌우로 분할 (좌: 뉴스 본문, 우: 알림 모아보기)
        col1, col2 = st.columns([5, 4], gap="large")
        
        with col1:
            st.subheader("📝 기사 본문 및 체크 포인트")
            
            for idx, text in enumerate(paragraphs, 1):
                alerts = analyze_text(text)
                
                if alerts:
                    # 경고가 있는 문단은 노란색 하이라이트 박스로 표시
                    st.markdown(
                        f"""
                        <div style="background-color: #fff3cd; padding: 12px; border-left: 5px solid #ffc107; border-radius: 4px; margin-bottom: 12px;">
                            <strong>[문단 {idx}]</strong> {text}
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                else:
                    # 경고가 없는 일반 문단
                    st.markdown(
                        f"<div style='padding: 12px; margin-bottom: 12px; line-height: 1.6;'><strong>[문단 {idx}]</strong> {text}</div>", 
                        unsafe_allow_html=True
                    )
                    
        with col2:
            st.subheader("💡 비판적 사고 알림창")
            st.write("각 문단에서 포착된 주의 사항입니다.")
            st.markdown("---")
            
            has_any_alert = False
            for idx, text in enumerate(paragraphs, 1):
                alerts = analyze_text(text)
                for alert in alerts:
                    has_any_alert = True
                    if alert["type"] == "error":
                        st.error(f"**{alert['title']} (문단 {idx})**\n\n{alert['msg']}")
                    elif alert["type"] == "warning":
                        st.warning(f"**{alert['title']} (문단 {idx})**\n\n{alert['msg']}")
                    else:
                        st.info(f"**{alert['title']} (문단 {idx})**\n\n{alert['msg']}")
                        
            if not has_any_alert:
                st.success("🎉 본문에서 뚜렷한 가짜뉴스 패턴이나 자극적인 표현이 발견되지 않았습니다! 비교적 객관적인 뉴스일 수 있습니다.")
