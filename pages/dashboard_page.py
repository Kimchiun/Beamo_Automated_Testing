"""
Dashboard page object model for Beamo portal.
Handles dashboard functionality and navigation.
"""

import asyncio
import logging
from typing import Optional, List
from playwright.async_api import Page
from utils.config_loader import EnvironmentConfig


class DashboardPage:
    """Page Object Model for Beamo dashboard page."""
    
    def __init__(self, page: Page, config: EnvironmentConfig):
        self.page = page
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Common selectors (based on actual Beamo dashboard structure)
        self.selectors = {
            # 헤더 영역
            "dashboard_container": ".el-container.views-container, .el-main",
            "main_header": ".main-header, .el-header",
            "header_left": ".header-left",
            "header_right": ".header-right",
            "user_team_dropdown": ".user-team-dropdown",
            
            # 알림 시스템
            "notifications": ".js-notifications-trigger",
            "iot_alerts": ".js-alerts-trigger",
            
            # 메인 콘텐츠
            "main_content": ".el-main, .control-panel__content",
            "control_panel": ".control-panel__content",
            
            # 정렬 및 필터
            "sort_filter_header": ".sort-filter-header",
            "sort_select": ".sort-select",
            "filter_drawer": ".filter-drawer",
            "filter_drawer_header": ".filter-drawer-header",
            
            # 검색 및 입력
            "search_input": "input[placeholder='Search']",
            "select_input": "input[placeholder='Select']",
            
            # 버튼들
            "reset_button": "button:has-text('Reset')",
            "refine_search_button": ".sort-filter-header button, [class*='filter'] button",
            "create_site_button": ".create-site, .create-site-button",
            
            # 사이트 관련
            "sites_empty_state": "#icon-home_sites_empty",
            "sites_list": ".sites-list, .list-container",
            "building_address": ".building-address",
            "building_last_updated": ".building-last-updated",
            "bookmark_icon": ".bookmark-icon",
            "create_site_button": ".create-site-button, .create-site",
            "site_create_dialog": ".site-create-dialog",
            
            # Create Site 다이얼로그
            "site_name_input": "input[placeholder='Enter a Name']",
            "site_address_input": "input[placeholder='Enter an Address']",
            "site_latitude_input": "input[placeholder='Latitude']",
            "site_longitude_input": "input[placeholder='Longitude']",
            "site_thumbnail_upload": "input[type='file']",
            "create_site_submit_button": ".site-create-dialog .el-button--primary",
            "create_site_cancel_button": ".site-create-dialog .el-button--default",
            
                    # 검색 기능
        "search_input": "input[placeholder='검색'], input[placeholder*='search'], input[placeholder*='Search'], .search-input, [data-testid='search-input']",
        "search_button": ".search-button, button[aria-label*='search'], button[aria-label*='Search']",
        "search_results": ".search-results, .site-list, .site-item",
        "search_result_item": ".building, .el-card, .site-item, .list-item, [data-testid='site-item'], .card, .item, li, .site",
        "building_name": ".building-name",
        }
    
    async def wait_for_dashboard_load(self) -> None:
        """Wait for dashboard to be fully loaded."""
        try:
            # Wait for main header or main content to be visible
            await self.page.wait_for_selector(
                f"{self.selectors['main_header']}, {self.selectors['main_content']}",
                timeout=10000
            )
            self.logger.info("Dashboard loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load dashboard: {e}")
            raise
    
    async def is_dashboard_visible(self) -> bool:
        """Check if dashboard is visible."""
        try:
            # Check for main header or main content
            header_element = await self.page.query_selector(self.selectors["main_header"])
            content_element = await self.page.query_selector(self.selectors["main_content"])
            
            return (header_element is not None and await header_element.is_visible()) or \
                   (content_element is not None and await content_element.is_visible())
        except Exception:
            return False
    
    async def get_current_url(self) -> str:
        """Get current page URL."""
        return self.page.url
    
    async def get_page_title(self) -> str:
        """Get page title."""
        return await self.page.title()
    
    async def click_user_team_dropdown(self) -> None:
        """Click user team dropdown."""
        try:
            dropdown = await self.page.wait_for_selector(self.selectors["user_team_dropdown"])
            await dropdown.click()
            self.logger.info("User team dropdown clicked")
        except Exception as e:
            self.logger.error(f"Failed to click user team dropdown: {e}")
            raise
    
    async def click_notifications(self) -> None:
        """Click notifications button."""
        try:
            notifications = await self.page.wait_for_selector(self.selectors["notifications"])
            await notifications.click()
            self.logger.info("Notifications button clicked")
        except Exception as e:
            self.logger.error(f"Failed to click notifications: {e}")
            raise
    
    async def click_iot_alerts(self) -> None:
        """Click IoT alerts button."""
        try:
            alerts = await self.page.wait_for_selector(self.selectors["iot_alerts"])
            await alerts.click()
            self.logger.info("IoT alerts button clicked")
        except Exception as e:
            self.logger.error(f"Failed to click IoT alerts: {e}")
            raise
    

    
    async def open_filter_drawer(self) -> None:
        """Open filter drawer."""
        try:
            filter_button = await self.page.wait_for_selector(self.selectors["refine_search_button"])
            await filter_button.click()
            self.logger.info("Filter drawer opened")
        except Exception as e:
            self.logger.error(f"Failed to open filter drawer: {e}")
            raise
    
    async def reset_filters(self) -> None:
        """Reset all filters."""
        try:
            reset_button = await self.page.wait_for_selector(self.selectors["reset_button"])
            await reset_button.click()
            self.logger.info("Filters reset")
        except Exception as e:
            self.logger.error(f"Failed to reset filters: {e}")
            raise
    
    async def create_new_site(self) -> None:
        """Click create new site button."""
        try:
            create_button = await self.page.wait_for_selector(self.selectors["create_site_button"])
            await create_button.click()
            self.logger.info("Create new site button clicked")
        except Exception as e:
            self.logger.error(f"Failed to create new site: {e}")
            raise
    
    async def is_sites_empty(self) -> bool:
        """Check if sites list is empty."""
        try:
            empty_state = await self.page.query_selector(self.selectors["sites_empty_state"])
            return empty_state is not None and await empty_state.is_visible()
        except Exception:
            return False
    
    async def get_sort_options(self) -> list:
        """Get available sort options."""
        try:
            sort_options = await self.page.query_selector_all(".sort-option")
            options = []
            for option in sort_options:
                text = await option.text_content()
                if text:
                    options.append(text.strip())
            return options
        except Exception as e:
            self.logger.error(f"Failed to get sort options: {e}")
            return []
    
    async def select_sort_option(self, option_text: str) -> None:
        """Select a sort option."""
        try:
            # Click sort select to open dropdown
            sort_select = await self.page.wait_for_selector(self.selectors["sort_select"])
            await sort_select.click()
            
            # Select the option
            option = await self.page.wait_for_selector(f".sort-option:has-text('{option_text}')")
            await option.click()
            self.logger.info(f"Selected sort option: {option_text}")
        except Exception as e:
            self.logger.error(f"Failed to select sort option: {e}")
            raise
    
    async def get_site_addresses(self) -> list:
        """Get all site addresses."""
        try:
            address_elements = await self.page.query_selector_all(self.selectors["building_address"])
            addresses = []
            for element in address_elements:
                text = await element.text_content()
                if text:
                    addresses.append(text.strip())
            return addresses
        except Exception as e:
            self.logger.error(f"Failed to get site addresses: {e}")
            return []
    
    async def get_site_survey_dates(self) -> list:
        """Get all site survey dates."""
        try:
            date_elements = await self.page.query_selector_all(self.selectors["building_last_updated"])
            dates = []
            for element in date_elements:
                text = await element.text_content()
                if text:
                    dates.append(text.strip())
            return dates
        except Exception as e:
            self.logger.error(f"Failed to get site survey dates: {e}")
            return []
    
    async def click_bookmark(self, site_index: int = 0) -> None:
        """Click bookmark icon for a specific site."""
        try:
            bookmark_icons = await self.page.query_selector_all(self.selectors["bookmark_icon"])
            if site_index < len(bookmark_icons):
                await bookmark_icons[site_index].click()
                self.logger.info(f"Clicked bookmark for site {site_index}")
            else:
                raise ValueError(f"Site index {site_index} out of range")
        except Exception as e:
            self.logger.error(f"Failed to click bookmark: {e}")
            raise
    
    async def open_create_site_dialog(self) -> None:
        """Open create site dialog."""
        try:
            # Check if dialog is already open
            if await self.is_create_site_dialog_open():
                self.logger.info("Create site dialog is already open")
                return
            
            # Find and click create button
            create_button = await self.page.wait_for_selector(self.selectors["create_site_button"])
            await create_button.click()
            
            # Wait for dialog to open
            await self.page.wait_for_selector(self.selectors["site_create_dialog"], timeout=10000)
            self.logger.info("Create site dialog opened")
        except Exception as e:
            self.logger.error(f"Failed to open create site dialog: {e}")
            raise
    
    async def is_create_site_dialog_open(self) -> bool:
        """Check if create site dialog is open."""
        try:
            dialog = await self.page.query_selector(self.selectors["site_create_dialog"])
            return dialog is not None and await dialog.is_visible()
        except Exception:
            return False
    
    async def fill_site_name(self, site_name: str) -> None:
        """Fill site name input field."""
        try:
            name_input = await self.page.wait_for_selector(self.selectors["site_name_input"])
            await name_input.fill(site_name)
            self.logger.info(f"Filled site name: {site_name}")
        except Exception as e:
            self.logger.error(f"Failed to fill site name: {e}")
            raise
    
    async def fill_site_address(self, address: str) -> None:
        """Fill site address input field."""
        try:
            address_input = await self.page.wait_for_selector(self.selectors["site_address_input"])
            await address_input.fill(address)
            self.logger.info(f"Filled site address: {address}")
        except Exception as e:
            self.logger.error(f"Failed to fill site address: {e}")
            raise
    
    async def fill_site_coordinates(self, latitude: str, longitude: str) -> None:
        """Fill site coordinates input fields."""
        try:
            lat_input = await self.page.wait_for_selector(self.selectors["site_latitude_input"])
            lon_input = await self.page.wait_for_selector(self.selectors["site_longitude_input"])
            
            await lat_input.fill(latitude)
            await lon_input.fill(longitude)
            
            self.logger.info(f"Filled coordinates: lat={latitude}, lon={longitude}")
        except Exception as e:
            self.logger.error(f"Failed to fill coordinates: {e}")
            raise
    
    async def upload_site_thumbnail(self, file_path: str) -> None:
        """Upload site thumbnail image."""
        try:
            file_input = await self.page.wait_for_selector(self.selectors["site_thumbnail_upload"])
            await file_input.set_input_files(file_path)
            self.logger.info(f"Uploaded thumbnail: {file_path}")
        except Exception as e:
            self.logger.error(f"Failed to upload thumbnail: {e}")
            raise
    
    async def submit_create_site(self) -> None:
        """Submit create site form."""
        try:
            submit_button = await self.page.wait_for_selector(self.selectors["create_site_submit_button"])
            await submit_button.click()
            self.logger.info("Submitted create site form")
        except Exception as e:
            self.logger.error(f"Failed to submit create site form: {e}")
            raise
    
    async def cancel_create_site(self) -> None:
        """Cancel create site dialog."""
        try:
            cancel_button = await self.page.wait_for_selector(self.selectors["create_site_cancel_button"])
            await cancel_button.click()
            self.logger.info("Cancelled create site dialog")
        except Exception as e:
            self.logger.error(f"Failed to cancel create site dialog: {e}")
            raise
    
    async def create_site(self, site_name: str, address: str, latitude: str = "", longitude: str = "", thumbnail_path: str = "") -> bool:
        """Create a new site with all required information."""
        try:
            # Open create site dialog
            await self.open_create_site_dialog()
            
            # Wait for dialog to be open
            await self.page.wait_for_selector(self.selectors["site_create_dialog"], timeout=10000)
            
            # Fill site name (required)
            await self.fill_site_name(site_name)
            
            # Fill address (required)
            await self.fill_site_address(address)
            
            # Fill coordinates if provided
            if latitude and longitude:
                await self.fill_site_coordinates(latitude, longitude)
            
            # Upload thumbnail if provided
            if thumbnail_path:
                await self.upload_site_thumbnail(thumbnail_path)
            
            # Submit the form
            await self.submit_create_site()
            
            # Wait for dialog to close (success) or error message
            try:
                await self.page.wait_for_selector(self.selectors["site_create_dialog"], state="hidden", timeout=10000)
                self.logger.info(f"Site created successfully: {site_name}")
                
                # Wait a bit for the page to update
                await asyncio.sleep(2)
                
                # Refresh the page to see the new site
                await self.page.reload()
                await self.page.wait_for_load_state("networkidle", timeout=10000)
                
                return True
            except Exception:
                # Check if there's an error message
                error_element = await self.page.query_selector(".el-message--error, .error-message")
                if error_element:
                    error_text = await error_element.text_content()
                    self.logger.error(f"Site creation failed: {error_text}")
                    return False
                else:
                    self.logger.info(f"Site created successfully: {site_name}")
                    
                    # Refresh the page to see the new site
                    await self.page.reload()
                    await self.page.wait_for_load_state("networkidle", timeout=10000)
                    
                    return True
                    
        except Exception as e:
            self.logger.error(f"Failed to create site: {e}")
            return False
    
    # 검색 기능 관련 메서드들
    async def search_sites(self, search_term: str) -> None:
        """Search for sites using the search input."""
        try:
            # JavaScript를 사용해서 검색 실행
            await self.page.evaluate(f"""
                (searchTerm) => {{
                    // 검색 입력 필드 찾기
                    const searchInput = document.querySelector('input[placeholder="검색"], input[placeholder*="search"], input[placeholder*="Search"]');
                    if (searchInput) {{
                        // disabled 속성 제거
                        searchInput.removeAttribute('disabled');
                        // 검색어 입력
                        searchInput.value = searchTerm;
                        // input 이벤트 발생
                        searchInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        // Enter 키 이벤트 발생
                        searchInput.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }}));
                        searchInput.dispatchEvent(new KeyboardEvent('keypress', {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }}));
                        searchInput.dispatchEvent(new KeyboardEvent('keyup', {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }}));
                    }}
                }}
            """, search_term)
            
            # 검색 실행 후 잠시 대기
            await asyncio.sleep(2)
            
            self.logger.info(f"Searched for sites with term: {search_term}")
        except Exception as e:
            self.logger.error(f"Failed to search sites: {e}")
            raise
    
    async def clear_search(self) -> None:
        """Clear the search input."""
        try:
            search_input = await self.page.wait_for_selector(self.selectors["search_input"])
            await search_input.clear()
            await search_input.press("Enter")
            self.logger.info("Search cleared")
        except Exception as e:
            self.logger.error(f"Failed to clear search: {e}")
            raise
    
    async def get_search_results_count(self) -> int:
        """Get the number of search results."""
        try:
            results = await self.page.query_selector_all(self.selectors["search_result_item"])
            return len(results)
        except Exception as e:
            self.logger.error(f"Failed to get search results count: {e}")
            return 0
    
    async def click_search_result_by_index(self, index: int) -> None:
        """Click on a search result by index."""
        try:
            # 직접 .building 요소를 찾아서 클릭 (가장 안정적)
            results = await self.page.query_selector_all(".building")
            if index < len(results):
                await results[index].click()
                self.logger.info(f"Clicked search result at index: {index} (direct .building click)")
            else:
                raise ValueError(f"Search result index {index} out of range")
        except Exception as e:
            self.logger.error(f"Failed to click search result: {e}")
            raise
    
    async def click_search_result_by_name(self, site_name: str) -> bool:
        """Click on a search result by site name."""
        try:
            results = await self.page.query_selector_all(self.selectors["search_result_item"])
            
            for i, result in enumerate(results):
                try:
                    text = await result.text_content()
                    if site_name.lower() in text.lower():
                        await result.click()
                        self.logger.info(f"Clicked search result with name: {site_name}")
                        return True
                except Exception:
                    continue
            
            self.logger.warning(f"Site with name '{site_name}' not found in search results")
            return False
        except Exception as e:
            self.logger.error(f"Failed to click search result by name: {e}")
            return False
    
    async def search_and_click_site(self, site_name: str) -> bool:
        """Search for a site and click on it (no hard sleep)."""
        try:
            # 검색 실행
            await self.search_sites(site_name)
            # 검색 결과가 나타날 때까지 대기
            try:
                await self.page.wait_for_selector(
                    f"{self.selectors['search_result_item']}, .building",
                    timeout=10000
                )
            except Exception:
                self.logger.warning("Search results not visible within timeout")
            
            # 검색 결과에서 사이트 클릭
            success = await self.click_search_result_by_name(site_name)
            
            if success:
                # 사이트 상세 화면의 핵심 요소가 나타날 때까지 대기
                await self.page.wait_for_load_state("networkidle", timeout=15000)
                await self.page.wait_for_selector(
                    ".site-profile, .site-name, .site-title, .control-panel__content, .viewer-controls",
                    timeout=15000
                )
                return True
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to search and click site: {e}")
            return False
    
    async def get_sites_count(self) -> int:
        """Get the number of sites in the list."""
        try:
            addresses = await self.get_site_addresses()
            return len(addresses)
        except Exception as e:
            self.logger.error(f"Failed to get sites count: {e}")
            return 0
    
    async def click_site_by_index(self, index: int) -> None:
        """Click on a site by its index in the list."""
        try:
            addresses = await self.page.query_selector_all(self.selectors["building_address"])
            if index < len(addresses):
                await addresses[index].click()
                self.logger.info(f"Clicked site at index {index}")
            else:
                raise ValueError(f"Site index {index} out of range")
        except Exception as e:
            self.logger.error(f"Failed to click site: {e}")
            raise
    
    async def click_site_in_list_by_index(self, index: int) -> None:
        """Click on a site in the site list by index."""
        try:
            sites = await self.page.query_selector_all(".building")
            if index < len(sites):
                await sites[index].click()
                self.logger.info(f"Clicked site in list at index: {index}")
            else:
                raise ValueError(f"Site index {index} out of range")
        except Exception as e:
            self.logger.error(f"Failed to click site in list: {e}")
            raise
    
    async def click_first_available_site(self) -> bool:
        """강력한 사이트 클릭 메서드 - 여러 방법을 시도합니다."""
        try:
            self.logger.info("🔍 첫 번째 사이트 클릭 시도 시작...")
            
            # 방법 1: .building 셀렉터로 시도
            try:
                buildings = await self.page.query_selector_all(".building")
                if buildings and len(buildings) > 0:
                    await buildings[0].click()
                    self.logger.info("✅ .building 셀렉터로 사이트 클릭 성공")
                    await self.page.wait_for_load_state("networkidle", timeout=15000)
                    await self.page.wait_for_selector(
                        ".site-profile, .site-name, .site-title, .control-panel__content, .viewer-controls",
                        timeout=15000
                    )
                    return True
            except Exception as e:
                self.logger.warning(f"⚠️ .building 방법 실패: {e}")
            
            # 방법 2: .building-address 셀렉터로 시도
            try:
                addresses = await self.page.query_selector_all(".building-address")
                if addresses and len(addresses) > 0:
                    await addresses[0].click()
                    self.logger.info("✅ .building-address 셀렉터로 사이트 클릭 성공")
                    await self.page.wait_for_load_state("networkidle", timeout=15000)
                    await self.page.wait_for_selector(
                        ".site-profile, .site-name, .site-title, .control-panel__content, .viewer-controls",
                        timeout=15000
                    )
                    return True
            except Exception as e:
                self.logger.warning(f"⚠️ .building-address 방법 실패: {e}")
            
            # 방법 3: .el-card 셀렉터로 시도
            try:
                cards = await self.page.query_selector_all(".el-card")
                if cards and len(cards) > 0:
                    await cards[0].click()
                    self.logger.info("✅ .el-card 셀렉터로 사이트 클릭 성공")
                    await self.page.wait_for_load_state("networkidle", timeout=15000)
                    await self.page.wait_for_selector(
                        ".site-profile, .site-name, .site-title, .control-panel__content, .viewer-controls",
                        timeout=15000
                    )
                    return True
            except Exception as e:
                self.logger.warning(f"⚠️ .el-card 방법 실패: {e}")
            
            # 방법 4: .site-item 셀렉터로 시도
            try:
                site_items = await self.page.query_selector_all(".site-item")
                if site_items and len(site_items) > 0:
                    await site_items[0].click()
                    self.logger.info("✅ .site-item 셀렉터로 사이트 클릭 성공")
                    await self.page.wait_for_load_state("networkidle", timeout=15000)
                    await self.page.wait_for_selector(
                        ".site-profile, .site-name, .site-title, .control-panel__content, .viewer-controls",
                        timeout=15000
                    )
                    return True
            except Exception as e:
                self.logger.warning(f"⚠️ .site-item 방법 실패: {e}")
            
            # 방법 5: .list-item 셀렉터로 시도
            try:
                list_items = await self.page.query_selector_all(".list-item")
                if list_items and len(list_items) > 0:
                    await list_items[0].click()
                    self.logger.info("✅ .list-item 셀렉터로 사이트 클릭 성공")
                    await self.page.wait_for_load_state("networkidle", timeout=15000)
                    await self.page.wait_for_selector(
                        ".site-profile, .site-name, .site-title, .control-panel__content, .viewer-controls",
                        timeout=15000
                    )
                    return True
            except Exception as e:
                self.logger.warning(f"⚠️ .list-item 방법 실패: {e}")
            
            # 방법 6: JavaScript로 클릭 가능한 요소 찾기
            try:
                clickable_elements = await self.page.evaluate("""
                    () => {
                        const selectors = [
                            '.building',
                            '.building-address', 
                            '.el-card',
                            '.site-item',
                            '.list-item',
                            '[data-testid*="site"]',
                            '.card',
                            '.item'
                        ];
                        
                        for (const selector of selectors) {
                            const elements = document.querySelectorAll(selector);
                            if (elements.length > 0) {
                                return {
                                    selector: selector,
                                    count: elements.length,
                                    firstElement: elements[0].tagName + (elements[0].className ? '.' + elements[0].className.split(' ').join('.') : '')
                                };
                            }
                        }
                        return null;
                    }
                """)
                
                if clickable_elements:
                    self.logger.info(f"🔍 JavaScript로 찾은 요소: {clickable_elements}")
                    # JavaScript로 직접 클릭
                    await self.page.evaluate(f"""
                        () => {{
                            const elements = document.querySelectorAll('{clickable_elements['selector']}');
                            if (elements.length > 0) {{
                                elements[0].click();
                                return true;
                            }}
                            return false;
                        }}
                    """)
                    self.logger.info(f"✅ JavaScript로 {clickable_elements['selector']} 클릭 성공")
                    await self.page.wait_for_load_state("networkidle", timeout=15000)
                    await self.page.wait_for_selector(
                        ".site-profile, .site-name, .site-title, .control-panel__content, .viewer-controls",
                        timeout=15000
                    )
                    return True
                    
            except Exception as e:
                self.logger.warning(f"⚠️ JavaScript 방법 실패: {e}")
            
            # 방법 7: 페이지 새로고침 후 재시도
            try:
                self.logger.info("🔄 페이지 새로고침 후 재시도...")
                await self.page.reload()
                await self.page.wait_for_load_state("networkidle", timeout=10000)
                
                # 새로고침 후 다시 .building 시도
                buildings = await self.page.query_selector_all(".building")
                if buildings and len(buildings) > 0:
                    await buildings[0].click()
                    self.logger.info("✅ 새로고침 후 .building 셀렉터로 사이트 클릭 성공")
                    await self.page.wait_for_load_state("networkidle", timeout=15000)
                    await self.page.wait_for_selector(
                        ".site-profile, .site-name, .site-title, .control-panel__content, .viewer-controls",
                        timeout=15000
                    )
                    return True
                    
            except Exception as e:
                self.logger.warning(f"⚠️ 새로고침 후 재시도 실패: {e}")
            
            self.logger.error("❌ 모든 사이트 클릭 방법 실패")
            return False
            
        except Exception as e:
            self.logger.error(f"❌ click_first_available_site 실패: {e}")
            return False
    
    async def get_site_info_by_index(self, index: int) -> dict:
        """Get site information by index."""
        try:
            addresses = await self.page.query_selector_all(self.selectors["building_address"])
            dates = await self.page.query_selector_all(self.selectors["building_last_updated"])
            names = await self.page.query_selector_all(self.selectors["building_name"])
            
            if index < len(addresses):
                address_text = await addresses[index].text_content()
                date_text = await dates[index].text_content() if index < len(dates) else ""
                name_text = await names[index].text_content() if index < len(names) else ""
                
                return {
                    "name": name_text.strip() if name_text else "",
                    "address": address_text.strip() if address_text else "",
                    "survey_date": date_text.strip() if date_text else "",
                    "index": index
                }
            else:
                raise ValueError(f"Site index {index} out of range")
        except Exception as e:
            self.logger.error(f"Failed to get site info: {e}")
            return {}
    
    async def get_site_name_by_index(self, index: int) -> str:
        """Get site name by index."""
        try:
            names = await self.page.query_selector_all(self.selectors["building_name"])
            
            if index < len(names):
                name_text = await names[index].text_content()
                return name_text.strip() if name_text else ""
            else:
                raise ValueError(f"Site index {index} out of range")
        except Exception as e:
            self.logger.error(f"Failed to get site name: {e}")
            return ""
    
    async def take_dashboard_screenshot(self, name: str = "dashboard") -> str:
        """Take screenshot of dashboard page."""
        try:
            # Create reports directory if it doesn't exist
            import os
            screenshot_dir = f"reports/{self.config.environment}/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            
            # Generate screenshot filename
            import time
            timestamp = int(time.time())
            filename = f"{name}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)
            
            # Take screenshot
            await self.page.screenshot(path=filepath)
            self.logger.info(f"Screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {e}")
            return ""
    
    async def click_user_profile(self) -> None:
        """Click user profile menu."""
        try:
            profile_element = await self.page.wait_for_selector(self.selectors["user_profile"])
            await profile_element.click()
            self.logger.info("User profile menu clicked")
        except Exception as e:
            self.logger.error(f"Failed to click user profile: {e}")
            raise
    
    async def logout(self) -> None:
        """Perform logout action."""
        try:
            # First click user profile if needed
            await self.click_user_profile()
            
            # Then click logout
            logout_button = await self.page.wait_for_selector(self.selectors["logout_button"])
            await logout_button.click()
            self.logger.info("Logout button clicked")
            
            # Wait for redirect to login page
            await self.page.wait_for_load_state("networkidle", timeout=5000)
            
        except Exception as e:
            self.logger.error(f"Failed to logout: {e}")
            raise
    
    async def navigate_to_sites(self) -> None:
        """Navigate to sites list page."""
        try:
            sites_link = await self.page.wait_for_selector(self.selectors["site_list_link"])
            await sites_link.click()
            self.logger.info("Navigated to sites page")
        except Exception as e:
            self.logger.error(f"Failed to navigate to sites: {e}")
            raise
    
    async def navigate_to_projects(self) -> None:
        """Navigate to projects page."""
        try:
            projects_link = await self.page.wait_for_selector(self.selectors["projects_link"])
            await projects_link.click()
            self.logger.info("Navigated to projects page")
        except Exception as e:
            self.logger.error(f"Failed to navigate to projects: {e}")
            raise
    
    async def navigate_to_settings(self) -> None:
        """Navigate to settings page."""
        try:
            settings_link = await self.page.wait_for_selector(self.selectors["settings_link"])
            await settings_link.click()
            self.logger.info("Navigated to settings page")
        except Exception as e:
            self.logger.error(f"Failed to navigate to settings: {e}")
            raise
    
    async def search(self, query: str) -> None:
        """Perform search action."""
        try:
            search_input = await self.page.wait_for_selector(self.selectors["search_input"])
            await search_input.fill(query)
            await search_input.press("Enter")
            self.logger.info(f"Search performed: {query}")
        except Exception as e:
            self.logger.error(f"Failed to perform search: {e}")
            raise
    
    async def get_notifications(self) -> List[str]:
        """Get list of notification messages."""
        try:
            notification_elements = await self.page.query_selector_all(self.selectors["notifications"])
            notifications = []
            
            for element in notification_elements:
                if await element.is_visible():
                    text = await element.text_content()
                    if text:
                        notifications.append(text.strip())
            
            return notifications
        except Exception as e:
            self.logger.error(f"Failed to get notifications: {e}")
            return []
    
    async def get_breadcrumb(self) -> List[str]:
        """Get breadcrumb navigation items."""
        try:
            breadcrumb_elements = await self.page.query_selector_all(self.selectors["breadcrumb"])
            breadcrumbs = []
            
            for element in breadcrumb_elements:
                if await element.is_visible():
                    text = await element.text_content()
                    if text:
                        breadcrumbs.append(text.strip())
            
            return breadcrumbs
        except Exception as e:
            self.logger.error(f"Failed to get breadcrumb: {e}")
            return []
    
    async def is_logged_out(self) -> bool:
        """Check if user is logged out."""
        try:
            current_url = self.page.url
            return "/login" in current_url or "/logout" in current_url
        except Exception as e:
            self.logger.error(f"Error checking logout status: {e}")
            return False
    
    async def take_dashboard_screenshot(self, test_name: str = "dashboard", status: str = "unknown") -> str:
        """실패/에러 상태에서만 대시보드 스크린샷 저장."""
        from pathlib import Path
        from datetime import datetime
        
        if status not in ("failure", "error"):
            self.logger.info(f"Skipping dashboard screenshot for status '{status}'")
            return ""
        
        reports_dir = Path(f"reports/{self.config.environment}/screenshots")
        reports_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{status}_{timestamp}.png"
        screenshot_path = reports_dir / filename
        await self.page.screenshot(path=str(screenshot_path))
        self.logger.info(f"Screenshot saved: {screenshot_path}")
        return str(screenshot_path)
    
    async def wait_for_navigation(self, expected_url_pattern: str, timeout: int = 10000) -> bool:
        """Wait for navigation to specific URL pattern."""
        try:
            await self.page.wait_for_url(
                lambda url: expected_url_pattern in url,
                timeout=timeout
            )
            self.logger.info(f"Navigation completed to: {self.page.url}")
            return True
        except Exception as e:
            self.logger.error(f"Navigation timeout: {e}")
            return False
