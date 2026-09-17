import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide"
)

# 메인 타이틀
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.write("박스오피스 상위권 영화 데이터를 통해 장르별 분포 및 여러 지표 간의 관계를 탐색합니다.")

# 데이터 불러오기 함수 (캐싱 적용)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # genre 열 전처리: 세로막대(|) 기호로 묶인 여러 장르 중 첫 번째 장르만 추출
    df['genre'] = df['genre'].astype(str).apply(lambda x: x.split('|')[0].strip())
    return df

df = load_data()

# 데이터 요약 정보 확인 (선택 사항)
with st.expander("📄 원본 데이터 미리보기"):
    st.dataframe(df)

st.divider()

# ---------------------------------------------------------
# 섹션 1: 장르별 영화 편수 (도넛 차트)
# ---------------------------------------------------------
st.header("1. 장르별 영화 편수 분포")

# 장르별 영화 편수 집계
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['장르', '영화편수']

# Plotly 도넛 차트 생성
fig_donut = px.pie(
    genre_counts,
    values='영화편수',
    names='장르',
    hole=0.4,
    title="장르별 영화 비율 및 편수"
)

# 마우스 오버 시 편수와 비율이 모두 표기되도록 설정
fig_donut.update_traces(
    hoverinfo='label+value+percent',
    textinfo='percent+label',
    hovertemplate="<b>장르:</b> %{label}<br><b>편수:</b> %{value}편<br><b>비율:</b> %{percent}"
)

# Streamlit에 그래프 출력
st.plotly_chart(fig_donut, use_container_width=True)

# 그래프 해석 및 인사이트 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 개봉한 박스오피스 상위 영화 중 어떤 장르가 가장 높은 비중을 차지하는지 장르별 편수와 비율로 쉽게 파악할 수 있습니다.")

st.divider()

# ---------------------------------------------------------
# 추가 탐색 섹션 (추후 다른 분포/관계 그래프 추가 공간)
# ---------------------------------------------------------
st.header("2. 관객 수와 스크린 수의 관계")

# 예시: 개봉일 스크린수와 총 관객수 간 상관관계 산점도
fig_scatter = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    color='genre',
    hover_data=['movieNm'],
    labels={'first_scrn': '개봉일 스크린수', 'total_audi': '총 관객수', 'genre': '장르'},
    title="개봉일 스크린수 vs 총 관객수"
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 개봉일 스크린수가 확보될수록 총 관객수가 증가하는 경향을 보이지만, 장르 및 영화별 흥행 성과에 따라 상이할 수 있습니다.")
