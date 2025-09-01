# Beamo Portal Automated Testing Platform

Beamo 포탈의 자동화 테스트 플랫폼입니다. Python과 Playwright를 사용하여 dev, stage, live 환경에서 일관된 E2E 테스트를 수행합니다.

## 환경 구성

- **Dev**: https://accounts.beamo.dev/login
- **Stage**: https://accounts.3inc.xyz/login  
- **Live**: https://accounts.beamo.ai/login

## 기술 스택

- **Language**: Python 3.x
- **Testing Framework**: Playwright
- **Reporting**: Playwright HTML Reporter + Rich
- **Containerization**: Docker
- **Configuration**: YAML

## 프로젝트 구조

```
/
├── config/                     # 환경별 설정 파일
│   ├── dev.yaml
│   ├── stage.yaml
│   └── live.yaml
├── tests/                      # 테스트 시나리오
│   ├── __init__.py
│   ├── smoke/                  # 스모크 테스트
│   └── regression/             # 회귀 테스트
├── pages/                      # Page Object Model
│   ├── __init__.py
│   ├── login_page.py
│   └── dashboard_page.py
├── utils/                      # 유틸리티 함수
│   ├── __init__.py
│   ├── config_loader.py
│   └── browser_manager.py
├── reports/                    # 테스트 리포트
├── test_data/                  # 테스트 데이터
│   └── images/                 # 테스트용 이미지 파일
├── requirements.txt            # Python 의존성
├── Dockerfile                  # Docker 설정
└── run_tests.py               # 메인 실행 스크립트
```

## 빠른 시작

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. Playwright 브라우저 설치
```bash
playwright install
```

### 3. 테스트 실행 (Dev-First 접근법)
```bash
# Phase 1: Dev 환경 스모크 테스트 (개발/검증)
python run_tests.py --env dev --tags smoke

# Phase 1: Dev 환경 회귀 테스트 (검증)
python run_tests.py --env dev --tags regression

# Phase 2: Stage 환경 테스트 (Dev 검증 후)
python run_tests.py --env stage --tags smoke

# Phase 3: Live 환경 테스트 (최종 검증)
python run_tests.py --env live --tags smoke
```

### 4. Docker로 실행 (Dev-First 접근법)
```bash
# 이미지 빌드
docker build -t beamo-test .

# Phase 1: Dev 환경 실행 (개발/검증)
docker run -e BEAMO_ENV=dev beamo-test

# Phase 2: Stage 환경 실행 (Dev 검증 후)
docker run -e BEAMO_ENV=stage beamo-test

# Phase 3: Live 환경 실행 (최종)
docker run -e BEAMO_ENV=live beamo-test
```

## 주요 기능

- ✅ 크로스 브라우저 테스트 (Chrome, Firefox, Safari)
- ✅ 모바일 에뮬레이션 지원
- ✅ 환경별 설정 관리
- ✅ HTML 리포트 생성
- ✅ 실패 시 스크린샷 자동 캡처
- ✅ 동영상 녹화 및 자동 저장
- ✅ 커스터마이징된 파일명 (테스트명_상태_타임스탬프)
- ✅ 네이티브 파일 다이얼로그 자동 처리
- ✅ Docker 컨테이너 지원
- ✅ CI/CD 파이프라인 연동

## 테스트 태그

- `@smoke`: 핵심 기능 검증 (10분 이내)
- `@regression`: 전체 회귀 테스트
- `@p0`: 최우선 순위 테스트
- `@p1`: 중간 우선순위 테스트

## 개발 전략: Dev-First 접근법

**핵심 원칙**: Dev 환경을 기준으로 구축하고 성공한 후 다른 환경에 적용

### 단계별 개발 프로세스

1. **Phase 1: Dev 환경 구축 및 검증**
   - Dev 환경에서 모든 구성요소 개발 및 테스트
   - Page Object Model, 테스트 시나리오, 설정 파일 검증
   - 실제 Beamo Dev 환경에서 E2E 테스트 성공 확인

2. **Phase 2: Stage 환경 적용**
   - Dev에서 검증된 코드를 Stage 환경에 적용
   - Stage 환경별 설정 차이점 확인 및 조정
   - Stage 환경에서 전체 테스트 스위트 검증

3. **Phase 3: Live 환경 적용**
   - Dev/Stage에서 검증된 코드를 Live 환경에 적용
   - Live 환경 특성에 맞는 안전장치 추가 (읽기 전용, 빠른 타임아웃 등)
   - Synthetic Monitoring 설정

### 테스트 이미지 사용

Add Plan 테스트에서는 실제 이미지 파일을 사용합니다:

```bash
# 테스트용 이미지 생성 (자동으로 생성됨)
test_data/images/test_gallery_image.png

# Add Plan 테스트 실행
pytest tests/smoke/test_add_plan.py -v

# Add Plan + New Survey 완전한 플로우 테스트
pytest tests/smoke/test_add_plan_and_survey.py -v
```

**테스트 이미지 특징:**
- 800x600 픽셀 PNG 형식
- 건물 도면 스타일의 테스트 이미지
- 자동으로 생성되며 `.gitignore`에 포함됨
- 네이티브 파일 다이얼로그 자동 처리

### 파일명 커스터마이징

모든 테스트 아티팩트는 다음 형식으로 저장됩니다:

```
{testname}_{status}_{timestamp}.{extension}
```

**예시:**
- `add_plan_complete_success_20250901_191344.png`
- `add_plan_and_create_survey_flow_success_20250901_191607.webm`
- `before_new_survey_attempt_unknown_20250901_191600.png`

**상태 값:**
- `success`: 테스트 성공
- `failure`: 테스트 실패
- `unknown`: 상태 불명

### 환경별 실행 전략

- **Dev**: 스모크 테스트 + P0 테스트 (개발/검증 단계)
- **Stage**: 전체 회귀 테스트 (Dev 검증 후)
- **Live**: 읽기 전용 스모크 테스트 (최종 검증)
