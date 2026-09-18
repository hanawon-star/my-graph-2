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
    
    # genre 열 전처리: .str 메서드를 사용해 첫 번째 장르만 추출 (최신 pandas 오류 해결)
    df['genre'] = df['genre'].fillna('').astype(str).str.split('|').str[0].str.strip()
    return df

df = load_data()

# 데이터 요약 정보 확인
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

# 마우스 오버 시 편수와 비율 표기
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
# 섹션 2: 장르 및 영화별 총 관객수 분포 (트리맵)
# ---------------------------------------------------------
st.header("2. 장르별 영화 계층 및 총 관객수 분포")

# Plotly 트리맵 차트 생성 (장르 -> 영화명 계층 구조)
fig_treemap = px.treemap(
    df,
    path=[px.Constant("전체 장르"), 'genre', 'movieNm'],
    values='total_audi',
    color='genre',
    title="장르 및 영화별 총 관객수 (크기: 총 관객수)"
)

# 마우스 오버 시 영화명과 총 관객수 표시
fig_treemap.update_traces(
    hovertemplate="<b>영화명/구분:</b> %{label}<br><b>총 관객수:</b> %{value:,}명<extra></extra>"
)

# Streamlit에 그래프 출력
st.plotly_chart(fig_treemap, use_container_width=True)

# 그래프 해석 및 인사이트 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 각 장르가 전체 관객수에서 차지하는 지분과, 해당 장르 내에서 어떤 영화가 흥행을 주도했는지 면적의 크기로 한눈에 비교할 수 있습니다.")

st.divider()

# ---------------------------------------------------------
# 섹션 3: 총 관객수 분포 (히스토그램)
# ---------------------------------------------------------
st.header("3. 총 관객수 분포")

# Plotly 히스토그램 생성
fig_hist = px.histogram(
    df,
    x='total_audi',
    nbins=30,
    title="총 관객수 구간별 영화 편수 분포",
    labels={'total_audi': '총 관객수', 'count': '영화 수'},
    color_discrete_sequence=['#636EFA']
)

fig_hist.update_layout(
    xaxis_title="총 관객수 (명)",
    yaxis_title="영화 수 (편)",
    bargap=0.1
)

# Streamlit에 그래프 출력
st.plotly_chart(fig_hist, use_container_width=True)

# 데이터 기반 최고 관객수 영화 정보 추출
top_movie = df.loc[df['total_audi'].idxmax()]
top_movie_name = top_movie['movieNm']
top_movie_audi = top_movie['total_audi']

# 그래프 해석 및 인사이트 구역
st.info(
    f"💡 **이 그래프로 알 수 있는 것:** 대부분의 영화는 관객수 하위 구간(약 100만~300만 명 이하)에 촘촘히 몰려 있는 양극화 구조를 보이며, "
    f"가장 관객 수가 많은 영화는 **'{top_movie_name}'**(총 {top_movie_audi:,}명)입니다."
)

st.divider()

# ---------------------------------------------------------
# 섹션 4: 개봉일 스크린수와 총 관객수의 관계 (산점도)
# ---------------------------------------------------------
st.header("4. 개봉일 스크린수와 총 관객수의 관계")

# Plotly 산점도 생성
fig_scatter = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    title="개봉일 스크린수 vs 총 관객수",
    labels={
        'first_scrn': '개봉일 스크린수',
        'total_audi': '총 관객수',
        'genre': '장르'
    }
)

# 마우스 오버 툴팁 서식 설정
fig_scatter.update_traces(
    hovertemplate="<b>%{hovertext}</b><br><br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명<extra></extra>"
)

fig_scatter.update_layout(
    xaxis_title="개봉일 스크린수 (개)",
    yaxis_title="총 관객수 (명)"
)

# Streamlit에 그래프 출력
st.plotly_chart(fig_scatter, use_container_width=True)

# 그래프 해석 및 인사이트 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 개봉일 스크린수가 많을수록 총 관객수도 함께 증가하는 양의 상관관계를 보이며, 장르에 따라서도 분포 차이가 나타남을 확인할 수 있습니다.")

st.divider()

# ---------------------------------------------------------
# 섹션 5: 주요 장르별 총 관객수 분포 (박스플롯)
# ---------------------------------------------------------
st.header("5. 주요 장르별 총 관객수 분포 (10편 이상 장르)")

# 영화 수 10편 이상인 장르만 필터링
genre_counts_series = df['genre'].value_counts()
major_genres = genre_counts_series[genre_counts_series >= 10].index
df_filtered = df[df['genre'].isin(major_genres)]

# Plotly 상자 그림(Box Plot) 생성
fig_box = px.box(
    df_filtered,
    x='genre',
    y='total_audi',
    color='genre',
    points='outliers',
    hover_name='movieNm',
    title="주요 장르별 총 관객수 박스플롯",
    labels={
        'genre': '장르',
        'total_audi': '총 관객수'
    }
)

# 툴팁 및 마우스 오버 서식 설정
fig_box.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>총 관객수: %{y:,}명<extra></extra>"
)

fig_box.update_layout(
    xaxis_title="장르",
    yaxis_title="총 관객수 (명)",
    showlegend=False
)

# Streamlit에 그래프 출력
st.plotly_chart(fig_box, use_container_width=True)

# 그래프 해석 및 인사이트 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 주요 장르별 관객수의 중위수와 편차를 한눈에 볼 수 있으며, 상자 밖으로 튀어나온 이상치(Outlier) 점들을 통해 장르 평균을 뛰어넘는 대흥행작들을 식별할 수 있습니다.")

