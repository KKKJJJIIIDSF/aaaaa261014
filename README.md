# 🏭 제조 품질 현황 대시보드

AI 비전검사 PoC를 준비하기 위한 간단한 제조 품질 데이터 모니터링 대시보드입니다.

## 프로젝트 목적

본격적인 AI 비전검사 모델을 개발하기 전에 Python, pandas, Streamlit, GitHub, Streamlit Community Cloud를 이용해 데이터 처리부터 웹 대시보드 제작과 배포까지의 전체 흐름을 경험합니다.

## 주요 기능

- CSV 파일 업로드
- CSV가 없을 때 기본 샘플 데이터 사용
- 날짜 / 제품 / 검사 결과 필터
- 전체 검사 / 정상 / 불량 / 불량률 KPI
- 날짜별 검사 현황 선그래프
- 불량 유형별 건수 막대그래프
- 최근 검사 결과 10건 표시

## 프로젝트 구조

```text
quality-dashboard/
├── app.py
├── requirements.txt
└── README.md
```

## CSV 형식

다음 컬럼이 필요합니다.

```text
inspection_date
product_id
result
defect_type
confidence
```

예시:

```csv
inspection_date,product_id,result,defect_type,confidence
2026-10-01,P001,OK,None,0.98
2026-10-01,P002,NG,Scratch,0.91
2026-10-02,P003,OK,None,0.96
2026-10-02,P004,NG,Crack,0.88
```

## Windows에서 로컬 실행

### 1. 가상환경 생성

```bash
python -m venv .venv
```

### 2. 가상환경 활성화

```bash
.venv\Scripts\activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. 앱 실행

```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501`을 엽니다.

## GitHub 업로드

GitHub에서 새 Repository를 만든 뒤 프로젝트 폴더에서:

```bash
git init
git add .
git commit -m "Create quality dashboard"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

`YOUR_GITHUB_REPOSITORY_URL`은 본인이 만든 Repository 주소로 바꿉니다.

## Streamlit Community Cloud 배포

1. Streamlit Community Cloud에 GitHub 계정으로 로그인합니다.
2. 새 앱을 생성합니다.
3. GitHub Repository를 선택합니다.
4. Branch를 `main`으로 선택합니다.
5. Main file을 `app.py`로 선택합니다.
6. Deploy를 실행합니다.

`requirements.txt`에 적힌 패키지를 Streamlit Community Cloud가 설치합니다.

## 문제 해결

### streamlit 명령어가 없는 경우

가상환경이 활성화되어 있는지 확인한 후:

```bash
pip install -r requirements.txt
```

를 다시 실행합니다.

### CSV 오류

CSV에 다음 컬럼이 모두 있는지 확인합니다.

```text
inspection_date
product_id
result
defect_type
confidence
```

### 절대 경로

다음과 같은 로컬 절대 경로는 사용하지 않습니다.

```python
pd.read_csv("C:/Users/홍길동/Desktop/data.csv")
```

대신 Streamlit의 CSV 업로더를 사용합니다.

## 향후 비전검사 PoC 확장

1. CSV 입력을 실제 제품 이미지 입력으로 변경
2. AI 비전검사 모델을 연결해 OK/NG와 불량 유형 생성
3. confidence를 실제 모델 추론 신뢰도로 연결
4. 원본 검사 이미지와 불량 위치를 함께 표시
5. 검사 결과 저장 및 실시간 생산라인 모니터링으로 확장
