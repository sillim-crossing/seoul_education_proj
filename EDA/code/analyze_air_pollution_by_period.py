# 계절/기간별 분석 함수 (데이터에 해당 정보가 있는 경우)
def analyze_by_period(results, df):
    """계절/기간별 공기질 분석을 수행하는 함수"""

    # 상하반기 구분 정보가 있는지 확인
    if 'SEM_STR' in df.columns:
        # 상하반기 정보 추가
        results['조사기간'] = df['SEM_STR']

        # 유효한 기간 필터링
        period_counts = results['조사기간'].value_counts()
        valid_periods = period_counts[period_counts >= 10].index.tolist()

        if len(valid_periods) >= 2:  # 비교 가능한 기간이 있는 경우
            filtered_results = results[results['조사기간'].isin(valid_periods)]

            # 1. 기간별 공기질 종합점수 비교 (박스플롯)
            plt.figure(figsize=(12, 8))
            sns.boxplot(x='조사기간', y='종합_점수', data=filtered_results, palette='Set3')
            plt.title('기간별 공기질 종합점수 분포', fontsize=16)
            plt.xlabel('조사기간', fontsize=14)
            plt.ylabel('종합 점수', fontsize=14)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.show()

            # 2. 기간별 미세먼지 농도 비교 (박스플롯)
            plt.figure(figsize=(12, 8))
            sns.boxplot(x='조사기간', y='PM10_교실_최대값', data=filtered_results, palette='Set3')
            plt.title('기간별 교실 미세먼지(PM10) 농도 분포', fontsize=16)
            plt.xlabel('조사기간', fontsize=14)
            plt.ylabel('미세먼지 농도(μg/㎥)', fontsize=14)
            plt.axhline(y=75, color='red', linestyle='--', label='적합 기준(75μg/㎥)')
            plt.axhline(y=50, color='orange', linestyle='--', label='WHO 권고 기준(50μg/㎥)')
            plt.legend(fontsize=12)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.show()

            # 3. 기간별 자치구별 미세먼지 농도 비교 (히트맵)
            # 유효한 자치구 필터링
            district_counts = filtered_results['자치구'].value_counts()
            valid_districts = district_counts[district_counts >= 3].index.tolist()
            valid_districts = [d for d in valid_districts if d != "정보 없음"]

            district_period_data = filtered_results[filtered_results['자치구'].isin(valid_districts)]

            if len(valid_districts) >= 3:  # 충분한 자치구 데이터가 있는 경우
                pivot_period_pm10 = district_period_data.pivot_table(
                    values='PM10_교실_최대값',
                    index='자치구',
                    columns='조사기간',
                    aggfunc='mean'
                )

                plt.figure(figsize=(12, len(valid_districts) * 0.5 + 4))
                sns.heatmap(pivot_period_pm10, annot=True, fmt='.1f', cmap='YlOrRd',
                           linewidths=.5, cbar_kws={'label': '평균 미세먼지 농도(μg/㎥)'})

                plt.title('기간별 자치구별 미세먼지(PM10) 농도', fontsize=16)
                plt.tight_layout()
                plt.show()

                # 4. 기간별 초미세먼지 농도 비교 (히트맵)
                pivot_period_pm25 = district_period_data.pivot_table(
                    values='PM2.5_최대값',
                    index='자치구',
                    columns='조사기간',
                    aggfunc='mean'
                )

                plt.figure(figsize=(12, len(valid_districts) * 0.5 + 4))
                sns.heatmap(pivot_period_pm25, annot=True, fmt='.1f', cmap='YlOrRd',
                           linewidths=.5, cbar_kws={'label': '평균 초미세먼지 농도(μg/㎥)'})

                plt.title('기간별 자치구별 초미세먼지(PM2.5) 농도', fontsize=16)
                plt.tight_layout()
                plt.show()

            # 5. 기간별 통계 요약
            period_stats = filtered_results.groupby('조사기간').agg({
                '종합_점수': ['mean', 'median', 'std', 'count'],
                'PM10_교실_최대값': ['mean', 'median', 'max'],
                'PM2.5_최대값': ['mean', 'median', 'max'],
                'CO2_최대값': ['mean', 'median', 'max'],
                '부적합_항목수': ['mean', 'sum']
            })

            # 컬럼명 정리
            period_stats.columns = [
                '종합점수_평균', '종합점수_중앙값', '종합점수_표준편차', '학교수',
                'PM10_평균', 'PM10_중앙값', 'PM10_최대값',
                'PM2.5_평균', 'PM2.5_중앙값', 'PM2.5_최대값',
                'CO2_평균', 'CO2_중앙값', 'CO2_최대값',
                '부적합항목_평균', '부적합항목_총합'
            ]

            print("\n===== 기간별 공기질 통계 =====")
            print(period_stats)

            return period_stats