st.divider()

# ---------------------------------------------------------
# 섹션 6: 스크린수, 총 관객수 및 첫 주 관객수 (버블 차트)
# ---------------------------------------------------------
st.header("6. 개봉일 스크린수, 총 관객수 및 첫 주 관객수의 관계 (버블 차트)")

# Plotly 버블 차트 생성 (size=first_week_audi)
fig_bubble = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    size='first_week_audi',
    color='genre',
    hover_name='movieNm',
    size_max=40,
    title="개봉일 스크린수 vs 총 관객수 (원 크기: 개봉 첫 주 관객수)",
    labels={
        'first_scrn': '개봉일 스크린수',
        'total_audi': '총 관객수',
        'genre': '장르',
        'first_week_audi': '첫 주 관객수'
    }
)

# 마우스 오버 툴팁 서식 설정
fig_bubble.update_traces(
    hovertemplate="<b>%{hovertext}</b><br><br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명<br>첫 주 관객수: %{marker.size:,}명<extra></extra>"
)

fig_bubble.update_layout(
    xaxis_title="개봉일 스크린수 (개)",
    yaxis_title="총 관객수 (명)"
)

# Streamlit에 그래프 출력
st.plotly_chart(fig_bubble, use_container_width=True)

# 그래프 해석 및 인사이트 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 개봉일 스크린수와 총 관객수 외에도 원의 크기를 통해 개봉 첫 주 초반 흥행 동력(첫 주 관객수)이 최종 총 관객수에 미친 영향을 다차원적으로 파악할 수 있습니다.")

st.divider()

# ---------------------------------------------------------
# 섹션 7: 제작 국가 및 장르별 영화 편수 (선버스트 차트)
# ---------------------------------------------------------
st.header("7. 제작 국가 및 장르별 영화 편수 분포 (선버스트 차트)")

# 국가별, 장르별 영화 편수 집계
nation_genre_counts = df.groupby(['nation', 'genre']).size().reset_index(name='movie_count')

# Plotly 선버스트 차트 생성 (국가 -> 장르 계층 구조)
fig_sunburst = px.sunburst(
    nation_genre_counts,
    path=['nation', 'genre'],
    values='movie_count',
    title="제작 국가 및 장르별 영화 편수 (크기: 영화 편수)"
)

# 마우스 오버 툴팁 서식 설정
fig_sunburst.update_traces(
    hovertemplate="<b>구분:</b> %{label}<br><b>영화 편수:</b> %{value}편<extra></extra>"
)

# Streamlit에 그래프 출력
st.plotly_chart(fig_sunburst, use_container_width=True)

# 그래프 해석 및 인사이트 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 각 제작 국가가 전체 영화 중 차지하는 비율과 함께, 해당 국가 내에서 어떤 장르의 영화가 주로 개봉했는지 계층적인 원형 구조로 쉽게 파악할 수 있습니다.")

st.divider()

# ---------------------------------------------------------
# 섹션 8: 인기 장르 상위 5개의 3D 지표 관계 그래프
# ---------------------------------------------------------
st.header("8. 인기 장르 상위 5개의 3D 지표 비교 (스크린수 x 상영횟수 x 총관객수)")

st.caption("※ 원본 데이터셋에 연령 및 성별 정보가 없어, 영화 관련 주요 3개 수치 지표(스크린수, 상영횟수, 총관객수)로 3D 축을 구성했습니다.")

# 영화 편수 기준 상위 5개 장르 추출
top5_genres = df['genre'].value_counts().head(5).index.tolist()

# 탭을 생성하여 장르별로 5가지 그래프 구성
tabs = st.tabs([f"TOP {i+1}: {genre}" for i, genre in enumerate(top5_genres)])

for i, genre_name in enumerate(top5_genres):
    with tabs[i]:
        # 해당 장르 데이터 및 총 관객수 기준 상위 10위 영화 추출
        genre_df = df[df['genre'] == genre_name].sort_values(by='total_audi', ascending=False).head(10)
        
        # 3D 산점도 그래프 생성
        fig_3d = px.scatter_3d(
            genre_df,
            x='first_scrn',
            y='first_show',
            z='total_audi',
            color='movieNm',
            size='days_in_top10',
            hover_name='movieNm',
            title=f"[{genre_name}] 장르 관객수 TOP 10 영화의 3D 지표 분포",
            labels={
                'first_scrn': '개봉일 스크린수',
                'first_show': '개봉일 상영횟수',
                'total_audi': '총 관객수',
                'days_in_top10': 'Top10 유지일수'
            }
        )
        
        fig_3d.update_traces(
            hovertemplate="<b>%{hovertext}</b><br><br>" +
                          "개봉일 스크린수: %{x:,}개<br>" +
                          "개봉일 상영횟수: %{y:,}회<br>" +
                          "총 관객수: %{z:,}명<extra></extra>"
        )
        
        fig_3d.update_layout(
            height=600,
            scene=dict(
                xaxis_title='개봉일 스크린수',
                yaxis_title='개봉일 상영횟수',
                zaxis_title='총 관객수'
            )
        )
        
        st.plotly_chart(fig_3d, use_container_width=True)
        
        st.info(f"💡 **이 그래프로 알 수 있는 것:** {genre_name} 장르 상위 10개 영화의 초기 스크린/상영 횟수 확보 수준과 최종 총 관객수 간의 3차원적 관계를 입체적으로 비교할 수 있습니다.")
