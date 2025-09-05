import os
from pathlib import Path
import pytest


# 각 테스트의 성공/실패 리포트를 item 속성으로 저장
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(autouse=True)
def cleanup_artifacts_on_success(request):
    """
    테스트 시작 시점의 스크린샷/비디오 목록을 기록하고,
    테스트가 성공하면 새로 생성된 파일을 삭제한다.
    (실패 케이스에서만 산출물이 남도록 강제)
    """
    # 환경 디렉터리 추정 (기본 dev) — 필요 시 BEAMO_ENV 로 분기
    env = os.getenv("BEAMO_ENV", "dev")
    screenshots_dir = Path(f"reports/{env}/screenshots")
    videos_dir = Path(f"reports/{env}/videos")

    before_shots = set(screenshots_dir.glob("*.png")) if screenshots_dir.exists() else set()
    before_vids = set(videos_dir.glob("*.webm")) if videos_dir.exists() else set()

    yield

    # call 단계의 결과로 성공/실패 판단
    rep_call = getattr(request.node, "rep_call", None)
    failed = bool(rep_call and rep_call.failed)

    if not failed:
        after_shots = set(screenshots_dir.glob("*.png")) if screenshots_dir.exists() else set()
        after_vids = set(videos_dir.glob("*.webm")) if videos_dir.exists() else set()
        new_files = (after_shots - before_shots) | (after_vids - before_vids)
        for f in new_files:
            try:
                f.unlink()
            except Exception:
                pass


