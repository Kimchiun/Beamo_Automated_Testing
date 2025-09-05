# Beamo Portal Automated Testing Platform

Beamo 포탈의 자동화 테스트 플랫폼입니다. Python과 Playwright를 사용하여 dev, stage, live 환경에서 일관된 E2E 테스트를 수행합니다.

## 🎯 프로젝트 목표

- **테스트 자동화**: 수동 QA 시간 70% 단축
- **빠른 피드백**: 스모크 테스트 10분 이내 완료
- **품질 보장**: 회귀 테스트 자동화로 릴리즈 안정성 확보
- **환경 일관성**: dev → stage → live 순차적 검증

## 🌍 환경 구성

| 환경 | URL | 용도 | 테스트 범위 |
|------|-----|------|-------------|
| **Dev** | https://accounts.beamo.dev/login | 개발/검증 | 스모크 + 회귀 |
| **Stage** | https://accounts.3inc.xyz/login | 베타 검증 | 스모크 + 회귀 |
| **Live** | https://accounts.beamo.ai/login | 최종 검증 | 스모크만 |

## 🛠️ 기술 스택

| 카테고리 | 기술 | 버전 | 선택 이유 |
|----------|------|-------|-----------|
| **Language** | Python | 3.x | 높은 생산성, 풍부한 라이브러리 |
| **Testing** | Playwright | 최신 | 크로스 브라우저, 모바일 에뮬레이션 |
| **Reporting** | pytest-html | 4.1.1 | HTML 리포트, 시각적 결과 |
| **Email** | SMTP | Gmail | 자동 테스트 결과 전송 |
| **Container** | Docker | 최신 | 일관된 실행 환경 |
| **Config** | YAML | - | 가독성, 환경별 설정 |

## 📁 프로젝트 구조

```
Beamo_Automated_Testing/
├── 📁 config/                     # 환경별 설정 파일
│   ├── dev.yaml                   # 개발 환경 설정
│   ├── stage.yaml                 # 스테이징 환경 설정
│   └── live.yaml                  # 라이브 환경 설정
├── 📁 tests/                      # 테스트 시나리오
│   ├── smoke/                     # 스모크 테스트 (핵심 기능)
│   │   ├── test_login.py         # 로그인 테스트
│   │   ├── test_add_plan.py      # 플랜 추가 테스트
│   │   └── test_failure_example.py # 실패 테스트 예제
│   ├── regression/                # 회귀 테스트 (전체 기능)
│   └── analysis/                  # 분석 테스트 (디버깅용)
├── 📁 pages/                      # Page Object Model
│   ├── login_page.py             # 로그인 페이지
│   ├── dashboard_page.py         # 대시보드 페이지
│   └── components/               # 공통 컴포넌트
│       └── global_navigation.py  # 글로벌 네비게이션
├── 📁 utils/                      # 유틸리티 함수
│   ├── config_loader.py          # 설정 로더 (Pydantic)
│   ├── browser_manager.py        # 브라우저 관리 (Playwright)
│   └── email_sender.py           # 이메일 전송 유틸리티
├── 📁 reports/                    # 테스트 결과 및 아티팩트
│   ├── dev/                      # 개발 환경 결과
│   │   ├── screenshots/          # 스크린샷 (실패한 테스트만)
│   │   ├── videos/               # 동영상 (실패한 테스트만)
│   │   └── test_report.html     # HTML 테스트 리포트
│   ├── stage/                    # 스테이징 환경 결과
│   └── live/                     # 라이브 환경 결과
├── 📁 test_data/                  # 테스트 데이터
│   └── images/                   # 테스트용 이미지 파일
├── 📄 requirements.txt            # Python 의존성
├── 📄 Dockerfile                  # Docker 설정
├── 📄 run_tests.py               # 기본 테스트 실행 스크립트
├── 📄 run_all_tests_with_email.py # 전체 테스트 + 이메일 전송
├── 📄 GMAIL_SETUP_GUIDE.md       # Gmail 설정 가이드
└── 📄 README.md                   # 프로젝트 문서
```

## 🚀 빠른 시작

### 1. 환경 설정

#### Python 가상환경 생성
```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate     # Windows
```

#### 의존성 설치
```bash
pip install -r requirements.txt
```

#### Playwright 브라우저 설치
```bash
playwright install
```

### 2. 이메일 설정 (선택사항)

테스트 완료 후 결과를 이메일로 받으려면 Gmail 앱 비밀번호를 설정하세요:

```bash
# 1. GMAIL_SETUP_GUIDE.md 참조하여 앱 비밀번호 생성
# 2. config/dev.yaml에 이메일 설정 추가
```

```yaml
# config/dev.yaml
email:
  smtp_server: "smtp.gmail.com"
  smtp_port: 587
  sender_email: "your-email@gmail.com"      # Gmail 계정
  sender_password: "your-app-password"       # Gmail 앱 비밀번호
  recipient_email: "steve.kim@3i.ai"        # 수신자
  send_on_completion: true
```

### 3. 테스트 실행 (Dev-First 접근법)

