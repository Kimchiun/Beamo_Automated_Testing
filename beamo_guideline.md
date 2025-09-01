# Beamo Automated Testing Platform - Development Guidelines

## 1. 프로젝트 개요

이 프로젝트는 **Beamo Portal 및 App(Web/Android/iOS)**의 주요 사용자 흐름을 자동화 검증하기 위한 Python + Playwright + Appium 기반 E2E 테스트 스위트를 제공합니다.
환경별(dev/stage/live) 핵심 시나리오를 빠르고 일관되게 검증할 수 있습니다.

### 환경 구성
- **Dev**: https://accounts.beamo.dev/login
- **Stage**: https://accounts.3inc.xyz/login  
- **Live**: https://accounts.beamo.ai/login

## 2. 핵심 원칙

- **크로스 플랫폼 신뢰성**: Web, Android, iOS에서 일관되게 실행
- **유지보수성**: 모듈화된 POM 구조로 유지보수 비용 최소화
- **재사용성**: 환경 간 공통 플로우 재사용
- **확장성**: 새로운 Beamo 기능으로 쉽게 확장
- **관찰 가능성**: 실패 시 액션 가능한 로그, 스크린샷, 비디오, 트레이스 제공

## 3. 언어별 가이드라인

### Python

#### 파일 구성
- `pages/`, `flows/`, `fixtures/`, `utils/`, `tests/` 디렉토리 분리
- Beamo 페이지/모듈당 하나의 POM 파일 (`login_page.py`, `dashboard_page.py`)
- 환경별 설정을 `config/`에 저장

#### Import 규칙
- 공유 유틸리티는 절대 import: `from utils.config_loader import load_env_config`
- 같은 패키지 내에서는 상대 import: `from .login_page import LoginPage`
- PEP8 import 그룹화 준수 (stdlib → third-party → local)

#### 에러 처리
- Playwright 호출을 재시도로 감싸서 불안정한 네트워크/UI 처리
- `logging` 모듈로 구조화된 로그 사용 (`INFO`, `WARNING`, `ERROR`)
- 예외 재발생 전에 스택 트레이스, 스크린샷, 네트워크 로그 캡처

```python
try:
    await page.locator("data-testid=login-btn").click()
except TimeoutError as e:
    logging.error(f"[Stage][Login] Timeout during login: {e}")
    await page.screenshot(path="artifacts/login_timeout.png")
    raise
```

### Playwright (Web/Mobile Web)
- Page Object Model 사용: 각 Portal 화면 = 하나의 POM 클래스
- Locator 우선순위: data-testid → role → aria-label; XPath 지양
- DOM idle/network settled 대기 후 assertion
- 테스트 태그: @smoke, @regression, @p0, @stage

```python
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.login_button = "data-testid=login-btn"

    async def click_login(self):
        await self.page.locator(self.login_button).click()
```

### Docker
- `.dockerignore`로 캐시, 로그, venv 제외
- Multi-stage 빌드 (base Python + dependencies → slim runtime)
- 보안을 위해 non-root 사용자로 실행
- 환경 변수로 환경 설정 (BEAMO_ENV=stage)

### YAML (설정)
- 환경별 설정 파일: config.dev.yaml, config.stage.yaml, config.live.yaml
- 테스트 데이터(URL, 자격증명, 타임아웃)를 YAML에 저장
- 설정을 선언적으로 유지, 비즈니스 로직 포함 금지
- 로드 시 설정 검증

## 4. 코드 스타일 규칙

### MUST
- PEP8 준수 (Black/Flake8 강제)
- 모듈/클래스/메서드에 docstring
- 모든 함수 시그니처에 타입 힌트
- 일관된 형식으로 logging 사용 `[ENV][Module][Step]`
- 테스트 케이스를 50줄 이하로 유지, 로직은 POM/flows에 위임
- 단일 책임 원칙(SRP) 적용

```python
async def test_login_smoke(beamo_portal):
    """
    Smoke test: Login and verify dashboard loaded
    """
    portal = beamo_portal
    await portal.login("smoke_admin")
    assert await portal.dashboard_visible()
```

### MUST NOT
- 테스트 플로우 중복 (flows/ 재사용)
- 자격증명, URL, 선택자 하드코딩
- 예외를 조용히 무시
- 시크릿이나 환경 설정을 repo에 커밋
- 전역 가변 상태 사용

## 5. 아키텍처 패턴

