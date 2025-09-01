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
                "record_video_dir": f"reports/{self.config.environment}/videos",
                "record_video_size": {"width": 1920, "height": 1080},
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
    
    async def take_screenshot(self, test_name: str, status: str = "unknown") -> str:
        """Take screenshot and save to reports directory with test name and status."""
        if not self.page:
            raise RuntimeError("Browser page not initialized")
        
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
    
    async def start_video_recording(self, test_name: str, status: str = "unknown") -> str:
        """Start video recording with test name and status."""
        if not self.page:
            raise RuntimeError("Browser page not initialized")
        
        # Create reports directory if it doesn't exist
        video_dir = Path(f"reports/{self.config.environment}/videos")
        video_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename with test name, status, and timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{status}_{timestamp}.webm"
        filepath = video_dir / filename
        
        try:
            # Start video recording
            await self.page.video.save_as(str(filepath))
            self.logger.info(f"Video recording started: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Failed to start video recording: {e}")
            raise
    
    async def stop_video_recording(self, test_name: str = "test", status: str = "unknown") -> str:
        """Stop video recording and save with custom filename."""
        try:
            if self.page and self.page.video:
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
                return ""
        except Exception as e:
            self.logger.error(f"Failed to stop video recording: {e}")
            raise
    
    async def close_browser(self, test_name: str = "test", status: str = "unknown") -> None:
        """Close browser and cleanup resources."""
        try:
            # Save video before closing
            if self.context and hasattr(self.context, 'close'):
                try:
                    # Playwright automatically saves video when context closes
                    self.logger.info(f"Video will be saved automatically for test: {test_name}_{status}")
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
        status = "failure" if exc_type else "success"
        test_name = getattr(self, 'current_test_name', 'test')
        
        # Set video filename before closing
        if self.context and hasattr(self.context, 'close'):
            try:
                # Rename the video file to include test name and status
                import os
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                video_filename = f"{test_name}_{status}_{timestamp}.webm"
                
                # Get the default video directory
                video_dir = f"reports/{self.config.environment}/videos"
                if os.path.exists(video_dir):
                    # Find the most recent video file and rename it
                    video_files = [f for f in os.listdir(video_dir) if f.endswith('.webm')]
                    if video_files:
                        # Sort by modification time and get the most recent
                        video_files.sort(key=lambda x: os.path.getmtime(os.path.join(video_dir, x)), reverse=True)
                        old_name = video_files[0]
                        old_path = os.path.join(video_dir, old_name)
                        new_path = os.path.join(video_dir, video_filename)
                        
                        if os.path.exists(old_path):
                            os.rename(old_path, new_path)
                            self.logger.info(f"Video renamed to: {video_filename}")
            except Exception as e:
                self.logger.warning(f"Failed to rename video: {e}")
        
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
