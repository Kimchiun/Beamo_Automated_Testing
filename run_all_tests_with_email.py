#!/usr/bin/env python3
"""
Beamo 전체 테스트 실행 및 이메일 리포트 전송
"""

import asyncio
import sys
import time
import subprocess
from pathlib import Path
from typing import List, Dict, Any
import logging
import re

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.config_loader import get_config
from utils.email_sender import EmailSender

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('reports/test_execution.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class TestRunnerWithEmail:
    """테스트 실행 및 이메일 전송을 담당하는 클래스"""
    
    def __init__(self, environment: str = "dev"):
        self.environment = environment
        self.config = get_config(environment)
        self.start_time = None
        self.end_time = None
        
        # 이메일 설정 확인
        if not hasattr(self.config, 'email') or not self.config.email:
            logger.warning("이메일 설정이 없습니다. config.yaml에 email 섹션을 추가해주세요.")
            self.email_enabled = False
        else:
            self.email_enabled = True
            try:
                # Pydantic v2 호환성
                if hasattr(self.config.email, 'model_dump'):
                    email_config = self.config.email.model_dump()
                else:
                    email_config = self.config.email.dict()
                
                self.email_sender = EmailSender(email_config)
                logger.info("이메일 전송기 초기화 완료")
            except Exception as e:
                logger.error(f"이메일 전송기 초기화 실패: {e}")
                self.email_enabled = False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """전체 테스트 실행"""
        logger.info(f"🚀 {self.environment} 환경에서 전체 테스트 실행 시작")
        self.start_time = time.time()
        
        try:
            result = self._execute_pytest()
            self.end_time = time.time()
            execution_time = self.end_time - self.start_time
            
            test_summary = self._generate_test_summary(result, execution_time)
            logger.info(f"✅ 테스트 실행 완료 (소요시간: {execution_time:.1f}초)")
            return test_summary
            
        except Exception as e:
            logger.error(f"❌ 테스트 실행 중 오류 발생: {e}")
            self.end_time = time.time()
            execution_time = self.end_time - self.start_time
            
            return {
                "total_tests": 0,
                "passed_tests": 0,
                "failed_tests": 0,
                "skipped_tests": 0,
                "execution_time": f"{execution_time:.1f}s",
                "environment": self.environment,
                "status": "error",
                "error_message": str(e)
            }
    
    def _execute_pytest(self) -> subprocess.CompletedProcess:
        """pytest 실행"""
        cmd = [
            sys.executable, "-m", "pytest",
            "tests",
            "-v",
            "--tb=short",
            f"--html=reports/{self.environment}/test_report.html",
            "--self-contained-html",
            "--capture=no",
        ]
        
        logger.info(f"실행 명령어: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=project_root,
            timeout=300
        )
        
        return result
    
    def _generate_test_summary(self, result: subprocess.CompletedProcess, execution_time: float) -> Dict[str, Any]:
        """테스트 결과 요약 생성"""
        output = result.stdout + result.stderr
        
        # pytest 세션 결과에서 추출
        passed_tests = 0
        failed_tests = 0
        skipped_tests = 0
        
        if "passed in" in output:
            passed_match = re.search(r'(\d+) passed', output)
            if passed_match:
                passed_tests = int(passed_match.group(1))
        
        if "failed" in output:
            failed_match = re.search(r'(\d+) failed', output)
            if failed_match:
                failed_tests = int(failed_match.group(1))
        
        total_tests = passed_tests + failed_tests + skipped_tests
        
        # 상태 판단
        if result.returncode == 0:
            status = "success"
        elif failed_tests > 0:
            status = "failure"
        else:
            status = "error"
        
        summary = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "skipped_tests": skipped_tests,
            "execution_time": f"{execution_time:.1f}s",
            "environment": self.environment,
            "status": status,
            "return_code": result.returncode
        }
        
        logger.info(f"📊 테스트 결과 요약: {summary}")
        return summary
    
    def collect_artifacts(self) -> tuple[List[str], List[str]]:
        """테스트 아티팩트 수집"""
        reports_dir = Path(f"reports/{self.environment}")
        
        screenshots = []
        videos = []
        
        if reports_dir.exists():
            screenshot_dir = reports_dir / "screenshots"
            if screenshot_dir.exists():
                screenshots = [str(f) for f in screenshot_dir.glob("*.png")]
            
            video_dir = reports_dir / "videos"
            if video_dir.exists():
                videos = [str(f) for f in video_dir.glob("*.webm")]
        
        logger.info(f"📎 수집된 아티팩트: 스크린샷 {len(screenshots)}개, 동영상 {len(videos)}개")
        return screenshots, videos
    
    def send_email_report(self, test_summary: Dict[str, Any]) -> bool:
        """테스트 결과 이메일 전송"""
        if not self.email_enabled:
            logger.warning("이메일 기능이 비활성화되어 있습니다.")
            return False
        
        try:
            screenshots, videos = self.collect_artifacts()
            success = self.email_sender.send_test_report(test_summary, screenshots, videos)
            
            if success:
                logger.info("📧 테스트 결과 이메일 전송 완료")
            else:
                logger.error("❌ 테스트 결과 이메일 전송 실패")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ 이메일 전송 중 오류 발생: {e}")
            return False
    
    def run(self) -> bool:
        """전체 테스트 실행 및 이메일 전송"""
        try:
            test_summary = self.run_all_tests()
            
            if self.email_enabled and test_summary.get("send_on_completion", True):
                email_success = self.send_email_report(test_summary)
                if email_success:
                    logger.info("🎉 테스트 실행 및 이메일 전송 완료!")
                else:
                    logger.warning("⚠️ 테스트는 완료되었지만 이메일 전송에 실패했습니다.")
            else:
                logger.info("📧 이메일 전송이 비활성화되어 있습니다.")
            
            return test_summary.get("status") in ["success", "failure"]
            
        except Exception as e:
            logger.error(f"❌ 전체 프로세스 실행 중 오류 발생: {e}")
            return False


async def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Beamo 전체 테스트 실행 및 이메일 리포트 전송")
    parser.add_argument(
        "--environment", "-e", default="dev", 
        choices=["dev", "stage", "live"],
        help="실행할 환경 (기본값: dev)"
    )
    parser.add_argument(
        "--no-email", action="store_true",
        help="이메일 전송 비활성화"
    )
    
    args = parser.parse_args()
    
    runner = TestRunnerWithEmail(args.environment)
    
    if args.no_email:
        runner.email_enabled = False
        logger.info("이메일 전송이 비활성화되었습니다.")
    
    success = runner.run()
    
    if success:
        logger.info("✅ 모든 작업이 성공적으로 완료되었습니다.")
        sys.exit(0)
    else:
        logger.error("❌ 일부 작업에서 오류가 발생했습니다.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
