# 학교유형별 지역별 분석 함수
def analyze_by_school_type_and_district(results):
    """학교유형별, 지역별 공기질 분석을 수행하는 함수"""

    # 유효한 학교유형 및 자치구 필터링
    valid_types = results['학교유형'].value_counts()[results['학교유형'].value_counts() >= 5].index.tolist()
    valid_districts = results['자치구'].value_counts()[results['자치구'].value_counts() >= 3].index.tolist()
    valid_districts = [d for d in valid_districts if d != "정보 없음"]

    filtered_results = results[results['학교유형'].isin(valid_types) & results['자치구'].isin(valid_districts)]

    if len(filtered_results) < 10:  # 데이터가 너무 적으면 분석 중단
        print("학교유형별, 지역별 분석을 위한 충분한 데이터가 없습니다.")
        return

    # 1. 학교유형별 공기질 종합점수 비교 (박스플롯)
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='학교유형', y='종합_점수', data=filtered_results, palette='Set3')
    plt.title('학교유형별 공기질 종합점수 분포', fontsize=16)
    plt.xlabel('학교유형', fontsize=14)
    plt.ylabel('종합 점수', fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    # 학교유형별 지역별 분석 함수 (계속)
def analyze_by_school_type_and_district(results):
    """학교유형별, 지역별 공기질 분석을 수행하는 함수"""

    # 유효한 학교유형 및 자치구 필터링
    valid_types = results['학교유형'].value_counts()[results['학교유형'].value_counts() >= 5].index.tolist()
    valid_districts = results['자치구'].value_counts()[results['자치구'].value_counts() >= 3].index.tolist()
    valid_districts = [d for d in valid_districts if d != "정보 없음"]

    filtered_results = results[results['학교유형'].isin(valid_types) & results['자치구'].isin(valid_districts)]

    if len(filtered_results) < 10:  # 데이터가 너무 적으면 분석 중단
        print("학교유형별, 지역별 분석을 위한 충분한 데이터가 없습니다.")
        return

    # 1. 학교유형별 공기질 종합점수 비교 (박스플롯)
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='학교유형', y='종합_점수', data=filtered_results, palette='Set3')
    plt.title('학교유형별 공기질 종합점수 분포', fontsize=16)
    plt.xlabel('학교유형', fontsize=14)
    plt.ylabel('종합 점수', fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    # 2. 학교유형별 미세먼지 농도 비교 (바이올린 플롯)
    plt.figure(figsize=(12, 8))
    sns.violinplot(x='학교유형', y='PM10_교실_최대값', data=filtered_results, palette='Set2')
    plt.title('학교유형별 교실 미세먼지(PM10) 농도 분포', fontsize=16)
    plt.xlabel('학교유형', fontsize=14)
    plt.ylabel('미세먼지 농도(μg/㎥)', fontsize=14)
    plt.axhline(y=75, color='red', linestyle='--', label='적합 기준(75μg/㎥)')
    plt.axhline(y=50, color='orange', linestyle='--', label='WHO 권고 기준(50μg/㎥)')
    plt.legend(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    # 3. 학교유형별 초미세먼지 농도 비교
    plt.figure(figsize=(12, 8))
    sns.violinplot(x='학교유형', y='PM2.5_최대값', data=filtered_results, palette='Set2')
    plt.title('학교유형별 초미세먼지(PM2.5) 농도 분포', fontsize=16)
    plt.xlabel('학교유형', fontsize=14)
    plt.ylabel('초미세먼지 농도(μg/㎥)', fontsize=14)
    plt.axhline(y=35, color='red', linestyle='--', label='적합 기준(35μg/㎥)')
    plt.axhline(y=25, color='orange', linestyle='--', label='WHO 권고 기준(25μg/㎥)')
    plt.legend(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    # 4. 학교유형별 부적합률 비교 (막대 그래프)
    unsuitable_columns = ['PM10_교실_적합성', 'PM10_체육관_적합성', 'PM2.5_적합성',
                         'CO2_적합성', 'CO_적합성', 'NO2_적합성', 'O3_적합성']

    # 학교유형별 항목별 부적합률 계산
    unsuitable_by_type = []

    for school_type in valid_types:
        type_data = filtered_results[filtered_results['학교유형'] == school_type]

        for col in unsuitable_columns:
            item_name = col.split('_')[0]
            unsuitable_count = sum(type_data[col] == "부적합")
            total = sum((type_data[col] == "부적합") | (type_data[col] == "적합"))

            if total > 0:
                rate = (unsuitable_count / total) * 100
            else:
                rate = 0

            unsuitable_by_type.append({
                '학교유형': school_type,
                '항목': item_name,
                '부적합률(%)': rate
            })

    unsuitable_df = pd.DataFrame(unsuitable_by_type)

    plt.figure(figsize=(14, 8))
    sns.barplot(x='항목', y='부적합률(%)', hue='학교유형', data=unsuitable_df, palette='Set1')
    plt.title('학교유형별 항목별 부적합률', fontsize=16)
    plt.xlabel('항목', fontsize=14)
    plt.ylabel('부적합률(%)', fontsize=14)
    plt.legend(title='학교유형', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    # 5. 학교유형별 자치구별 공기질 히트맵
    pivot_data = filtered_results.pivot_table(
        values='종합_점수',
        index='자치구',
        columns='학교유형',
        aggfunc='mean'
    )

    plt.figure(figsize=(14, 10))
    sns.heatmap(pivot_data, annot=True, fmt='.2f', cmap='RdYlGn_r',
               linewidths=.5, cbar_kws={'label': '평균 종합 점수'})

    plt.title('학교유형별 자치구별 공기질 종합점수', fontsize=16)
    plt.tight_layout()
    plt.show()

    # 6. 학교유형별 자치구별 미세먼지(PM10) 히트맵
    pivot_pm10 = filtered_results.pivot_table(
        values='PM10_교실_최대값',
        index='자치구',
        columns='학교유형',
        aggfunc='mean'
    )

    plt.figure(figsize=(14, 10))
    sns.heatmap(pivot_pm10, annot=True, fmt='.1f', cmap='YlOrRd',
               linewidths=.5, cbar_kws={'label': '평균 미세먼지 농도(μg/㎥)'})

    plt.title('학교유형별 자치구별 미세먼지(PM10) 농도', fontsize=16)
    plt.tight_layout()
    plt.show()

    # 7. 학교유형별 통계 요약
    type_stats = filtered_results.groupby('학교유형').agg({
        '종합_점수': ['mean', 'median', 'std', 'count'],
        'PM10_교실_최대값': ['mean', 'median', 'max'],
        'PM2.5_최대값': ['mean', 'median', 'max'],
        'CO2_최대값': ['mean', 'median', 'max'],
        '부적합_항목수': ['mean', 'sum']
    })

    # 컬럼명 정리
    type_stats.columns = [
        '종합점수_평균', '종합점수_중앙값', '종합점수_표준편차', '학교수',
        'PM10_평균', 'PM10_중앙값', 'PM10_최대값',
        'PM2.5_평균', 'PM2.5_중앙값', 'PM2.5_최대값',
        'CO2_평균', 'CO2_중앙값', 'CO2_최대값',
        '부적합항목_평균', '부적합항목_총합'
    ]

    # 종합점수 기준으로 정렬
    type_stats = type_stats.sort_values('종합점수_평균', ascending=False)

    print("\n===== 학교유형별 공기질 통계 =====")
    print(type_stats)

    return type_stats
