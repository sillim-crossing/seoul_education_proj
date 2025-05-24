# 지역별 공기질 시각화 함수
def visualize_district_analysis(results):
    # '정보 없음' 및 데이터가 매우 적은 자치구 제외
    district_counts = results['자치구'].value_counts()
    valid_districts = district_counts[district_counts >= 3].index.tolist()
    filtered_results = results[results['자치구'].isin(valid_districts)]

    if len(valid_districts) < 2:
        print("자치구 정보가 충분하지 않습니다. 데이터를 확인해주세요.")
        return

    filtered_results = results[results['자치구'].isin(valid_districts)]

    # 1. 자치구별 공기질 종합 점수 평균 비교
    plt.figure(figsize=(14, 8))
    district_scores = filtered_results.groupby('자치구')['종합_점수'].mean().sort_values(ascending=False)

    # 색상 맵 설정 (점수가 높을수록 빨간색, 낮을수록 파란색)
    colors = plt.cm.RdYlBu_r(np.linspace(0, 1, len(district_scores)))

    ax = district_scores.plot(kind='bar', color=colors)
    plt.title('자치구별 공기질 종합 점수 평균 (점수가 높을수록 나쁨)', fontsize=16)
    plt.xlabel('자치구', fontsize=14)
    plt.ylabel('평균 종합 점수', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # 서울시 평균 표시
    seoul_avg = filtered_results['종합_점수'].mean()
    plt.axhline(y=seoul_avg, color='r', linestyle='--', label=f'서울시 평균: {seoul_avg:.2f}')
    plt.legend(fontsize=12)

    # 값 표시
    for i, v in enumerate(district_scores):
        ax.text(i, v + 0.05, f'{v:.2f}', ha='center', fontsize=11)

    plt.tight_layout()
    plt.show()

    # 2. 자치구별 부적합 항목 비율
    plt.figure(figsize=(14, 8))

    # 자치구별 부적합 항목 수 및 비율 계산
    district_unsuitable = filtered_results.groupby('자치구')['부적합_항목수'].mean().sort_values(ascending=False)

    ax = district_unsuitable.plot(kind='bar', color=plt.cm.Reds(np.linspace(0.3, 0.9, len(district_unsuitable))))
    plt.title('자치구별 평균 부적합 항목 수', fontsize=16)
    plt.xlabel('자치구', fontsize=14)
    plt.ylabel('평균 부적합 항목 수', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # 서울시 평균 표시
    seoul_avg_unsuitable = filtered_results['부적합_항목수'].mean()
    plt.axhline(y=seoul_avg_unsuitable, color='r', linestyle='--',
                label=f'서울시 평균: {seoul_avg_unsuitable:.2f}')
    plt.legend(fontsize=12)

    # 값 표시
    for i, v in enumerate(district_unsuitable):
        ax.text(i, v + 0.05, f'{v:.2f}', ha='center', fontsize=11)

    plt.tight_layout()
    plt.show()

    # 3. 자치구별 미세먼지(PM10) 농도 평균 비교
    plt.figure(figsize=(14, 8))

    # 자치구별 미세먼지 농도 평균 계산
    district_pm10 = filtered_results.groupby('자치구')['PM10_교실_최대값'].mean().sort_values(ascending=False)

    # 색상 맵 설정 (농도가 높을수록 빨간색)
    colors = plt.cm.YlOrRd(np.linspace(0.3, 0.9, len(district_pm10)))

    ax = district_pm10.plot(kind='bar', color=colors)
    plt.title('자치구별 교실 미세먼지(PM10) 평균 농도', fontsize=16)
    plt.xlabel('자치구', fontsize=14)
    plt.ylabel('평균 미세먼지 농도(μg/㎥)', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # 기준선 표시
    plt.axhline(y=75, color='red', linestyle='--', label='적합 기준(75μg/㎥)')
    plt.axhline(y=50, color='orange', linestyle='--', label='WHO 권고 기준(50μg/㎥)')

    # 서울시 평균 표시
    seoul_avg_pm10 = filtered_results['PM10_교실_최대값'].mean()
    plt.axhline(y=seoul_avg_pm10, color='green', linestyle='-.',
                label=f'서울시 평균: {seoul_avg_pm10:.2f}μg/㎥')

    plt.legend(fontsize=12)

    # 값 표시
    for i, v in enumerate(district_pm10):
        ax.text(i, v + 1, f'{v:.1f}', ha='center', fontsize=11)

    plt.tight_layout()
    plt.show()

    # 4. 자치구별 초미세먼지(PM2.5) 농도 평균 비교
    plt.figure(figsize=(14, 8))

    # 자치구별 초미세먼지 농도 평균 계산
    district_pm25 = filtered_results.groupby('자치구')['PM2.5_최대값'].mean().sort_values(ascending=False)

    # 색상 맵 설정 (농도가 높을수록 빨간색)
    colors = plt.cm.YlOrRd(np.linspace(0.3, 0.9, len(district_pm25)))

    ax = district_pm25.plot(kind='bar', color=colors)
    plt.title('자치구별 초미세먼지(PM2.5) 평균 농도', fontsize=16)
    plt.xlabel('자치구', fontsize=14)
    plt.ylabel('평균 초미세먼지 농도(μg/㎥)', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # 기준선 표시
    plt.axhline(y=35, color='red', linestyle='--', label='적합 기준(35μg/㎥)')
    plt.axhline(y=25, color='orange', linestyle='--', label='WHO 권고 기준(25μg/㎥)')

    # 서울시 평균 표시
    seoul_avg_pm25 = filtered_results['PM2.5_최대값'].mean()
    plt.axhline(y=seoul_avg_pm25, color='green', linestyle='-.',
                label=f'서울시 평균: {seoul_avg_pm25:.2f}μg/㎥')

    plt.legend(fontsize=12)

    # 값 표시
    for i, v in enumerate(district_pm25):
        ax.text(i, v + 0.5, f'{v:.1f}', ha='center', fontsize=11)

    plt.tight_layout()
    plt.show()

    # 5. 자치구별 이산화탄소(CO2) 농도 평균 비교
    plt.figure(figsize=(14, 8))

    # 자치구별 이산화탄소 농도 평균 계산
    district_co2 = filtered_results.groupby('자치구')['CO2_최대값'].mean().sort_values(ascending=False)

    # 색상 맵 설정 (농도가 높을수록 빨간색)
    colors = plt.cm.YlOrRd(np.linspace(0.3, 0.9, len(district_co2)))

    ax = district_co2.plot(kind='bar', color=colors)
    plt.title('자치구별 이산화탄소(CO2) 평균 농도', fontsize=16)
    plt.xlabel('자치구', fontsize=14)
    plt.ylabel('평균 이산화탄소 농도(ppm)', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # 기준선 표시
    plt.axhline(y=1500, color='red', linestyle='--', label='적합 기준(1500ppm)')
    plt.axhline(y=1000, color='orange', linestyle='--', label='권고 기준(1000ppm)')

    # 서울시 평균 표시
    seoul_avg_co2 = filtered_results['CO2_최대값'].mean()
    plt.axhline(y=seoul_avg_co2, color='green', linestyle='-.',
                label=f'서울시 평균: {seoul_avg_co2:.0f}ppm')

    plt.legend(fontsize=12)

    # 값 표시
    for i, v in enumerate(district_co2):
        ax.text(i, v + 25, f'{v:.0f}', ha='center', fontsize=11)

    plt.tight_layout()
    plt.show()

    # 6. 자치구별 종합등급 분포 시각화
    plt.figure(figsize=(16, 10))

    # 자치구별 종합등급 분포 계산
    grade_order = ["매우 좋음", "좋음", "보통", "주의 필요", "위험", "평가 불가 (데이터 부족)"]
    district_grades = pd.crosstab(filtered_results['자치구'], filtered_results['종합_등급'])

    # 누락된 등급 열 추가
    for grade in grade_order:
        if grade not in district_grades.columns:
            district_grades[grade] = 0

    # 순서 재정렬
    district_grades = district_grades[grade_order]

    # 비율로 변환
    district_grades_pct = district_grades.div(district_grades.sum(axis=1), axis=0) * 100

    # 자치구를 종합점수 평균 순으로 정렬
    district_order = filtered_results.groupby('자치구')['종합_점수'].mean().sort_values(ascending=False).index
    district_grades_pct = district_grades_pct.reindex(district_order)

    # 스택 바 차트 그리기
    district_grades_pct.plot(kind='bar', stacked=True, figsize=(16, 10),
                          colormap='RdYlGn_r')

    plt.title('자치구별 공기질 종합등급 분포', fontsize=16)
    plt.xlabel('자치구', fontsize=14)
    plt.ylabel('비율 (%)', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.legend(title='종합 등급', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()

    # 7. 학교유형별 자치구 공기질 비교 (히트맵)
    if '학교유형' in filtered_results.columns:
        # 유효한 학교유형 필터링
        school_type_counts = filtered_results['학교유형'].value_counts()
        valid_types = school_type_counts[school_type_counts >= 5].index.tolist()

        if len(valid_types) >= 2:  # 최소 2개 이상의 유효한 학교유형이 있을 때
            type_district_data = filtered_results[filtered_results['학교유형'].isin(valid_types)]

            # 학교유형별 자치구별 평균 종합점수 계산
            pivot_data = type_district_data.pivot_table(
                values='종합_점수',
                index='자치구',
                columns='학교유형',
                aggfunc='mean'
            )

            # 히트맵 그리기
            plt.figure(figsize=(12, 10))
            sns.heatmap(pivot_data, annot=True, fmt='.2f', cmap='RdYlGn_r',
                       linewidths=.5, cbar_kws={'label': '평균 종합 점수'})

            plt.title('학교유형별 자치구 공기질 종합점수 비교', fontsize=16)
            plt.tight_layout()
            plt.show()

            # 학교유형별 자치구별 미세먼지(PM10) 평균 농도 계산
            pivot_pm10 = type_district_data.pivot_table(
                values='PM10_교실_최대값',
                index='자치구',
                columns='학교유형',
                aggfunc='mean'
            )

            # 히트맵 그리기
            plt.figure(figsize=(12, 10))
            sns.heatmap(pivot_pm10, annot=True, fmt='.1f', cmap='YlOrRd',
                       linewidths=.5, cbar_kws={'label': '평균 PM10 농도(μg/㎥)'})

            plt.title('학교유형별 자치구 미세먼지(PM10) 농도 비교', fontsize=16)
            plt.tight_layout()
            plt.show()

    # 8. 자치구별 부적합률 히트맵
    unsuitable_columns = ['PM10_교실_적합성', 'PM10_체육관_적합성', 'PM2.5_적합성',
                         'CO2_적합성', 'CO_적합성', 'NO2_적합성', 'O3_적합성']

    # 자치구별 항목별 부적합률 계산
    unsuitable_rates = pd.DataFrame(index=valid_districts)

    for col in unsuitable_columns:
        item_name = col.split('_')[0]
        district_data = filtered_results.groupby('자치구')[col]

        for district in valid_districts:
            if district in district_data.groups:  # 해당 자치구 데이터가 있는지 확인
                district_col_data = district_data.get_group(district)
                unsuitable_count = sum(district_col_data == "부적합")
                total = sum((district_col_data == "부적합") | (district_col_data == "적합"))

                if total > 0:
                    rate = (unsuitable_count / total) * 100
                else:
                    rate = 0

                unsuitable_rates.loc[district, item_name] = rate

    # 실제 생성된 컬럼에 맞게 컬럼명 지정
    actual_columns = unsuitable_rates.columns.tolist()
    column_mapping = {
        'PM10': 'PM10(교실)',
        'GMNSM_MNUT_DST': 'PM10(체육관)',
        'ULTRA_DST': 'PM2.5',
        'CO2': 'CO2',
        'CO': 'CO',
        'NO2': 'NO2',
        'O3': 'O3'
    }

    # 실제 존재하는 컬럼에 대해서만 이름 변경
    renamed_columns = []
    for col in actual_columns:
        if col in column_mapping:
            renamed_columns.append(column_mapping[col])
        else:
            renamed_columns.append(col)

    unsuitable_rates.columns = renamed_columns

    # 데이터가 충분한 경우에만 히트맵 그리기
    if not unsuitable_rates.empty and unsuitable_rates.shape[1] > 0:
        plt.figure(figsize=(14, 10))
        sns.heatmap(unsuitable_rates, annot=True, fmt='.1f', cmap='Reds',
                   linewidths=.5, cbar_kws={'label': '부적합률 (%)'})

        plt.title('자치구별 항목별 부적합률 (%)', fontsize=16)
        plt.tight_layout()
        plt.show()
    else:
        print("자치구별 항목별 부적합률을 표시할 충분한 데이터가 없습니다.")

# 추가: 공기질 항목별 지역 분포 시각화 함수
def visualize_pollutant_distribution_by_district(results):
    """공기질 항목별 지역 분포를 시각화하는 함수"""

    # 유효한 자치구 필터링
    district_counts = results['자치구'].value_counts()
    valid_districts = district_counts[district_counts >= 3].index.tolist()
    valid_districts = [d for d in valid_districts if d != "정보 없음"]

    if len(valid_districts) < 3:
        print("자치구 정보가 충분하지 않습니다. 데이터를 확인해주세요.")
        return

    filtered_results = results[results['자치구'].isin(valid_districts)]

    # 분석할 오염물질 및 설명
    pollutants = [
        {'col': 'PM10_교실_최대값', 'name': '미세먼지(PM10)', 'unit': 'μg/㎥',
         'limit': 75, 'who_limit': 50, 'cmap': 'YlOrRd'},
        {'col': 'PM2.5_최대값', 'name': '초미세먼지(PM2.5)', 'unit': 'μg/㎥',
         'limit': 35, 'who_limit': 25, 'cmap': 'YlOrRd'},
        {'col': 'CO2_최대값', 'name': '이산화탄소(CO2)', 'unit': 'ppm',
         'limit': 1500, 'who_limit': 1000, 'cmap': 'YlOrRd'},
        {'col': 'CO_최대값', 'name': '일산화탄소(CO)', 'unit': 'ppm',
         'limit': 10, 'who_limit': 5, 'cmap': 'YlOrRd'},
        {'col': 'NO2_최대값', 'name': '이산화질소(NO2)', 'unit': 'ppm',
         'limit': 0.05, 'who_limit': 0.03, 'cmap': 'YlOrRd'},
        {'col': 'O3_최대값', 'name': '오존(O3)', 'unit': 'ppm',
         'limit': 0.06, 'who_limit': 0.03, 'cmap': 'YlOrRd'}
    ]

    # 각 오염물질에 대해 지역별 분포 시각화
    for pollutant in pollutants:
        col = pollutant['col']

        # 해당 항목에 데이터가 충분한지 확인
        valid_data = filtered_results[pd.notna(filtered_results[col])]
        if len(valid_data) < 10:
            continue

        # 1. 자치구별 해당 오염물질 농도 분포 (박스플롯)
        plt.figure(figsize=(14, 8))
        sns.boxplot(x='자치구', y=col, data=valid_data, palette='YlOrRd_r')
        plt.title(f'자치구별 {pollutant["name"]} 농도 분포', fontsize=16)
        plt.xlabel('자치구', fontsize=14)
        plt.ylabel(f'{pollutant["name"]} 농도({pollutant["unit"]})', fontsize=14)
        plt.axhline(y=pollutant['limit'], color='red', linestyle='--',
                   label=f'적합 기준({pollutant["limit"]}{pollutant["unit"]})')
        plt.axhline(y=pollutant['who_limit'], color='orange', linestyle='--',
                   label=f'권고 기준({pollutant["who_limit"]}{pollutant["unit"]})')
        plt.legend(fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

        # 2. 자치구별 해당 오염물질 농도 평균 (바 차트)
        plt.figure(figsize=(14, 8))
        district_avg = valid_data.groupby('자치구')[col].mean().sort_values(ascending=False)

        # 색상 맵 설정 (값에 따라)
        norm = plt.Normalize(district_avg.min(), max(district_avg.max(), pollutant['limit'] * 1.2))
        colors = plt.cm.get_cmap(pollutant['cmap'])(norm(district_avg.values))

        ax = district_avg.plot(kind='bar', color=colors, figsize=(14, 8))
        plt.title(f'자치구별 {pollutant["name"]} 평균 농도', fontsize=16)
        plt.xlabel('자치구', fontsize=14)
        plt.ylabel(f'{pollutant["name"]} 농도({pollutant["unit"]})', fontsize=14)
        plt.axhline(y=pollutant['limit'], color='red', linestyle='--',
                   label=f'적합 기준({pollutant["limit"]}{pollutant["unit"]})')
        plt.axhline(y=pollutant['who_limit'], color='orange', linestyle='--',
                   label=f'권고 기준({pollutant["who_limit"]}{pollutant["unit"]})')

        # 서울시 평균 표시
        seoul_avg = valid_data[col].mean()
        plt.axhline(y=seoul_avg, color='green', linestyle='-.',
                   label=f'서울시 평균: {seoul_avg:.2f}{pollutant["unit"]}')

        plt.legend(fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # 값 표시
        for i, v in enumerate(district_avg):
            ax.text(i, v + (pollutant['limit'] * 0.02), f'{v:.2f}', ha='center', fontsize=11)

        plt.tight_layout()
        plt.show()

        # 3. 자치구별 해당 오염물질 적합/부적합 비율 (스택 바 차트)
        if f'{pollutant["name"].split("(")[0]}_적합성' in filtered_results.columns:
            suitability_col = f'{pollutant["name"].split("(")[0]}_적합성'

            plt.figure(figsize=(14, 8))
            district_suitability = pd.crosstab(
                filtered_results['자치구'],
                filtered_results[suitability_col],
                normalize='index'
            ) * 100

            # '데이터 없음' 열이 있으면 제거
            if '데이터 없음' in district_suitability.columns:
                district_suitability = district_suitability.drop('데이터 없음', axis=1)

            # 종합점수 평균 기준으로 자치구 정렬
            district_order = filtered_results.groupby('자치구')['종합_점수'].mean().sort_values(ascending=False).index
            district_order = [d for d in district_order if d in district_suitability.index]
            district_suitability = district_suitability.reindex(district_order)

            # 적합/부적합 컬럼이 모두 있는지 확인
            if '적합' not in district_suitability.columns:
                district_suitability['적합'] = 0
            if '부적합' not in district_suitability.columns:
                district_suitability['부적합'] = 0

            # 컬럼 순서 지정
            district_suitability = district_suitability[['적합', '부적합']]

            # 스택 바 차트 그리기
            district_suitability.plot(
                kind='bar',
                stacked=True,
                color=['lightgreen', 'red'],
                figsize=(14, 8)
            )

            plt.title(f'자치구별 {pollutant["name"]} 적합/부적합 비율', fontsize=16)
            plt.xlabel('자치구', fontsize=14)
            plt.ylabel('비율 (%)', fontsize=14)
            plt.xticks(rotation=45, ha='right', fontsize=12)
            plt.legend(title='적합 여부', fontsize=12)
            plt.grid(axis='y', linestyle='--', alpha=0.3)
            plt.tight_layout()
            plt.show()

