"""
Login page object model for Beamo portal.
Handles login functionality across different environments.
"""

import logging
from typing import Optional
from playwright.async_api import Page
from utils.config_loader import EnvironmentConfig


class LoginPage:
    """Page Object Model for Beamo login page."""
    
    def __init__(self, page: Page, config: EnvironmentConfig):
        self.page = page
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Common selectors (based on actual Beamo login flow)
        self.selectors = {
            # 3단계 로그인
            "space_id_input": "input[name='spaceId']",
            "next_button": "button[type='submit']",
            "email_input": "input[name='userId']",
            "email_login_button": "button[type='submit']",
            "password_input": "input[name='userPassword']",
            "remember_me_checkbox": "input[type='checkbox']",
            "final_login_button": "button[type='submit']",
            
            # 새로운 1단계 로그인 (d-ge-eric)
            "user_id_input": "input[name='userId']",
            "login_button": "button[type='submit']",
            
            # 공통
            "error_message": ".error-message, .alert-error, [data-testid='error-message']",
            "success_message": ".success-message, .alert-success",
        }
    
    async def navigate_to_login(self) -> None:
        """Navigate to login page."""
        login_url = f"{self.config.base_url}/login"
        await self.page.goto(login_url)
        self.logger.info(f"Navigated to login page: {login_url}")
    
    async def wait_for_page_load(self) -> None:
        """Wait for login page to be fully loaded."""
        try:
            # Wait for space ID input to be visible (1단계 로그인 페이지)
            await self.page.wait_for_selector(
                self.selectors["space_id_input"],
                timeout=10000
            )
            self.logger.info("Login page loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load login page: {e}")
            raise
    
    async def fill_email(self, email: str) -> None:
        """Fill email input field."""
        try:
            email_input = await self.page.wait_for_selector(self.selectors["email_input"])
            await email_input.fill(email)
            self.logger.info(f"Filled email: {email}")
        except Exception as e:
            self.logger.error(f"Failed to fill email: {e}")
            raise
    
    async def fill_password(self, password: str) -> None:
        """Fill password input field."""
        try:
            password_input = await self.page.wait_for_selector(self.selectors["password_input"])
            await password_input.fill(password)
            self.logger.info("Password filled")
        except Exception as e:
            self.logger.error(f"Failed to fill password: {e}")
            raise
    
    async def toggle_remember_me(self) -> None:
        """Toggle remember me checkbox."""
        try:
            checkbox = await self.page.wait_for_selector(self.selectors["remember_me_checkbox"])
            await checkbox.click()
            self.logger.info("Remember me checkbox toggled")
        except Exception as e:
            self.logger.error(f"Failed to toggle remember me: {e}")
            raise
    
    async def login(self, space_id: str, email: str, password: str, remember_me: bool = False) -> None:
        """Perform complete 3-step login process."""
        try:
            # 1단계: 스페이스 ID 입력
            await self.fill_space_id(space_id)
            await self.click_next_button()
            
            # 2단계: 이메일 입력
            await self.fill_email(email)
            await self.click_email_login_button()
            
            # 3단계: 비밀번호 입력
            await self.fill_password(password)
            if remember_me:
                await self.toggle_remember_me()
            await self.click_final_login_button()
            
            self.logger.info(f"3-step login completed for: {email} in space: {space_id}")
        except Exception as e:
            self.logger.error(f"Login failed: {e}")
            raise
    
    async def fill_space_id(self, space_id: str) -> None:
        """Fill space ID input field."""
        try:
            space_id_input = await self.page.wait_for_selector(self.selectors["space_id_input"])
            await space_id_input.fill(space_id)
            self.logger.info(f"Filled space ID: {space_id}")
        except Exception as e:
            self.logger.error(f"Failed to fill space ID: {e}")
            raise
    
    async def click_next_button(self) -> None:
        """Click next button after space ID input."""
        try:
            next_button = await self.page.wait_for_selector(self.selectors["next_button"])
            await next_button.click()
            self.logger.info("Next button clicked")
        except Exception as e:
            self.logger.error(f"Failed to click next button: {e}")
            raise
    
    async def click_email_login_button(self) -> None:
        """Click login button after email input."""
        try:
            email_login_button = await self.page.wait_for_selector(self.selectors["email_login_button"])
            await email_login_button.click()
            self.logger.info("Email login button clicked")
        except Exception as e:
            self.logger.error(f"Failed to click email login button: {e}")
            raise
    
    async def click_final_login_button(self) -> None:
        """Click final login button after password input."""
        try:
            final_login_button = await self.page.wait_for_selector(self.selectors["final_login_button"])
            await final_login_button.click()
            self.logger.info("Final login button clicked")
        except Exception as e:
            self.logger.error(f"Failed to click final login button: {e}")
            raise
    
    async def is_error_message_visible(self) -> bool:
        """Check if error message is visible."""
        try:
            error_element = await self.page.query_selector(self.selectors["error_message"])
            return error_element is not None and await error_element.is_visible()
        except Exception:
            return False
    
    async def get_error_message(self) -> Optional[str]:
        """Get error message text if visible."""
        try:
            if await self.is_error_message_visible():
                error_element = await self.page.query_selector(self.selectors["error_message"])
                return await error_element.text_content()
            return None
        except Exception as e:
            self.logger.error(f"Failed to get error message: {e}")
            return None
    
    async def is_success_message_visible(self) -> bool:
        """Check if success message is visible."""
        try:
            success_element = await self.page.query_selector(self.selectors["success_message"])
            return success_element is not None and await success_element.is_visible()
        except Exception:
            return False
    
    async def click_forgot_password(self) -> None:
        """Click forgot password link."""
        try:
            forgot_link = await self.page.wait_for_selector(self.selectors["forgot_password_link"])
            await forgot_link.click()
            self.logger.info("Forgot password link clicked")
        except Exception as e:
            self.logger.error(f"Failed to click forgot password: {e}")
            raise
    
    async def toggle_remember_me(self) -> None:
        """Toggle remember me checkbox."""
        try:
            checkbox = await self.page.wait_for_selector(self.selectors["remember_me_checkbox"])
            await checkbox.click()
            self.logger.info("Remember me checkbox toggled")
        except Exception as e:
            self.logger.error(f"Failed to toggle remember me: {e}")
            raise
    
    async def is_logged_in(self) -> bool:
        """Check if user is successfully logged in."""
        try:
            # Wait for redirect or dashboard elements
            await self.page.wait_for_load_state("networkidle", timeout=5000)
            
            # Check if we're still on login page
            current_url = self.page.url
            if "/login" in current_url:
                return False
            
            # Check for Beamo app specific indicators
            # Based on actual analysis: URL should be like https://{space-id}.beamo.dev/list
            if "/list" in current_url or "/dashboard" in current_url:
                self.logger.info("Login successful - dashboard detected")
                return True
            
            # Check for dashboard or main app elements
            dashboard_indicators = [
                "dashboard",
                "main", 
                "app",
                "workspace",
                "projects",
                "sites",
                "settings"
            ]
            
            for indicator in dashboard_indicators:
                try:
                    await self.page.wait_for_selector(f"[data-testid*='{indicator}'], .{indicator}, #{indicator}", timeout=2000)
                    self.logger.info(f"Login successful - {indicator} detected")
                    return True
                except Exception:
                    continue
            
            # If we're not on login page and no specific dashboard element found
            return "/login" not in current_url
            
        except Exception as e:
            self.logger.error(f"Error checking login status: {e}")
            return False
    
    async def take_login_screenshot(self, test_name: str = "login_page", status: str = "unknown") -> str:
        """Take screenshot of login page with test name and status."""
        try:
            # Create reports directory if it doesn't exist
            from pathlib import Path
            from datetime import datetime
            screenshot_dir = Path(f"reports/{self.config.environment}/screenshots")
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate filename with test name, status, and timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{test_name}_{status}_{timestamp}.png"
            filepath = screenshot_dir / filename
            
            # Take screenshot
            await self.page.screenshot(path=str(filepath))
            self.logger.info(f"Screenshot saved: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {e}")
            return ""
