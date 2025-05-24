
import pandas as pd
import numpy as np
import re

# 지역별 분석을 위한 데이터 전처리 함수
def preprocess_for_district_analysis(df, results):
    # 지역 정보 추출
    if 'ADRCD_NM' in df.columns:
        results['지역'] = df['ADRCD_NM']

    # 주소가 있는 경우 자치구 추출
    if 'SCHUL_ADRES' in df.columns:
        results['주소'] = df['SCHUL_ADRES']
        results['자치구'] = df['SCHUL_ADRES'].apply(extract_district)
    else:
        # 주소 정보가 없을 경우 지역명에서 추출 시도
        if 'ADRCD_NM' in df.columns:
            results['자치구'] = df['ADRCD_NM'].apply(lambda x: x if pd.notna(x) and '구' in x else "정보 없음")
        else:
            results['자치구'] = "정보 없음"

    # 학교유형 정보 추출
    if 'SCHUL_KND_SC_CODE' in df.columns:
        results['학교유형'] = df['SCHUL_KND_SC_CODE'].apply(extract_school_type)

    return results

# 주소에서 자치구 추출 함수
def extract_district(address):
    if pd.isna(address):
        return "정보 없음"

    # 서울특별시 OO구 형태의 주소에서 구 추출
    district_match = re.search(r'서울특별시\s+(\S+구)', address)
    if district_match:
        return district_match.group(1)
    else:
        return "정보 없음"

# 학교유형 추출 함수
def extract_school_type(code):
    if pd.isna(code):
        return "정보 없음"

    code = str(code)
    if code == '2':
        return '초등학교'
    elif code == '3':
        return '중학교'
    elif code == '4':
        return '고등학교'
    else:
        return '기타'


# 지역별 공기질 분석 함수
def analyze_district_air_quality(results):
    # 자치구별 종합 통계
    district_stats = results.groupby('자치구').agg({
        '종합_점수': ['mean', 'median', 'std', 'count'],
        'PM10_교실_최대값': ['mean', 'median', 'max'],
        'PM2.5_최대값': ['mean', 'median', 'max'],
        'CO2_최대값': ['mean', 'median', 'max'],
        '부적합_항목수': ['mean', 'sum']
    })

    # 컬럼명 정리
    district_stats.columns = [
        '종합점수_평균', '종합점수_중앙값', '종합점수_표준편차', '학교수',
        'PM10_평균', 'PM10_중앙값', 'PM10_최대값',
        'PM2.5_평균', 'PM2.5_중앙값', 'PM2.5_최대값',
        'CO2_평균', 'CO2_중앙값', 'CO2_최대값',
        '부적합항목_평균', '부적합항목_총합'
    ]

    # 종합점수 기준으로 정렬
    district_stats = district_stats.sort_values('종합점수_평균', ascending=False)

    # 학교수가 충분한 자치구만 필터링
    district_stats = district_stats[district_stats['학교수'] >= 3]

    # 자치구별 공기질 등급 분포
    district_grades = pd.crosstab(
        results['자치구'],
        results['종합_등급'],
        normalize='index'
    ) * 100

    # 상위 5개, 하위 5개 자치구 통계
    top5_worst = district_stats.head(5)
    top5_best = district_stats.sort_values('종합점수_평균').head(5)

    return {
        'district_stats': district_stats,
        'district_grades': district_grades,
        'top5_worst': top5_worst,
        'top5_best': top5_best
    }


# 메인 함수: 데이터 분석 및 결과 출력 (지역별 분석 추가)
def analyze_school_air_quality(data_file):
    # 데이터 로드
    df = pd.read_csv(data_file)

    # 공기질 평가
    results = evaluate_air_quality(df)

    # 지역별 분석을 위한 데이터 전처리
    results = preprocess_for_district_analysis(df, results)

    # 학교별 결과 시각화
    print("학교별 공기질 분석 결과 시각화 중...")
    visualize_results(results)

    # 지역별 결과 시각화
    print("지역별 공기질 분석 결과 시각화 중...")
    visualize_district_analysis(results)

    # 지역별 종합 분석
    print("지역별 종합 분석 수행 중...")
    district_analysis = analyze_district_air_quality(results)

    # 권고사항 생성
    recommendations = generate_recommendations(results)

    # 결과 저장
    results.to_csv('학교별_공기질_평가_결과.csv', index=False, encoding='utf-8-sig')
    recommendations.to_csv('학교별_공기질_개선_권고사항.csv', index=False, encoding='utf-8-sig')
    save_district_results(district_analysis)

    print(f"분석 완료. 총 {len(df)}개 학교의 공기질 평가 결과가 저장되었습니다.")
    return results, recommendations, district_analysis

# 자치구별 결과를 파일로 저장하는 함수
def save_district_results(district_analysis, filename='자치구별_공기질_분석결과.xlsx'):
    # Excel 파일로 저장
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        district_analysis['district_stats'].to_excel(writer, sheet_name='자치구별_종합통계')
        district_analysis['district_grades'].to_excel(writer, sheet_name='자치구별_등급분포')
        district_analysis['top5_worst'].to_excel(writer, sheet_name='공기질_하위5개_자치구')
        district_analysis['top5_best'].to_excel(writer, sheet_name='공기질_상위5개_자치구')

    print(f"자치구별 분석 결과가 '{filename}' 파일로 저장되었습니다.")

# 사용 예시
results, recommendations = analyze_school_air_quality('/content/서울특별시_국공립_초중고_환경위생관리현황.csv')
