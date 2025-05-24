# 추가: 지역별 공기질 문제 요약 함수
def summarize_district_issues(district_analysis):
    """자치구별 주요 공기질 문제를 요약하여 출력하는 함수"""

    district_stats = district_analysis['district_stats']

    # 공기질 종합점수 하위 5개 자치구
    worst_districts = district_stats.nlargest(5, '종합점수_평균')

    print("===== 공기질 종합점수 하위 5개 자치구 =====")
    for idx, (district, row) in enumerate(worst_districts.iterrows(), 1):
        print(f"{idx}. {district}")
        print(f"   - 종합점수: {row['종합점수_평균']:.2f} (서울시 평균보다 {row['종합점수_평균'] - district_stats['종합점수_평균'].mean():.2f} 높음)")
        print(f"   - 미세먼지(PM10): {row['PM10_평균']:.1f}μg/㎥ (최대 {row['PM10_최대값']:.1f}μg/㎥)")
        print(f"   - 초미세먼지(PM2.5): {row['PM2.5_평균']:.1f}μg/㎥ (최대 {row['PM2.5_최대값']:.1f}μg/㎥)")
        print(f"   - 이산화탄소(CO2): {row['CO2_평균']:.0f}ppm (최대 {row['CO2_최대값']:.0f}ppm)")
        print(f"   - 부적합 항목 평균: {row['부적합항목_평균']:.1f}개")
        print()

    # 주요 오염물질별 상위 3개 자치구
    print("===== 미세먼지(PM10) 농도 상위 3개 자치구 =====")
    for idx, (district, row) in enumerate(district_stats.nlargest(3, 'PM10_평균').iterrows(), 1):
        print(f"{idx}. {district}: {row['PM10_평균']:.1f}μg/㎥ (최대 {row['PM10_최대값']:.1f}μg/㎥)")

    print("\n===== 초미세먼지(PM2.5) 농도 상위 3개 자치구 =====")
    for idx, (district, row) in enumerate(district_stats.nlargest(3, 'PM2.5_평균').iterrows(), 1):
        print(f"{idx}. {district}: {row['PM2.5_평균']:.1f}μg/㎥ (최대 {row['PM2.5_최대값']:.1f}μg/㎥)")

    print("\n===== 이산화탄소(CO2) 농도 상위 3개 자치구 =====")
    for idx, (district, row) in enumerate(district_stats.nlargest(3, 'CO2_평균').iterrows(), 1):
        print(f"{idx}. {district}: {row['CO2_평균']:.0f}ppm (최대 {row['CO2_최대값']:.0f}ppm)")

    # 부적합 항목 많은 상위 3개 자치구
    print("\n===== 부적합 항목 많은 상위 3개 자치구 =====")
    for idx, (district, row) in enumerate(district_stats.nlargest(3, '부적합항목_평균').iterrows(), 1):
        print(f"{idx}. {district}: 평균 {row['부적합항목_평균']:.1f}개 (총 {row['부적합항목_총합']}개)")
