import streamlit as st
import requests
from bs4 import BeautifulSoup

# 1. 페이지 설정
st.set_page_config(
    page_title="실시간 뉴스 비판적 사고 가이드",
    page_icon="🔍",
    layout="wide"
)

# 2. 웹 크롤링 함수 (보안 우회 헤더 강화)
def fetch_news_content(url):
    try:
        # 실제 사용자가 크롬 브라우저로 접속하는 것처럼 완벽하게 위장합니다.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # 접속 실패 시 즉시 에러 발생
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 제목 추출
        title = soup.find('title').get_text().strip() if soup.find('title') else "제목을 찾을 수 없음"
            
        # 본문 문단 추출
        paragraphs = []
        for p in soup.find_all('p'):
            text = p.get_text().strip()
            if len(text) > 30 and not text.startswith("Copyright") and not text.startswith("▶"):
                paragraphs.append(text)
                
        if not paragraphs:
            return None, None, "본문 추출에 실패했습니다. 해당 언론사가 자동 수집을 강력하게 차단하고 있습니다."
            
        return title, paragraphs, None
        
    except Exception as e:
        return None, None, "해당 링크에 접근할 수 없습니다. (보안 차단 또는 잘못된 주소)"

# 3. 비판적 요소 분석 함수
def analyze_text(text):
    alerts = []
    
    if any(w in text for w in ["익명", "관계자", "측근", "소식통", "한 전문가는"]):
        alerts.append({"type": "error", "title": "🚨 출처 불분명", "msg": "'익명 소식통'을 인용한 보도는 신뢰성을 교차 검증해야 합니다."})
        
    if any(w in text for w in ["충격", "경악", "발
