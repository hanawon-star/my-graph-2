st.divider()

# ---------------------------------------------------------
# 섹션 8: 인기 장르 상위 5개의 3D 지표 관계 그래프
# ---------------------------------------------------------
st.header("8. 인기 장르 상위 5개의 3D 지표 비교 (스크린수 x 상영횟수 x 총관객수)")

# 데이터셋 내 연령/성별 열 부재 관련 안내 메시지
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
        
        # 인사이트 문구 추가
        st.info(f"💡 **이 그래프로 알 수 있는 것:** {genre_name} 장르 상위 10개 영화의 초기 스크린/상영 횟수 확보 수준과 최종 총 관객수 간의 3차원적 관계를 입체적으로 비교할 수 있습니다.")
