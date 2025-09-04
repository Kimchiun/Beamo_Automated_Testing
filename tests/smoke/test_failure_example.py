#!/usr/bin/env python3
"""
실패하는 테스트 예제 - 스크린샷과 동영상 저장 테스트용
"""

import pytest
import asyncio
from utils.browser_manager import BrowserManager
from utils.config_loader import get_config


class TestFailureExample:
    """실패하는 테스트 예제 클래스"""
    
    @pytest.mark.asyncio
    async def test_forced_failure(self):
        """강제로 실패하는 테스트 - 스크린샷과 동영상 저장 확인용"""
        config = get_config("dev")
        
        async with BrowserManager(config) as browser_manager:
            # 테스트 이름과 상태 설정
            browser_manager.set_current_test("forced_failure_test")
            browser_manager.set_test_status("failure")
            
            # 페이지 이동
            await browser_manager.navigate_to("https://accounts.beamo.dev/login")
            
            # 동영상 녹화 시작 (실패한 테스트이므로 녹화됨)
            video_path = await browser_manager.start_video_recording("forced_failure_test")
            assert video_path is not None, "실패한 테스트에서는 동영상 녹화가 시작되어야 합니다"
            
            # 스크린샷 촬영 (실패한 테스트이므로 저장됨)
            screenshot_path = await browser_manager.take_screenshot("forced_failure_test")
            assert screenshot_path is not None, "실패한 테스트에서는 스크린샷이 저장되어야 합니다"
            
            # 강제로 테스트 실패
            assert False, "이 테스트는 의도적으로 실패합니다"
    
    @pytest.mark.asyncio
    async def test_success_no_artifacts(self):
        """성공하는 테스트 - 스크린샷과 동영상이 저장되지 않는지 확인"""
        config = get_config("dev")
        
        async with BrowserManager(config) as browser_manager:
            # 테스트 이름과 상태 설정
            browser_manager.set_current_test("success_test")
            browser_manager.set_test_status("success")
            
            # 페이지 이동
            await browser_manager.navigate_to("https://accounts.beamo.dev/login")
            
            # 스크린샷 촬영 (성공한 테스트이므로 저장되지 않음)
            screenshot_path = await browser_manager.take_screenshot("success_test")
            assert screenshot_path is None, "성공한 테스트에서는 스크린샷이 저장되지 않아야 합니다"
            
            # 테스트 성공
            assert True, "이 테스트는 성공해야 합니다"
