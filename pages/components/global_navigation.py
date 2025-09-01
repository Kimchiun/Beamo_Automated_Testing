#!/usr/bin/env python3
"""
Global Navigation Component
Handles the global navigation bar that appears on all pages
"""

import logging
from typing import Optional, List, Dict
from utils.config_loader import EnvironmentConfig


class GlobalNavigation:
    """Global Navigation Component for Beamo"""
    
    def __init__(self, page, config: EnvironmentConfig):
        self.page = page
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Global Navigation selectors
        self.selectors = {
            # 글로벌 네비게이션 컨테이너
            "global_nav": ".main-header, .el-header, .global-navigation",
            "nav_left": ".header-left, .nav-left",
            "nav_right": ".header-right, .nav-right",
            
            # 사용자 관련
            "user_team_dropdown": ".user-team-dropdown",
            "user_profile": ".user-profile, .profile-menu",
            "user_avatar": ".user-avatar, .avatar",
            "user_name": ".user-name, .username",
            
            # 알림 관련
            "notifications": ".js-notifications-trigger, .notifications",
            "iot_alerts": ".js-alerts-trigger, .alerts",
            "notification_badge": ".notification-badge, .badge",
            "alert_badge": ".alert-badge, .badge",
            
            # 브랜딩/로고
            "logo": ".logo, .brand-logo",
            "brand_name": ".brand-name, .company-name",
            
            # 네비게이션 메뉴
            "nav_menu": ".nav-menu, .navigation-menu",
            "nav_items": ".nav-item, .menu-item",
            "nav_links": ".nav-link, .menu-link",
            
            # 검색 (글로벌)
            "global_search": ".global-search, .search-box",
            "search_input": ".search-input, input[type='search']",
            "search_button": ".search-button, .search-btn",
            
            # 설정/도움말
            "settings_menu": ".settings-menu, .config-menu",
            "help_menu": ".help-menu, .support-menu",
            "language_selector": ".language-selector, .lang-selector",
            
            # 모바일 메뉴
            "mobile_menu_button": ".mobile-menu-btn, .hamburger",
            "mobile_menu": ".mobile-menu, .mobile-nav",
        }
    
    async def is_visible(self) -> bool:
        """Check if global navigation is visible."""
        try:
            nav = await self.page.query_selector(self.selectors["global_nav"])
            return nav is not None and await nav.is_visible()
        except Exception:
            return False
    
    async def wait_for_navigation_load(self, timeout: int = 10000) -> None:
        """Wait for global navigation to load."""
        try:
            await self.page.wait_for_selector(self.selectors["global_nav"], timeout=timeout)
            self.logger.info("Global navigation loaded")
        except Exception as e:
            self.logger.error(f"Failed to load global navigation: {e}")
            raise
    
    async def get_user_info(self) -> Dict:
        """Get current user information from navigation."""
        try:
            user_info = {}
            
            # 사용자 이름
            user_name_elem = await self.page.query_selector(self.selectors["user_name"])
            if user_name_elem:
                user_info["name"] = await user_name_elem.text_content()
            
            # 사용자 팀
            team_elem = await self.page.query_selector(self.selectors["user_team_dropdown"])
            if team_elem:
                user_info["team"] = await team_elem.text_content()
            
            return user_info
        except Exception as e:
            self.logger.error(f"Failed to get user info: {e}")
            return {}
    
    async def click_user_team_dropdown(self) -> None:
        """Click user team dropdown."""
        try:
            dropdown = await self.page.wait_for_selector(self.selectors["user_team_dropdown"])
            await dropdown.click()
            self.logger.info("Clicked user team dropdown")
        except Exception as e:
            self.logger.error(f"Failed to click user team dropdown: {e}")
            raise
    
    async def select_team(self, team_name: str) -> None:
        """Select a specific team from dropdown."""
        try:
            await self.click_user_team_dropdown()
            
            # 팀 선택
            team_selector = f"{self.selectors['nav_items']}:has-text('{team_name}')"
            team_item = await self.page.wait_for_selector(team_selector, timeout=5000)
            await team_item.click()
            
            self.logger.info(f"Selected team: {team_name}")
        except Exception as e:
            self.logger.error(f"Failed to select team {team_name}: {e}")
            raise
    
    async def click_notifications(self) -> None:
        """Click notifications button."""
        try:
            notifications = await self.page.wait_for_selector(self.selectors["notifications"])
            await notifications.click()
            self.logger.info("Clicked notifications")
        except Exception as e:
            self.logger.error(f"Failed to click notifications: {e}")
            raise
    
    async def click_iot_alerts(self) -> None:
        """Click IoT alerts button."""
        try:
            alerts = await self.page.wait_for_selector(self.selectors["iot_alerts"])
            await alerts.click()
            self.logger.info("Clicked IoT alerts")
        except Exception as e:
            self.logger.error(f"Failed to click IoT alerts: {e}")
            raise
    
    async def get_notification_count(self) -> int:
        """Get notification count from badge."""
        try:
            badge = await self.page.query_selector(self.selectors["notification_badge"])
            if badge:
                count_text = await badge.text_content()
                return int(count_text) if count_text.isdigit() else 0
            return 0
        except Exception as e:
            self.logger.error(f"Failed to get notification count: {e}")
            return 0
    
    async def get_alert_count(self) -> int:
        """Get alert count from badge."""
        try:
            badge = await self.page.query_selector(self.selectors["alert_badge"])
            if badge:
                count_text = await badge.text_content()
                return int(count_text) if count_text.isdigit() else 0
            return 0
        except Exception as e:
            self.logger.error(f"Failed to get alert count: {e}")
            return 0
    
    async def click_logo(self) -> None:
        """Click logo to go to home/dashboard."""
        try:
            logo = await self.page.wait_for_selector(self.selectors["logo"])
            await logo.click()
            self.logger.info("Clicked logo")
        except Exception as e:
            self.logger.error(f"Failed to click logo: {e}")
            raise
    
    async def search_globally(self, query: str) -> None:
        """Perform global search."""
        try:
            # 검색 입력
            search_input = await self.page.wait_for_selector(self.selectors["search_input"])
            await search_input.fill(query)
            
            # 검색 버튼 클릭 또는 Enter 키
            search_button = await self.page.query_selector(self.selectors["search_button"])
            if search_button:
                await search_button.click()
            else:
                await self.page.keyboard.press("Enter")
            
            self.logger.info(f"Performed global search: {query}")
        except Exception as e:
            self.logger.error(f"Failed to perform global search: {e}")
            raise
    
    async def click_settings(self) -> None:
        """Click settings menu."""
        try:
            settings = await self.page.wait_for_selector(self.selectors["settings_menu"])
            await settings.click()
            self.logger.info("Clicked settings menu")
        except Exception as e:
            self.logger.error(f"Failed to click settings: {e}")
            raise
    
    async def click_help(self) -> None:
        """Click help menu."""
        try:
            help_menu = await self.page.wait_for_selector(self.selectors["help_menu"])
            await help_menu.click()
            self.logger.info("Clicked help menu")
        except Exception as e:
            self.logger.error(f"Failed to click help: {e}")
            raise
    
    async def change_language(self, language: str) -> None:
        """Change language setting."""
        try:
            # 언어 선택기 클릭
            lang_selector = await self.page.wait_for_selector(self.selectors["language_selector"])
            await lang_selector.click()
            
            # 언어 선택
            lang_option = f"{self.selectors['nav_items']}:has-text('{language}')"
            option = await self.page.wait_for_selector(lang_option, timeout=5000)
            await option.click()
            
            self.logger.info(f"Changed language to: {language}")
        except Exception as e:
            self.logger.error(f"Failed to change language: {e}")
            raise
    
    async def toggle_mobile_menu(self) -> None:
        """Toggle mobile menu (for responsive design)."""
        try:
            mobile_button = await self.page.wait_for_selector(self.selectors["mobile_menu_button"])
            await mobile_button.click()
            self.logger.info("Toggled mobile menu")
        except Exception as e:
            self.logger.error(f"Failed to toggle mobile menu: {e}")
            raise
    
    async def get_navigation_items(self) -> List[Dict]:
        """Get all navigation menu items."""
        try:
            nav_items = await self.page.query_selector_all(self.selectors["nav_items"])
            items = []
            
            for item in nav_items:
                try:
                    text = await item.text_content()
                    href = await item.get_attribute("href")
                    visible = await item.is_visible()
                    
                    items.append({
                        "text": text.strip() if text else "",
                        "href": href,
                        "visible": visible
                    })
                except Exception:
                    continue
            
            return items
        except Exception as e:
            self.logger.error(f"Failed to get navigation items: {e}")
            return []
    
    async def click_navigation_item(self, item_text: str) -> None:
        """Click a specific navigation item."""
        try:
            item_selector = f"{self.selectors['nav_items']}:has-text('{item_text}')"
            item = await self.page.wait_for_selector(item_selector, timeout=5000)
            await item.click()
            self.logger.info(f"Clicked navigation item: {item_text}")
        except Exception as e:
            self.logger.error(f"Failed to click navigation item {item_text}: {e}")
            raise
