# 📧 Gmail 앱 비밀번호 설정 가이드

Beamo 자동화 테스트 결과를 이메일로 전송하기 위해 Gmail 앱 비밀번호를 설정하는 방법입니다.

## 🔐 1단계: Gmail 2단계 인증 활성화

1. [Google 계정 보안 설정](https://myaccount.google.com/security)에 접속
2. **2단계 인증** 섹션에서 **2단계 인증 사용** 클릭
3. 휴대폰 번호 인증 및 보안 질문 설정 완료

## 🔑 2단계: 앱 비밀번호 생성

1. **2단계 인증** 섹션에서 **앱 비밀번호** 클릭
2. **앱 선택** 드롭다운에서 **기타 (사용자 지정 이름)** 선택
3. 앱 이름 입력: `Beamo Test Automation`
4. **생성** 버튼 클릭
5. 생성된 **16자리 앱 비밀번호** 복사 (예: `abcd efgh ijkl mnop`)

## ⚙️ 3단계: 설정 파일 업데이트

`config/dev.yaml` 파일의 이메일 설정을 업데이트하세요:

```yaml
# Email Configuration
email:
  smtp_server: "smtp.gmail.com"
  smtp_port: 587
  sender_email: "your-actual-gmail@gmail.com"  # 실제 Gmail 주소로 변경
  sender_password: "abcd efgh ijkl mnop"       # 생성된 앱 비밀번호로 변경
  recipient_email: "steve.kim@3i.ai"
  send_on_completion: true
```

## 🚀 4단계: 테스트 실행

이제 전체 테스트를 실행하고 결과를 이메일로 받을 수 있습니다:

```bash
# 전체 테스트 실행 + 이메일 전송
python run_all_tests_with_email.py

# 특정 환경에서 실행
python run_all_tests_with_email.py --environment stage

# 이메일 전송 없이 테스트만 실행
python run_all_tests_with_email.py --no-email
```

## 📋 이메일 내용

전송되는 이메일에는 다음 정보가 포함됩니다:

- **테스트 요약**: 전체/성공/실패/건너뜀 테스트 수
- **성공률**: 백분율로 표시
- **실행 시간**: 총 소요 시간
- **첨부 파일**: 스크린샷 및 동영상 (25MB 이하)
- **HTML 리포트**: 상세한 테스트 결과

## 🔒 보안 주의사항

- **앱 비밀번호는 절대 공유하지 마세요**
- **Git에 커밋하지 마세요** (`.gitignore`에 추가 권장)
- **정기적으로 앱 비밀번호를 재생성하세요**
- **프로덕션 환경에서는 환경변수 사용을 권장합니다**

## 🌍 환경변수 사용 (권장)

보안을 위해 환경변수를 사용할 수 있습니다:

```bash
export BEAMO_EMAIL_PASSWORD="your-app-password"
```

그리고 `config/dev.yaml`에서:

```yaml
email:
  sender_password: "${BEAMO_EMAIL_PASSWORD}"
```

## ❓ 문제 해결

### "Authentication failed" 오류
- 2단계 인증이 활성화되어 있는지 확인
- 앱 비밀번호가 정확한지 확인
- Gmail 계정이 잠기지 않았는지 확인

### "SMTP connection failed" 오류
- 방화벽에서 587 포트가 열려있는지 확인
- 회사 네트워크에서 SMTP 차단 여부 확인

### 이메일이 수신되지 않는 경우
- 스팸 폴더 확인
- `steve.kim@3i.ai` 주소가 정확한지 확인
- Gmail 계정의 보안 설정 확인

## 📞 지원

추가 도움이 필요하시면 개발팀에 문의해주세요!