### 도메인 주도 설계
각 Beamo 모듈(SITE, SETTING, DATA, USER, SPACE)마다 자체 POM & flow

### 단방향 데이터 흐름
Fixtures → Flows → POM → Assertions

### DTO
레이어 간 구조화된 데이터 전달용 (예: site profile)

### 인터페이스 우선
공개 메서드는 비즈니스 액션을 노출, DOM 세부사항은 숨김

```python
# GOOD: 사용자 여정을 캡슐화하는 Flow
class LoginFlow:
    async def login_and_verify_dashboard(self, portal, credentials):
        await portal.login_page.login(credentials)
        assert await portal.dashboard_page.is_loaded()
```

## 6. 테스트 태깅 & 실행 전략

### 태그
- `@smoke`: 최소 P0 시나리오 (≤10분)
- `@regression`: 전체 회귀 스위트
- `@synthetic`: 읽기 전용 live 모니터링 테스트

### 환경별 실행
- **Dev**: 스모크 + P0 테스트
- **Stage**: 전체 회귀 테스트
- **Live**: 읽기 전용 스모크 테스트

## 7. CI/CD 통합

### GitHub Actions & Jenkins 파이프라인
- 모든 PR에서 스모크 스위트 실행 → Dev
- Stage에서 매일 밤 전체 회귀 테스트
- Live에서 스케줄된 Synthetic 모니터링

### 아티팩트 업로드
- 스크린샷, 비디오, 트레이스를 CI에 업로드
- 실패 시 Slack 알림

```yaml
# GitHub Actions 예시
- name: Run Tests
  run: |
    python run_tests.py --env stage --tags regression
    
- name: Upload Test Results
  uses: actions/upload-artifact@v2
  with:
    name: test-results
    path: reports/
```

## 8. 개발 전략 및 테스트 실행

### 개발 전략: Dev-First 접근법

**핵심 원칙**: Dev 환경을 기준으로 구축하고 성공한 후 다른 환경에 적용

#### 단계별 개발 프로세스

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

#### 환경별 구성요소 동일성 보장

- **공통 구조**: 모든 환경에서 동일한 Page Object Model 사용
- **설정 분리**: 환경별 차이점은 `config/*.yaml` 파일에서만 관리
- **코드 재사용**: 테스트 로직은 환경에 독립적으로 작성
- **점진적 검증**: Dev → Stage → Live 순서로 단계적 검증

### 테스트 실행 예시

#### 로컬 실행
```bash
# Dev 환경 스모크 테스트 (개발 단계)
python run_tests.py --env dev --tags smoke

# Dev 환경 회귀 테스트 (검증 단계)
python run_tests.py --env dev --tags regression

# Stage 환경 테스트 (Dev 검증 후)
python run_tests.py --env stage --tags smoke

# Live 환경 테스트 (최종 검증)
python run_tests.py --env live --tags smoke
```

#### Docker 실행
```bash
# 이미지 빌드
docker build -t beamo-test .

# Dev 환경 실행 (개발/검증)
docker run -e BEAMO_ENV=dev beamo-test

# Stage 환경 실행 (Dev 검증 후)
docker run -e BEAMO_ENV=stage beamo-test

# Live 환경 실행 (최종)
docker run -e BEAMO_ENV=live beamo-test
```

## 9. 디버깅 & 트러블슈팅

### 일반적인 문제
1. **타임아웃**: 환경별 타임아웃 설정 확인
2. **선택자 변경**: DOM 구조 변경 시 POM 업데이트
3. **환경 차이**: 환경별 설정 파일 검증
4. **네트워크 문제**: 재시도 로직 및 에러 처리 확인

### 로그 분석
- `test_execution.log`에서 상세 로그 확인
- HTML 리포트에서 실패 케이스 분석
- 스크린샷으로 UI 상태 확인

## 10. 성능 최적화

### 테스트 실행 시간 단축
- 병렬 실행 활용 (`--parallel 4`)
- 불필요한 대기 시간 최소화
- 스크린샷/비디오 녹화 조건부 활성화

### 리소스 사용량 최적화
- 브라우저 컨텍스트 재사용
- 메모리 누수 방지를 위한 적절한 cleanup
- Docker 컨테이너 리소스 제한 설정

---

이 가이드라인을 따라 개발하면 일관되고 유지보수 가능한 자동화 테스트 플랫폼을 구축할 수 있습니다.
