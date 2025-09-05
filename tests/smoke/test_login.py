"""
Smoke tests for Beamo login functionality.
Tests basic login flows across different environments.
"""

import pytest
import pytest_asyncio
import logging
import asyncio
from functools import wraps
from utils.config_loader import get_config
from utils.browser_manager import BrowserFactory
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

def timeout(seconds):
    """타임아웃 데코레이터"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=seconds)
            except asyncio.TimeoutError:
                print(f"⏰ 테스트 타임아웃 ({seconds}초 초과)")
                return False
        return wrapper
    return decorator


class TestLoginSmoke:
    """Smoke tests for login functionality."""
    
    @pytest.fixture(autouse=True)
    def setup_logging(self):
        """Setup logging for tests."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    @pytest_asyncio.fixture
    async def browser_manager(self, request):
        """Browser manager fixture."""
        # Get environment from pytest marker or default to dev
        env = getattr(request.node.get_closest_marker('env'), 'args', ['dev'])[0]
        config = get_config(env)
        
        browser_manager = await BrowserFactory.create_and_start(config)
        yield browser_manager
        await browser_manager.close_browser()
    
    @pytest.fixture
    def test_data(self, request):
        """Test data fixture."""
        env = getattr(request.node.get_closest_marker('env'), 'args', ['dev'])[0]
        config = get_config(env)
        return config.test_data
    
    @pytest.mark.asyncio
    @pytest.mark.smoke
    @pytest.mark.p0
    @pytest.mark.env('dev')
    @timeout(30)  # 30초 타임아웃
    async def test_valid_login_dev(self, browser_manager, test_data):
        """Test valid login on dev environment."""
        self.logger.info("Starting valid login test for dev environment")
        
        try:
            # Create login page
            login_page = LoginPage(browser_manager.page, browser_manager.config)
            
            # Navigate to login page
            await login_page.navigate_to_login()
            await login_page.wait_for_page_load()
            
            # Perform 3-step login
            await login_page.login(
                "d-ge-pr",  # 스페이스 ID
                test_data.valid_user["email"],
                test_data.valid_user["password"]
            )
            
            # Verify login success
            assert await login_page.is_logged_in(), "Login should be successful"
            
            # Create dashboard page and verify
            dashboard_page = DashboardPage(browser_manager.page, browser_manager.config)
            await dashboard_page.wait_for_dashboard_load()
            
            assert await dashboard_page.is_dashboard_visible(), "Dashboard should be visible"
            
            self.logger.info("Valid login test passed for dev environment")
            
        except Exception as e:
            self.logger.error(f"Valid login test failed: {e}")
            await login_page.take_login_screenshot("valid_login", "failure")
            raise
    
    @pytest.mark.asyncio
    @pytest.mark.smoke
    @pytest.mark.p1
    @pytest.mark.env('dev')
    @timeout(22)  # 22초 타임아웃
    async def test_login_page_elements_dev(self, browser_manager):
        """Test login page elements are present on dev environment."""
        self.logger.info("Starting login page elements test for dev environment")
        
        try:
            # Create login page
            login_page = LoginPage(browser_manager.page, browser_manager.config)
            
            # Navigate to login page
            await login_page.navigate_to_login()
            await login_page.wait_for_page_load()
            
            # Verify page title contains expected text
            page_title = await browser_manager.page.title()
            assert "login" in page_title.lower() or "beamo" in page_title.lower(), \
                f"Page title should contain login or beamo: {page_title}"
            
            # Verify current URL is login page
            current_url = browser_manager.page.url
            assert "/login" in current_url, f"URL should contain /login: {current_url}"
            
            self.logger.info("Login page elements test passed for dev environment")
            
        except Exception as e:
            self.logger.error(f"Login page elements test failed: {e}")
            await login_page.take_login_screenshot("login_elements", "failure")
            raise
