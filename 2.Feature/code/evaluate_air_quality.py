import pandas as pd
import numpy as np

# 함수: 미세먼지(PM10) 단계 평가
def evaluate_pm10(value):
    if pd.isna(value) or value == "":
        return "데이터 없음", 0

    value = float(value)
    if value <= 30:
        return "좋음", 1
    elif value <= 50:
        return "보통(민감군 안전)", 2
    elif value <= 65:
        return "보통(민감군 주의)", 3
    elif value <= 75:
        return "보통(모두 주의)", 4
    elif value <= 150:
        return "나쁨", 5
    else:
        return "매우 나쁨", 6

# 함수: 초미세먼지(PM2.5) 단계 평가
def evaluate_pm25(value):
    if pd.isna(value) or value == "":
        return "데이터 없음", 0

    value = float(value)
    if value <= 15:
        return "좋음", 1
    elif value <= 25:
        return "보통(민감군 안전)", 2
    elif value <= 35:
        return "보통(민감군 주의)", 3
    elif value <= 50:
        return "나쁨", 4
    elif value <= 75:
        return "매우 나쁨", 5
    else:
        return "위험", 6

# 함수: 이산화탄소(CO2) 단계 평가
def evaluate_co2(value):
    if pd.isna(value) or value == "":
        return "데이터 없음", 0

    value = float(value)
    if value <= 700:
        return "좋음", 1
    elif value <= 1000:
        return "보통", 2
    elif value <= 1500:
        return "주의", 3
    else:
        return "나쁨", 4

# 함수: 일산화탄소(CO) 단계 평가
def evaluate_co(value):
    if pd.isna(value) or value == "":
        return "데이터 없음", 0

    value = float(value)
    if value <= 2:
        return "좋음", 1
    elif value <= 5:
        return "보통", 2
    elif value <= 10:
        return "주의", 3
    else:
        return "나쁨", 4

# 함수: 이산화질소(NO2) 단계 평가
def evaluate_no2(value):
    if pd.isna(value) or value == "":
        return "데이터 없음", 0

    value = float(value)
    if value <= 0.03:
        return "좋음", 1
    elif value <= 0.05:
        return "보통", 2
    elif value <= 0.1:
        return "주의", 3
    else:
        return "나쁨", 4

# 함수: 오존(O3) 단계 평가
def evaluate_o3(value):
    if pd.isna(value) or value == "":
        return "데이터 없음", 0

    value = float(value)
    if value <= 0.03:
        return "좋음", 1
    elif value <= 0.06:
        return "보통", 2
    elif value <= 0.1:
        return "주의", 3
    else:
        return "나쁨", 4

# 함수: 적합성 여부(Y/N) 평가
def evaluate_suitability(yn_value):
    if pd.isna(yn_value) or yn_value == "" or yn_value =="해당없음" or yn_value =='미실시':
        return "데이터 없음", 0
    elif yn_value == '적합':
        return "적합", 1
    else:
        return "부적합", 2

# 함수: 다중 측정값 처리 (최대값 또는 평균값 사용)
def process_multiple_values(row, base_col, use_max=True):
    cols = [f"{base_col}", f"{base_col}_2", f"{base_col}_3"]
    values = []

    for col in cols:
        if col in row and not pd.isna(row[col]) and row[col] != "":
            try:
                values.append(float(row[col]))
            except (ValueError, TypeError):
                pass

    if len(values) == 0:
        return None

    if use_max:
        return max(values)  # 최대값 사용 (보수적 접근)
    else:
        return sum(values) / len(values)  # 평균값 사용

