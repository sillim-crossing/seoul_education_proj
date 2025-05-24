# 학교별 권고사항 생성 함수
def generate_recommendations(results):
    recommendations = []

    for idx, row in results.iterrows():
        school_name = row['학교명']
        rec = {'학교명': school_name, '권고사항': []}

        # PM10 교실 권고사항
        if not pd.isna(row['PM10_교실_최대값']):
            pm10 = float(row['PM10_교실_최대값'])
            if pm10 > 75:
                rec['권고사항'].append(f"교실 미세먼지(PM10)가 {pm10:.1f}μg/㎥로 기준치(75μg/㎥)를 초과함. 실외활동 제한 및 공기청정기 가동 필요")
            elif pm10 > 65:
                rec['권고사항'].append(f"교실 미세먼지(PM10)가 {pm10:.1f}μg/㎥로 주의 수준. 호흡기 질환자 실외활동 제한 권고")
            elif pm10 > 50:
                rec['권고사항'].append(f"교실 미세먼지(PM10)가 {pm10:.1f}μg/㎥로 민감군 주의 필요. 천식 등 민감군 학생 모니터링")

        # PM2.5 권고사항
        if not pd.isna(row['PM2.5_최대값']):
            pm25 = float(row['PM2.5_최대값'])
            if pm25 > 35:
                rec['권고사항'].append(f"초미세먼지(PM2.5)가 {pm25:.1f}μg/㎥로 기준치(35μg/㎥)를 초과함. 실내 활동 권고")
            elif pm25 > 25:
                rec['권고사항'].append(f"초미세먼지(PM2.5)가 {pm25:.1f}μg/㎥로 주의 수준. 민감군 학생 마스크 착용 권고")

        # CO2 권고사항
        if not pd.isna(row['CO2_최대값']):
            co2 = float(row['CO2_최대값'])
            if co2 > 1500:
                rec['권고사항'].append(f"이산화탄소(CO2)가 {co2:.0f}ppm으로 기준치(1500ppm)를 초과함. 환기 시스템 점검 및 환기 빈도 증가 필요")
            elif co2 > 1000:
                rec['권고사항'].append(f"이산화탄소(CO2)가 {co2:.0f}ppm으로 주의 수준. 정기적인 환기 권고")

        # 종합 등급에 따른 권고사항
        grade = row['종합_등급']
        if grade == "위험":
            rec['권고사항'].append("공기질 종합 등급이 '위험'으로 평가됨. 즉각적인 조치 필요")
        elif grade == "주의 필요":
            rec['권고사항'].append("공기질 종합 등급이 '주의 필요'로 평가됨. 환기 및 공기질 개선 조치 권고")

        # 부적합 항목 관련 권고사항
        if row['부적합_항목수'] > 0:
            rec['권고사항'].append(f"총 {row['부적합_항목수']}개 항목이 부적합 판정. 공기질 개선 계획 수립 필요")

        recommendations.append(rec)

    return pd.DataFrame(recommendations)