#### 🧪 기본 테스트 실행
```bash
# Phase 1: Dev 환경 스모크 테스트 (개발/검증)
python -m pytest tests/smoke/ -v --tb=short

# Phase 1: Dev 환경 특정 테스트
python -m pytest tests/smoke/test_login.py::TestLoginSmoke::test_valid_login_dev -v

# Phase 2: Stage 환경 테스트 (Dev 검증 후)
python -m pytest tests/smoke/ -v --env stage

# Phase 3: Live 환경 테스트 (최종 검증)
python -m pytest tests/smoke/ -v --env live
```

#### 📧 전체 테스트 + 이메일 전송
```bash
# 전체 테스트 실행 및 결과를 steve.kim@3i.ai로 전송
python run_all_tests_with_email.py

# 특정 환경에서 실행
python run_all_tests_with_email.py --environment stage

# 이메일 전송 없이 테스트만 실행
python run_all_tests_with_email.py --no-email
```

#### 🐳 Docker로 실행
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

## ⚡ 테스트 성능

### 📊 현재 테스트 속도

| 테스트 유형 | 실행 시간 | 구성 요소 |
|-------------|-----------|-----------|
| **로그인 스모크** | ~11초 | 브라우저 시작(2초) + 테스트(8초) + 정리(1초) |
| **간단한 테스트** | ~3-4초 | 브라우저 시작(2초) + 테스트(1-2초) + 정리(0초) |
| **실패 테스트** | ~4초 | 브라우저 시작(2초) + 테스트(2초) + 정리(0초) |

### 🎯 성능 목표
- **스모크 테스트**: 10분 이내
- **개별 테스트**: 15초 이내
- **브라우저 시작**: 2초 이내

### 🔧 성능 특징
- ✅ **빠른 부분**: 브라우저 시작(2초), 리소스 정리(0.5초)
- ⚠️ **개선 필요**: 로그인 플로우(8초), 순차 실행

## 🎁 주요 기능

### ✅ 핵심 기능
- **크로스 브라우저 테스트**: Chrome, Firefox, Safari 지원
- **모바일 에뮬레이션**: Android/iOS 디바이스 시뮬레이션
- **환경별 설정 관리**: dev/stage/live 환경 분리
- **HTML 리포트 생성**: 시각적 테스트 결과
- **자동 아티팩트 관리**: 실패한 테스트에만 스크린샷/동영상 저장

### 📧 이메일 기능
- **자동 전송**: 테스트 완료 시 `steve.kim@3i.ai`로 결과 전송
- **HTML 리포트**: 시각적 테스트 통계 및 결과
- **아티팩트 첨부**: 스크린샷 및 동영상 자동 첨부
- **보안**: Gmail 앱 비밀번호, 환경변수 지원

### 🐳 Docker 지원
- **일관된 환경**: 로컬/CI 환경 동일한 실행 환경
- **멀티 스테이지**: 개발 → 스테이징 → 라이브 순차적 배포
- **CI/CD 연동**: GitHub Actions, Jenkins 파이프라인 지원

## 📊 아티팩트 관리

### 🎯 스마트 저장 전략
- **성공한 테스트**: 아티팩트 저장 안함 (저장 공간 절약)
- **실패한 테스트**: 스크린샷 + 동영상 모두 저장
- **자동 정리**: 성공한 테스트 후 기존 동영상 자동 삭제

### 💾 저장 공간 절약 효과
- **이전**: 모든 테스트에서 동영상 저장 (100% 저장)
- **현재**: 실패한 테스트에서만 동영상 저장 (10-20% 저장)
- **절약**: **80-90% 저장 공간 절약** 🎯

### 📁 파일 구조
```
reports/dev/
├── screenshots/                    # 실패한 테스트 스크린샷
│   └── test_name_failure_timestamp.png
├── videos/                        # 실패한 테스트 동영상
│   └── test_name_failure_timestamp.webm
└── test_report.html              # HTML 테스트 리포트
```

## 🔧 고급 기능

### 🧪 테스트 태깅
```bash
# 스모크 테스트만 실행
pytest -m smoke

# 회귀 테스트만 실행
pytest -m regression

# 특정 우선순위 테스트
pytest -m "p0 or p1"
```

### 📝 커스텀 설정
```yaml
# config/dev.yaml
test_config:
  screenshot_on_failure: true      # 실패 시 스크린샷
  video_recording: true            # 동영상 녹화
  trace_recording: false           # 트레이스 녹화
  timeout: 300                     # 테스트 타임아웃 (초)
```

### 🚀 CI/CD 연동
```yaml
# .github/workflows/test.yml
name: Beamo Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Tests
        run: |
          python -m pytest tests/smoke/ --html=reports/test_report.html
```

## 🐛 문제 해결

### 일반적인 문제들

#### 1. Playwright 브라우저 설치 실패
```bash
# 브라우저 재설치
playwright install --force
```

#### 2. 이메일 전송 실패
```bash
# Gmail 앱 비밀번호 확인
# 2단계 인증 활성화 필요
# config/dev.yaml 설정 확인
```

#### 3. 테스트 타임아웃
```yaml
# config/dev.yaml에서 타임아웃 증가
test_config:
  timeout: 600  # 10분으로 증가
```

---

**Beamo Automated Testing Platform** - 빠르고 안정적인 E2E 테스트 자동화 🚀