# 함수: 통합 공기질 평가
def evaluate_air_quality(df):
    # 결과를 저장할 DataFrame 생성
    results = pd.DataFrame()
    results['학교명'] = df['SCHUL_NM'] if 'SCHUL_NM' in df.columns else df.index
    results['학교코드'] = df['SCHUL_CODE'] if 'SCHUL_CODE' in df.columns else df.index

    # 미세먼지(PM10) - 교실 평가
    results['PM10_교실_최대값'] = df.apply(lambda row: process_multiple_values(row, 'MNUT_DST_RSLT_NMVL', True), axis=1)
    results['PM10_교실_단계'] = results['PM10_교실_최대값'].apply(lambda x: evaluate_pm10(x)[0])
    results['PM10_교실_점수'] = results['PM10_교실_최대값'].apply(lambda x: evaluate_pm10(x)[1])
    results['PM10_교실_적합성'] = df['MNUT_DST_STB_YN'].apply(lambda x: evaluate_suitability(x)[0])

    # 미세먼지(PM10) - 체육관 평가
    results['PM10_체육관_최대값'] = df.apply(lambda row: process_multiple_values(row, 'GMNSM_MNUT_DST_RSLT_NMVL', True), axis=1)
    results['PM10_체육관_단계'] = results['PM10_체육관_최대값'].apply(lambda x: evaluate_pm10(x)[0] if x is not None else "데이터 없음")
    results['PM10_체육관_점수'] = results['PM10_체육관_최대값'].apply(lambda x: evaluate_pm10(x)[1] if x is not None else 0)
    results['PM10_체육관_적합성'] = df['GMNSM_MNUT_DST_STB_YN'].apply(lambda x: evaluate_suitability(x)[0])

    # 초미세먼지(PM2.5) 평가
    results['PM2.5_최대값'] = df.apply(lambda row: process_multiple_values(row, 'ULTRA_DST_RSLT_NMVL', True), axis=1)
    results['PM2.5_단계'] = results['PM2.5_최대값'].apply(lambda x: evaluate_pm25(x)[0] if x is not None else "데이터 없음")
    results['PM2.5_점수'] = results['PM2.5_최대값'].apply(lambda x: evaluate_pm25(x)[1] if x is not None else 0)
    results['PM2.5_적합성'] = df['ULTRA_DST_STB_YN'].apply(lambda x: evaluate_suitability(x)[0])

    # 이산화탄소(CO2) 평가
    results['CO2_최대값'] = df.apply(lambda row: process_multiple_values(row, 'CO2_RSLT_NMVL', True), axis=1)
    results['CO2_단계'] = results['CO2_최대값'].apply(lambda x: evaluate_co2(x)[0] if x is not None else "데이터 없음")
    results['CO2_점수'] = results['CO2_최대값'].apply(lambda x: evaluate_co2(x)[1] if x is not None else 0)
    results['CO2_적합성'] = df['CO2_STB_YN'].apply(lambda x: evaluate_suitability(x)[0])

    # 일산화탄소(CO) 평가
    results['CO_최대값'] = df.apply(lambda row: process_multiple_values(row, 'CO_RSLT_NMVL', True), axis=1)
    results['CO_단계'] = results['CO_최대값'].apply(lambda x: evaluate_co(x)[0] if x is not None else "데이터 없음")
    results['CO_점수'] = results['CO_최대값'].apply(lambda x: evaluate_co(x)[1] if x is not None else 0)
    results['CO_적합성'] = df['CO_STB_YN'].apply(lambda x: evaluate_suitability(x)[0])

    # 이산화질소(NO2) 평가
    results['NO2_최대값'] = df.apply(lambda row: process_multiple_values(row, 'NO2_RSLT_NMVL', True), axis=1)
    results['NO2_단계'] = results['NO2_최대값'].apply(lambda x: evaluate_no2(x)[0] if x is not None else "데이터 없음")
    results['NO2_점수'] = results['NO2_최대값'].apply(lambda x: evaluate_no2(x)[1] if x is not None else 0)
    results['NO2_적합성'] = df['NO2_STB_YN'].apply(lambda x: evaluate_suitability(x)[0])

    # 오존(O3) 평가
    results['O3_최대값'] = df.apply(lambda row: process_multiple_values(row, 'O3_RSLT_NMVL', True), axis=1)
    results['O3_단계'] = results['O3_최대값'].apply(lambda x: evaluate_o3(x)[0] if x is not None else "데이터 없음")
    results['O3_점수'] = results['O3_최대값'].apply(lambda x: evaluate_o3(x)[1] if x is not None else 0)
    results['O3_적합성'] = df['O3_STB_YN'].apply(lambda x: evaluate_suitability(x)[0])

    # 종합 평가 (가중 평균 점수)
    # 미세먼지와 초미세먼지에 더 높은 가중치 부여
    weights = {
        'PM10_교실_점수': 0.25,
        'PM2.5_점수': 0.25,
        'CO2_점수': 0.15,
        'CO_점수': 0.1,
        'NO2_점수': 0.1,
        'O3_점수': 0.15
    }

    # 가중 평균 계산
    score_columns = ['PM10_교실_점수', 'PM2.5_점수', 'CO2_점수', 'CO_점수', 'NO2_점수', 'O3_점수']
    results['데이터_존재_항목수'] = results[score_columns].apply(lambda x: sum(x > 0), axis=1)

    # 최소 3개 이상의 데이터가 있는 경우에만 종합 점수 계산
    results['종합_점수'] = 0

    for idx, row in results.iterrows():
        if row['데이터_존재_항목수'] >= 3:
            weighted_sum = 0
            weight_sum = 0

            for col, weight in weights.items():
                if row[col] > 0:
                    weighted_sum += row[col] * weight
                    weight_sum += weight

            if weight_sum > 0:
                results.at[idx, '종합_점수'] = weighted_sum / weight_sum

    # 종합 등급 평가
    def get_overall_grade(score):
        if score == 0:
            return "평가 불가 (데이터 부족)"
        elif score < 2:
            return "매우 좋음"
        elif score < 3:
            return "좋음"
        elif score < 4:
            return "보통"
        elif score < 5:
            return "주의 필요"
        else:
            return "위험"

    results['종합_등급'] = results['종합_점수'].apply(get_overall_grade)

    # 부적합 항목 집계
    unsuitable_columns = ['PM10_교실_적합성', 'PM10_체육관_적합성', 'PM2.5_적합성',
                          'CO2_적합성', 'CO_적합성', 'NO2_적합성', 'O3_적합성']

    results['부적합_항목수'] = results[unsuitable_columns].apply(
        lambda x: sum(x == "부적합"), axis=1)

    return results
