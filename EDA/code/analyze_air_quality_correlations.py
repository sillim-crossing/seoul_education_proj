# 추가: 공기질 상관관계 분석 함수
def analyze_air_quality_correlations(results):
    """공기질 지표 간 상관관계 및 특성 분석 함수"""

    # 분석에 사용할 수치형 컬럼 선택
    numeric_cols = [
        'PM10_교실_최대값', 'PM10_체육관_최대값', 'PM2.5_최대값',
        'CO2_최대값', 'CO_최대값', 'NO2_최대값', 'O3_최대값',
        '종합_점수', '부적합_항목수'
    ]

    # 충분한 데이터가 있는 컬럼만 필터링
    valid_cols = []
    for col in numeric_cols:
        if col in results.columns and results[col].notna().sum() >= 10:
            valid_cols.append(col)

    if len(valid_cols) < 3:
        print("상관관계 분석을 위한 충분한 데이터가 없습니다.")
        return

    # 상관관계 분석용 데이터프레임 생성
    corr_data = results[valid_cols].copy()

    # 1. 상관관계 히트맵
    plt.figure(figsize=(12, 10))
    corr_matrix = corr_data.corr()
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(
        corr_matrix,
        mask=mask,
        annot=True,
        fmt='.2f',
        cmap='coolwarm',
        vmin=-1,
        vmax=1,
        square=True,
        linewidths=.5
    )
    plt.title('공기질 지표 간 상관관계', fontsize=16)
    plt.tight_layout()
    plt.show()

    # 2. 주요 오염물질 간 산점도 행렬
    scatter_cols = [col for col in ['PM10_교실_최대값', 'PM2.5_최대값', 'CO2_최대값', '종합_점수']
                   if col in valid_cols]

    if len(scatter_cols) >= 3:
        plt.figure(figsize=(14, 12))
        scatter_data = results[scatter_cols].copy()

        # 자치구 정보가 있으면 색상 구분
        if '자치구' in results.columns:
            # 데이터가 충분한 상위 5개 자치구만 선택
            top_districts = results['자치구'].value_counts().nlargest(5).index.tolist()
            scatter_data = results[scatter_cols + ['자치구']].copy()
            scatter_data = scatter_data[scatter_data['자치구'].isin(top_districts)]

            # 산점도 행렬 그리기 (자치구별 색상 구분)
            sns.pairplot(
                scatter_data,
                hue='자치구',
                diag_kind='kde',
                plot_kws={'alpha': 0.6, 's': 80, 'edgecolor': 'w'},
                diag_kws={'alpha': 0.6, 'linewidth': 2}
            )
            plt.suptitle('주요 공기질 지표 간 관계 (자치구별)', fontsize=16, y=1.02)
        else:
            # 자치구 정보가 없는 경우
            sns.pairplot(
                scatter_data,
                diag_kind='kde',
                plot_kws={'alpha': 0.6, 's': 80, 'edgecolor': 'w'},
                diag_kws={'alpha': 0.6, 'linewidth': 2}
            )
            plt.suptitle('주요 공기질 지표 간 관계', fontsize=16, y=1.02)

        plt.tight_layout()
        plt.show()

    # 3. 학교유형별 공기질 상관관계 (학교유형 정보가 있는 경우)
    if '학교유형' in results.columns:
        school_types = results['학교유형'].value_counts()
        valid_types = school_types[school_types >= 10].index.tolist()

        if len(valid_types) >= 2:
            # 학교유형별 상관관계 분석
            for school_type in valid_types:
                type_data = results[results['학교유형'] == school_type][valid_cols]

                if len(type_data) >= 10:  # 충분한 데이터가 있는 경우에만
                    plt.figure(figsize=(10, 8))
                    type_corr = type_data.corr()
                    mask = np.triu(np.ones_like(type_corr, dtype=bool))
                    sns.heatmap(
                        type_corr,
                        mask=mask,
                        annot=True,
                        fmt='.2f',
                        cmap='coolwarm',
                        vmin=-1,
                        vmax=1,
                        square=True,
                        linewidths=.5
                    )
                    plt.title(f'{school_type} 공기질 지표 간 상관관계', fontsize=16)
                    plt.tight_layout()
                    plt.show()

    # 4. 자치구별 공기질 상관관계 (주요 자치구 대상)
    if '자치구' in results.columns:
        district_counts = results['자치구'].value_counts()
        main_districts = district_counts[district_counts >= 15].index.tolist()
        main_districts = [d for d in main_districts if d != "정보 없음"]

        if len(main_districts) >= 3:
            # 상관관계가 가장 높은/낮은 자치구 찾기
            district_corrs = {}

            for district in main_districts:
                district_data = results[results['자치구'] == district][valid_cols]
                if len(district_data) >= 10:  # 충분한 데이터가 있는 경우
                    # PM10과 PM2.5 간 상관관계 계산
                    if 'PM10_교실_최대값' in valid_cols and 'PM2.5_최대값' in valid_cols:
                        corr = district_data['PM10_교실_최대값'].corr(district_data['PM2.5_최대값'])
                        district_corrs[district] = corr

            # 상관관계 기준 정렬
            sorted_districts = sorted(district_corrs.items(), key=lambda x: x[1], reverse=True)

            # 상관관계가 가장 높은 3개, 가장 낮은 3개 자치구 시각화
            top_districts = [d[0] for d in sorted_districts[:3]]
            bottom_districts = [d[0] for d in sorted_districts[-3:]]

            # 상관관계가 높은 자치구들의 산점도
            if len(top_districts) > 0:
                plt.figure(figsize=(15, 5))
                for i, district in enumerate(top_districts):
                    district_data = results[results['자치구'] == district]
                    plt.subplot(1, len(top_districts), i+1)
                    sns.scatterplot(
                        x='PM10_교실_최대값',
                        y='PM2.5_최대값',
                        data=district_data,
                        alpha=0.7
                    )

                    # 회귀선 추가
                    sns.regplot(
                        x='PM10_교실_최대값',
                        y='PM2.5_최대값',
                        data=district_data,
                        scatter=False,
                        line_kws={"color": "red"}
                    )

                    # 상관계수 표시
                    corr = district_data['PM10_교실_최대값'].corr(district_data['PM2.5_최대값'])
                    plt.title(f'{district}\n상관계수: {corr:.2f}', fontsize=12)
                    plt.grid(True, alpha=0.3)

                plt.suptitle('미세먼지(PM10)와 초미세먼지(PM2.5) 상관관계가 높은 자치구', fontsize=16)
                plt.tight_layout()
                plt.subplots_adjust(top=0.85)
                plt.show()

            # 상관관계가 낮은 자치구들의 산점도
            if len(bottom_districts) > 0:
                plt.figure(figsize=(15, 5))
                for i, district in enumerate(bottom_districts):
                    district_data = results[results['자치구'] == district]
                    plt.subplot(1, len(bottom_districts), i+1)
                    sns.scatterplot(
                        x='PM10_교실_최대값',
                        y='PM2.5_최대값',
                        data=district_data,
                        alpha=0.7
                    )

                    # 회귀선 추가
                    sns.regplot(
                        x='PM10_교실_최대값',
                        y='PM2.5_최대값',
                        data=district_data,
                        scatter=False,
                        line_kws={"color": "red"}
                    )

                    # 상관계수 표시
                    corr = district_data['PM10_교실_최대값'].corr(district_data['PM2.5_최대값'])
                    plt.title(f'{district}\n상관계수: {corr:.2f}', fontsize=12)
                    plt.grid(True, alpha=0.3)

                plt.suptitle('미세먼지(PM10)와 초미세먼지(PM2.5) 상관관계가 낮은 자치구', fontsize=16)
                plt.tight_layout()
                plt.subplots_adjust(top=0.85)
                plt.show()
