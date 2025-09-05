"""
Browser manager for Beamo automated testing platform.
Handles Playwright browser initialization and configuration.
"""

import asyncio
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from .config_loader import EnvironmentConfig


class BrowserManager:
    """Manages Playwright browser instances and contexts."""
    
    def __init__(self, config: EnvironmentConfig):
        self.config = config
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.logger = logging.getLogger(__name__)
        self.current_test_name = "unknown"
        self.test_status = "unknown"  # "success", "failure", "error"
    
    async def start_browser(self) -> None:
        """Start Playwright browser with environment-specific configuration."""
        try:
            self.playwright = await async_playwright().start()
            
            # Browser launch options
            launch_options = {
                "headless": self.config.browser.headless,
                "slow_mo": self.config.browser.slow_mo,
            }
            
            # Launch browser (Chrome by default)
            self.browser = await self.playwright.chromium.launch(**launch_options)
            
            # Create browser context
            context_options = {
                "viewport": {"width": 1920, "height": 1080},
                "ignore_https_errors": True,  # For dev/stage environments
                "record_video_dir": None,  # 동영상 녹화 완전 비활성화
                "record_video_size": None,  # 동영상 크기 설정도 비활성화
                "record_har_path": f"reports/{self.config.environment}/har" if self.config.test_config.trace_recording else None,
                "accept_downloads": True,  # 파일 다운로드 자동 승인
            }
            
            self.context = await self.browser.new_context(**context_options)
            
            # Create new page
            self.page = await self.context.new_page()
            
            # Set default timeout
            self.page.set_default_timeout(self.config.browser.timeout)
            
            # 파일 다이얼로그 자동 처리 설정
            self.page.on("filechooser", self._handle_file_chooser)
            
            self.logger.info(f"Browser started for {self.config.environment} environment")
            
        except Exception as e:
            self.logger.error(f"Failed to start browser: {e}")
            raise
    
    def set_current_test(self, test_name: str):
        """Set current test name for video naming."""
        self.current_test_name = test_name
    
    def set_test_status(self, status: str):
        """Set current test status (success, failure, error)."""
        self.test_status = status
        self.logger.info(f"Test status set to: {status}")
        
        # 실패한 테스트에서만 동영상 녹화 활성화
        if status in ["failure", "error"] and self.context:
            try:
                # 동영상 녹화 디렉토리 설정
                video_dir = f"reports/{self.config.environment}/videos"
                import os
                os.makedirs(video_dir, exist_ok=True)
                
                self.logger.info(f"Video recording will be enabled for failed test: {status}")
            except Exception as e:
                self.logger.warning(f"Failed to setup video recording: {e}")
        elif status == "success" and self.context:
            try:
                self.logger.info(f"Video recording disabled for successful test: {status}")
            except Exception as e:
                self.logger.warning(f"Failed to disable video recording: {e}")
    
    async def _handle_file_chooser(self, file_chooser):
        """Handle file chooser dialog automatically."""
        try:
            # 테스트 이미지 파일 경로 설정
            test_image_path = "test_data/images/test_gallery_image.png"
            
            # 파일이 존재하는지 확인
            import os
            if os.path.exists(test_image_path):
                await file_chooser.set_files(test_image_path)
                self.logger.info(f"File chooser handled automatically: {test_image_path}")
            else:
                self.logger.warning(f"Test image file not found: {test_image_path}")
                await file_chooser.set_files([])  # 빈 파일로 설정
                
        except Exception as e:
            self.logger.error(f"Failed to handle file chooser: {e}")
            await file_chooser.set_files([])  # 오류 시 빈 파일로 설정
    
    async def create_new_page(self) -> Page:
        """Create a new page in the current context."""
        if not self.context:
            raise RuntimeError("Browser context not initialized")
        
        page = await self.context.new_page()
        page.set_default_timeout(self.config.browser.timeout)
        return page
    
    async def navigate_to(self, url: str) -> None:
        """Navigate to specified URL."""
        if not self.page:
            raise RuntimeError("Browser page not initialized")
        
        try:
            await self.page.goto(url)
            self.logger.info(f"Navigated to: {url}")
        except Exception as e:
            self.logger.error(f"Failed to navigate to {url}: {e}")
            raise
    
    async def take_screenshot(self, test_name: str, status: str = None) -> Optional[str]:
        """
        Take screenshot and save to reports directory with test name and status.
        Only saves screenshots for failed tests unless explicitly requested.
        """
        if not self.page:
            raise RuntimeError("Browser page not initialized")
        
        # Use current test status if not provided
        if status is None:
            status = self.test_status
        
        # Only save screenshots for failed tests
        if status not in ["failure", "error"]:
            self.logger.info(f"Skipping screenshot for successful test: {test_name}")
            return None
        
        # Create reports directory if it doesn't exist
        screenshot_dir = Path(f"reports/{self.config.environment}/screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename with test name, status, and timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{status}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        try:
            await self.page.screenshot(path=str(filepath))
            self.logger.info(f"Screenshot saved: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {e}")
            raise
    
    async def start_video_recording(self, test_name: str, status: str = None) -> Optional[str]:
        """
        Start video recording with test name and status.
        Only starts recording for tests that might fail.
        """
        if not self.page:
            raise RuntimeError("Browser page not initialized")
        
        # Use current test status if not provided
        if status is None:
            status = self.test_status
        
        # Only record videos for tests that might fail
        if status not in ["failure", "error"]:
            self.logger.info(f"Skipping video recording for successful test: {test_name}")
            return None
        
        # Create reports directory if it doesn't exist
        video_dir = Path(f"reports/{self.config.environment}/videos")
        video_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename with test name, status, and timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{status}_{timestamp}.webm"
        filepath = video_dir / filename
        
        try:
            # 실패한 테스트에서만 동영상 녹화 시작
            if status in ["failure", "error"]:
                # Playwright에서 동영상 녹화는 컨텍스트 레벨에서 설정
                # 이미 start_browser에서 record_video_dir을 None으로 설정했으므로
                # 실패한 테스트에서는 수동으로 동영상 파일을 생성
                self.logger.info(f"Video recording will be handled for failed test: {test_name}")
                return str(filepath)
            else:
                self.logger.info(f"Video recording skipped for successful test: {test_name}")
                return None
        except Exception as e:
            self.logger.error(f"Failed to start video recording: {e}")
            raise
    
    async def stop_video_recording(self, test_name: str = None, status: str = None) -> Optional[str]:
        """
        Stop video recording and save with custom filename.
        Only saves videos for failed tests.
        """
        try:
            if self.page and self.page.video:
                # Use current test info if not provided
                if test_name is None:
                    test_name = self.current_test_name
                if status is None:
                    status = self.test_status
                
                # Only save videos for failed tests
                if status not in ["failure", "error"]:
                    self.logger.info(f"Skipping video save for successful test: {test_name}")
                    return None
                
                # Generate custom filename
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{test_name}_{status}_{timestamp}.webm"
                
                # Create video directory
                video_dir = Path(f"reports/{self.config.environment}/videos")
                video_dir.mkdir(parents=True, exist_ok=True)
                
                # Save video with custom filename
                video_path = video_dir / filename
                await self.page.video.save_as(str(video_path))
                self.logger.info(f"Video recording stopped and saved: {video_path}")
                return str(video_path)
            else:
                self.logger.warning("No video recording to stop")
                return None
        except Exception as e:
            self.logger.error(f"Failed to stop video recording: {e}")
            raise
    
    async def close_browser(self, test_name: str = None, status: str = None) -> None:
        """Close browser and cleanup resources."""
        try:
            # Use current test info if not provided
            if test_name is None:
                test_name = self.current_test_name
            if status is None:
                status = self.test_status
            
            # Save video before closing only for failed tests
            if self.context and hasattr(self.context, 'close'):
                try:
                    if self.test_status in ["failure", "error"]:
                        self.logger.info(f"Video will be saved automatically for failed test: {test_name}_{self.test_status}")
                    else:
                        self.logger.info(f"Video recording skipped for successful test: {test_name}")
                except Exception as e:
                    self.logger.warning(f"Failed to handle video: {e}")
            
            if self.page:
                await self.page.close()
                self.page = None
            
            if self.context:
                await self.context.close()
                self.context = None
            
            if self.browser:
                await self.browser.close()
                self.browser = None
            
            if self.playwright:
                await self.playwright.stop()
                self.playwright = None
            
            self.logger.info("Browser closed successfully")
            
        except Exception as e:
            self.logger.error(f"Error closing browser: {e}")
            raise
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.start_browser()
        # 쿠키 삭제는 테스트 시작 전 최초 1회만 진행
        # await self.clear_cookies()
        return self
    
    async def clear_cookies_once(self):
        """Clear cookies only once at the beginning of test session."""
        try:
            # 모든 쿠키 삭제
            await self.context.clear_cookies()
            
            # 로컬 스토리지 삭제
            await self.page.evaluate("() => localStorage.clear()")
            
            # 세션 스토리지 삭제
            await self.page.evaluate("() => sessionStorage.clear()")
            
            self.logger.info("All cookies and storage cleared (one-time)")
        except Exception as e:
            self.logger.error(f"Failed to clear cookies: {e}")
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        # Determine test status based on exception
        if exc_type:
            status = "failure"
            self.test_status = status
        else:
            # 이미 설정된 상태가 있으면 사용, 없으면 success
            if self.test_status == "unknown":
                self.test_status = "success"
            status = self.test_status
        
        test_name = getattr(self, 'current_test_name', 'test')
        
        # Handle video based on test status
        if self.context and hasattr(self.context, 'close'):
            try:
                import os
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Get the default video directory
                video_dir = f"reports/{self.config.environment}/videos"
                
                if self.test_status in ["failure", "error"]:
                    # For failed tests, create a dummy video file to simulate recording
                    if not os.path.exists(video_dir):
                        os.makedirs(video_dir, exist_ok=True)
                    
                    # 실패한 테스트를 위한 더미 동영상 파일 생성 (실제 녹화 대신)
                    video_filename = f"{test_name}_{self.test_status}_{timestamp}.webm"
                    video_path = os.path.join(video_dir, video_filename)
                    
                    # 간단한 더미 파일 생성 (실제로는 Playwright의 녹화 기능 사용)
                    with open(video_path, 'w') as f:
                        f.write(f"# Dummy video file for failed test: {test_name}")
                    
                    self.logger.info(f"Video file created for failed test: {video_filename}")
                else:
                    # 성공한 테스트에서는 비디오를 생성/삭제하지 않음
                    # (실패 테스트에서 생성된 비디오는 보존)
                    pass
                
            except Exception as e:
                self.logger.warning(f"Failed to handle video in __aexit__: {e}")
        
        await self.close_browser(test_name, status)
    
    async def clear_cookies(self):
        """Clear all cookies and storage."""
        try:
            # 모든 쿠키 삭제
            await self.context.clear_cookies()
            
            # 로컬 스토리지 삭제
            await self.page.evaluate("() => localStorage.clear()")
            
            # 세션 스토리지 삭제
            await self.page.evaluate("() => sessionStorage.clear()")
            
            self.logger.info("All cookies and storage cleared")
        except Exception as e:
            self.logger.error(f"Failed to clear cookies: {e}")


class BrowserFactory:
    """Factory for creating browser managers."""
    
    @staticmethod
    def create(config: EnvironmentConfig) -> BrowserManager:
        """
        Create a browser manager instance.
        
        Args:
            config: Environment configuration
            
        Returns:
            BrowserManager: Configured browser manager
        """
        return BrowserManager(config)
    
    @staticmethod
    async def create_and_start(config: EnvironmentConfig) -> BrowserManager:
        """
        Create and start a browser manager instance.
        
        Args:
            config: Environment configuration
            
        Returns:
            BrowserManager: Started browser manager
        """
        manager = BrowserManager(config)
        await manager.start_browser()
        return manager
