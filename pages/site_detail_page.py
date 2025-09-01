#!/usr/bin/env python3
"""
Site Detail Page Object Model
"""

import asyncio
import logging
from typing import Optional, List, Dict
from utils.config_loader import EnvironmentConfig


class SiteDetailPage:
    """Page Object Model for Beamo Site Detail Page"""
    
    def __init__(self, page, config: EnvironmentConfig):
        self.page = page
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Common selectors (based on actual Beamo site detail page)
        self.selectors = {
            # 글로벌 네비게이션은 별도 컴포넌트로 관리
            # (GlobalNavigation 클래스 사용)
            
            # 메인 콘텐츠 영역
            "main_content": ".el-main, .main-content",
            "control_panel": ".control-panel__content",
            "control_panel_collapse": ".control-panel__collapse-btn",
            
            # 사이트 프로필
            "site_profile": ".site-profile",
            "site_profile_bookmark": ".site-profile__bookmark",
            "site_name": ".site-profile h3, .site-name, .site-title",
            "site_address": ".site-address, .building-address",
            
            # 측정 도구
            "measure_tools": "[class*='measure'], [class*='tool'], [class*='ruler'], [class*='distance']",
            "measure_button": ".measure-button, .tool-button",
            "distance_tool": "[class*='distance']",
            "area_tool": "[class*='area']",
            "volume_tool": "[class*='volume']",
            "angle_tool": "[class*='angle']",
            
            # 3D 뷰어
            "viewer_container": "[class*='viewer'], [class*='3d'], [class*='canvas'], [class*='scene']",
            "viewer_canvas": "canvas",
            "viewer_controls": ".viewer-controls, .scene-controls",
            
            # 네비게이션
            "navigation_menu": ".nav-menu, .sidebar, .side-menu",
            "breadcrumb": ".breadcrumb, .nav-breadcrumb",
            
            # 액션 버튼들
            "export_button": "[class*='export']",
            "import_button": "[class*='import']",
            "share_button": "[class*='share']",
            "settings_button": "[class*='settings']",
            "help_button": "[class*='help']",
            
            # 상태 표시
            "loading_indicator": ".loading, .spinner",
            "error_message": ".error-message, .alert-error",
            "success_message": ".success-message, .alert-success",
            
            # Add a new plan 다이얼로그 (Guide 형태)
            "add_plan_dialog": "div.add-plan-guide",
            "add_plan_title": "h4.guide-title",
            "add_plan_content": "div.guide-content",
            "add_plan_learn_more_button": "button.el-button.el-button--default.el-button--small:has-text('Learn more')",
            "add_plan_got_it_button": "button.el-button.el-button--primary.el-button--small:has-text('Got it')",
            "add_plan_close_button": ".el-dialog__headerbtn, .close-button",
            
            # Add plan 버튼 (사이트에서 플랜 추가) - 우측 상단 버튼
            "add_plan_button": "button.el-button--primary.el-button--mini:has-text('Add plan')",
            "add_plan_file_input": ".el-upload--picture input[type='file']",
            "add_plan_dialog": ".el-dialog:has-text('Each image will be added as a single plan')",
            "add_plan_dialog_title": ".el-dialog__title, .dialog-title",
            "add_plan_dialog_content": ".el-dialog__body, .dialog-body",
            "add_plan_submit_button": "button:has-text('Add Plan').el-button--primary, button:has-text('Save').el-button--primary",
            "add_plan_cancel_button": "button:has-text('Cancel')",
            
            # Survey creation modal (Add Plan 성공 후 나타나는 모달)
            "survey_creation_modal": ".el-dialog:has-text('Create a new survey')",
            "survey_creation_modal_close": ".el-dialog__headerbtn, .el-dialog__close",
            "survey_creation_modal_title": ".el-dialog__title:has-text('Create a new survey')",
            "survey_creation_modal_content": ".el-dialog__body",
            "survey_creation_qr_code": ".qr-code, [class*='qr']",
            "survey_creation_download_button": "button:has-text('Download on the App Store')",
            "survey_creation_learn_more": "button:has-text('Learn more')",
            "survey_creation_got_it": "button:has-text('Got it')",
            
            # New Survey Creation selectors (Add Plan 성공 후 나타나는 + New survey 버튼)
            "new_survey_button": "button:has-text('New survey').el-button--primary.el-button--mini, button:has-text('New survey').create-survey-button",
            "new_survey_modal": ".el-dialog.create-survey-dialog",
            "new_survey_modal_close": ".el-dialog.create-survey-dialog .el-dialog__close",
            "new_survey_name_input": ".el-dialog.create-survey-dialog input[placeholder='Survey Title']",
            "new_survey_cancel_button": ".el-dialog.create-survey-dialog button:has-text('Cancel').el-button--default.el-button--small",
            "new_survey_add_button": ".el-dialog.create-survey-dialog button:has-text('Add').el-button--primary.el-button--small",
            
            # 갤러리 이미지 추가 관련 (하단 갤러리 섹션)
            "gallery_section": ".gallery, .image-gallery, .photo-gallery",
            "gallery_add_button": ".el-upload--text button, .el-upload--text .el-button--primary.el-button--mini.is-circle",
            "gallery_file_input": "input[type='file'][accept*='image'], input[type='file'][accept*='jpg'], input[type='file'][accept*='png'], input[type='file'][accept*='jpeg']",
            "gallery_dialog": ".el-dialog, .modal, .upload-dialog",
            "gallery_dialog_title": ".el-dialog__title, .dialog-title, .upload-title",
            "gallery_dialog_content": ".el-dialog__body, .dialog-body, .upload-content",
            "gallery_submit_button": "button:has-text('Upload'), button:has-text('Add'), button:has-text('Save')",
            "gallery_cancel_button": "button:has-text('Cancel')",
            "gallery_images": ".gallery-item, .image-item, .photo-item, .gallery-image",
            "gallery_image": "img[src*='gallery'], img[src*='image'], img[src*='photo']",
        }
    
    async def wait_for_page_load(self) -> None:
        """Wait for site detail page to be fully loaded."""
        try:
            # Wait for main content to be visible
            await self.page.wait_for_selector(
                self.selectors["main_content"],
                timeout=10000
            )
            self.logger.info("Site detail page loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load site detail page: {e}")
            raise
    
    async def is_page_loaded(self) -> bool:
        """Check if site detail page is loaded."""
        try:
            main_content = await self.page.query_selector(self.selectors["main_content"])
            return main_content is not None and await main_content.is_visible()
        except Exception:
            return False
    
    async def get_page_title(self) -> str:
        """Get page title."""
        try:
            return await self.page.title()
        except Exception as e:
            self.logger.error(f"Failed to get page title: {e}")
            return ""
    
    async def get_current_url(self) -> str:
        """Get current URL."""
        try:
            return self.page.url
        except Exception as e:
            self.logger.error(f"Failed to get current URL: {e}")
            return ""
    
    async def get_site_name(self) -> str:
        """Get site name."""
        try:
            site_name_elem = await self.page.query_selector(self.selectors["site_name"])
            if site_name_elem:
                return await site_name_elem.text_content()
            return ""
        except Exception as e:
            self.logger.error(f"Failed to get site name: {e}")
            return ""
    
    async def get_site_address(self) -> str:
        """Get site address."""
        try:
            address_elem = await self.page.query_selector(self.selectors["site_address"])
            if address_elem:
                return await address_elem.text_content()
            return ""
        except Exception as e:
            self.logger.error(f"Failed to get site address: {e}")
            return ""
    
    async def toggle_bookmark(self) -> None:
        """Toggle site bookmark."""
        try:
            bookmark_button = await self.page.wait_for_selector(self.selectors["site_profile_bookmark"])
            await bookmark_button.click()
            self.logger.info("Toggled site bookmark")
        except Exception as e:
            self.logger.error(f"Failed to toggle bookmark: {e}")
            raise
    
    async def collapse_control_panel(self) -> None:
        """Collapse control panel."""
        try:
            collapse_button = await self.page.wait_for_selector(self.selectors["control_panel_collapse"])
            await collapse_button.click()
            self.logger.info("Collapsed control panel")
        except Exception as e:
            self.logger.error(f"Failed to collapse control panel: {e}")
            raise
    
    async def expand_control_panel(self) -> None:
        """Expand control panel."""
        try:
            expand_button = await self.page.wait_for_selector(self.selectors["control_panel_collapse"])
            await expand_button.click()
            self.logger.info("Expanded control panel")
        except Exception as e:
            self.logger.error(f"Failed to expand control panel: {e}")
            raise
    
    async def get_measure_tools(self) -> List[Dict]:
        """Get available measure tools."""
        try:
            tool_elements = await self.page.query_selector_all(self.selectors["measure_tools"])
            tools = []
            
            for tool in tool_elements:
                try:
                    tool_class = await tool.get_attribute("class")
                    tool_text = await tool.text_content()
                    tool_visible = await tool.is_visible()
                    
                    tools.append({
                        "class": tool_class,
                        "text": tool_text.strip() if tool_text else "",
                        "visible": tool_visible
                    })
                except Exception:
                    continue
            
            return tools
        except Exception as e:
            self.logger.error(f"Failed to get measure tools: {e}")
            return []
    
    async def click_measure_tool(self, tool_name: str) -> None:
        """Click a specific measure tool."""
        try:
            # Try to find tool by text content
            tool_selector = f"{self.selectors['measure_tools']}:has-text('{tool_name}')"
            tool = await self.page.wait_for_selector(tool_selector, timeout=5000)
            await tool.click()
            self.logger.info(f"Clicked measure tool: {tool_name}")
        except Exception as e:
            self.logger.error(f"Failed to click measure tool {tool_name}: {e}")
            raise
    
    async def click_distance_tool(self) -> None:
        """Click distance measurement tool."""
        await self.click_measure_tool("Distance")
    
    async def click_area_tool(self) -> None:
        """Click area measurement tool."""
        await self.click_measure_tool("Area")
    
    async def click_volume_tool(self) -> None:
        """Click volume measurement tool."""
        await self.click_measure_tool("Volume")
    
    async def click_angle_tool(self) -> None:
        """Click angle measurement tool."""
        await self.click_measure_tool("Angle")
    
    async def is_viewer_loaded(self) -> bool:
        """Check if 3D viewer is loaded."""
        try:
            viewer = await self.page.query_selector(self.selectors["viewer_container"])
            return viewer is not None and await viewer.is_visible()
        except Exception:
            return False
    
    async def wait_for_viewer_load(self, timeout: int = 30000) -> None:
        """Wait for 3D viewer to load."""
        try:
            await self.page.wait_for_selector(self.selectors["viewer_container"], timeout=timeout)
            self.logger.info("3D viewer loaded")
        except Exception as e:
            self.logger.error(f"Failed to load 3D viewer: {e}")
            raise
    
    async def get_viewer_controls(self) -> List[Dict]:
        """Get viewer control buttons."""
        try:
            control_elements = await self.page.query_selector_all(self.selectors["viewer_controls"])
            controls = []
            
            for control in control_elements:
                try:
                    control_class = await control.get_attribute("class")
                    control_text = await control.text_content()
                    control_visible = await control.is_visible()
                    
                    controls.append({
                        "class": control_class,
                        "text": control_text.strip() if control_text else "",
                        "visible": control_visible
                    })
                except Exception:
                    continue
            
            return controls
        except Exception as e:
            self.logger.error(f"Failed to get viewer controls: {e}")
            return []
    
    async def click_export_button(self) -> None:
        """Click export button."""
        try:
            export_button = await self.page.wait_for_selector(self.selectors["export_button"])
            await export_button.click()
            self.logger.info("Clicked export button")
        except Exception as e:
            self.logger.error(f"Failed to click export button: {e}")
            raise
    
    async def click_share_button(self) -> None:
        """Click share button."""
        try:
            share_button = await self.page.wait_for_selector(self.selectors["share_button"])
            await share_button.click()
            self.logger.info("Clicked share button")
        except Exception as e:
            self.logger.error(f"Failed to click share button: {e}")
            raise
    
    async def click_settings_button(self) -> None:
        """Click settings button."""
        try:
            settings_button = await self.page.wait_for_selector(self.selectors["settings_button"])
            await settings_button.click()
            self.logger.info("Clicked settings button")
        except Exception as e:
            self.logger.error(f"Failed to click settings button: {e}")
            raise
    
    async def is_loading(self) -> bool:
        """Check if page is loading."""
        try:
            loading_indicator = await self.page.query_selector(self.selectors["loading_indicator"])
            return loading_indicator is not None and await loading_indicator.is_visible()
        except Exception:
            return False
    
    async def wait_for_loading_complete(self, timeout: int = 30000) -> None:
        """Wait for loading to complete."""
        try:
            # Wait for loading indicator to disappear
            await self.page.wait_for_selector(self.selectors["loading_indicator"], state="hidden", timeout=timeout)
            self.logger.info("Loading completed")
        except Exception as e:
            self.logger.error(f"Failed to wait for loading completion: {e}")
            raise
    
    async def get_error_message(self) -> str:
        """Get error message if any."""
        try:
            error_elem = await self.page.query_selector(self.selectors["error_message"])
            if error_elem:
                return await error_elem.text_content()
            return ""
        except Exception as e:
            self.logger.error(f"Failed to get error message: {e}")
            return ""
    
    async def get_success_message(self) -> str:
        """Get success message if any."""
        try:
            success_elem = await self.page.query_selector(self.selectors["success_message"])
            if success_elem:
                return await success_elem.text_content()
            return ""
        except Exception as e:
            self.logger.error(f"Failed to get success message: {e}")
            return ""
    
    async def take_screenshot(self, test_name: str = "site_detail", status: str = "unknown") -> str:
        """Take screenshot of site detail page with test name and status."""
        try:
            import os
            from datetime import datetime
            screenshot_dir = f"reports/{self.config.environment}/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            
            # Generate filename with test name, status, and timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{test_name}_{status}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)
            
            await self.page.screenshot(path=filepath)
            self.logger.info(f"Screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {e}")
            return ""
    
    # Add a new plan 다이얼로그 관련 메서드들
    async def is_add_plan_dialog_visible(self) -> bool:
        """Check if 'Add a new plan' dialog is visible."""
        try:
            dialog = await self.page.query_selector(self.selectors["add_plan_dialog"])
            return dialog is not None and await dialog.is_visible()
        except Exception:
            return False
    
    async def wait_for_add_plan_dialog(self, timeout: int = 10000) -> None:
        """Wait for 'Add a new plan' dialog to appear."""
        try:
            await self.page.wait_for_selector(self.selectors["add_plan_dialog"], timeout=timeout)
            self.logger.info("Add a new plan dialog appeared")
        except Exception as e:
            self.logger.error(f"Failed to wait for add plan dialog: {e}")
            raise
    
    async def get_add_plan_title(self) -> str:
        """Get the title of 'Add a new plan' dialog."""
        try:
            title_elem = await self.page.query_selector(self.selectors["add_plan_title"])
            if title_elem:
                return await title_elem.text_content()
            return ""
        except Exception as e:
            self.logger.error(f"Failed to get add plan title: {e}")
            return ""
    
    async def get_add_plan_content(self) -> str:
        """Get the content text of 'Add a new plan' dialog."""
        try:
            content_elem = await self.page.query_selector(self.selectors["add_plan_content"])
            if content_elem:
                return await content_elem.text_content()
            return ""
        except Exception as e:
            self.logger.error(f"Failed to get add plan content: {e}")
            return ""
    
    async def click_learn_more_button(self) -> None:
        """Click 'Learn more' button in 'Add a new plan' dialog."""
        try:
            learn_more_button = await self.page.wait_for_selector(self.selectors["add_plan_learn_more_button"])
            await learn_more_button.click()
            self.logger.info("Clicked Learn more button")
        except Exception as e:
            self.logger.error(f"Failed to click Learn more button: {e}")
            raise
    
    async def click_got_it_button(self) -> None:
        """Click 'Got it' button in 'Add a new plan' dialog."""
        try:
            got_it_button = await self.page.wait_for_selector(self.selectors["add_plan_got_it_button"])
            await got_it_button.click()
            self.logger.info("Clicked Got it button")
        except Exception as e:
            self.logger.error(f"Failed to click Got it button: {e}")
            raise
    
    async def close_add_plan_dialog(self) -> None:
        """Close 'Add a new plan' dialog."""
        try:
            close_button = await self.page.wait_for_selector(self.selectors["add_plan_close_button"])
            await close_button.click()
            self.logger.info("Closed Add a new plan dialog")
        except Exception as e:
            self.logger.error(f"Failed to close Add a new plan dialog: {e}")
            raise
    
    async def handle_add_plan_dialog(self, action: str = "got_it") -> None:
        """Handle 'Add a new plan' dialog with specified action."""
        try:
            if not await self.is_add_plan_dialog_visible():
                self.logger.info("Add a new plan dialog is not visible")
                return
            
            if action == "learn_more":
                await self.click_learn_more_button()
            elif action == "got_it":
                await self.click_got_it_button()
            elif action == "close":
                await self.close_add_plan_dialog()
            else:
                self.logger.warning(f"Unknown action: {action}")
                
        except Exception as e:
            self.logger.error(f"Failed to handle Add a new plan dialog: {e}")
            raise
    
    # Add plan 버튼 관련 메서드들 (사이트에서 플랜 추가)
    async def click_add_plan_button(self) -> None:
        """Click the +Add plan button."""
        try:
            # 먼저 query_selector로 시도
            add_plan_button = await self.page.query_selector(self.selectors["add_plan_button"])
            
            if not add_plan_button:
                # query_selector가 실패하면 wait_for_selector로 시도
                add_plan_button = await self.page.wait_for_selector(self.selectors["add_plan_button"], timeout=5000)
            
            if add_plan_button:
                await add_plan_button.click()
                self.logger.info("Clicked +Add plan button")
            else:
                raise Exception("Add plan button not found")
                
        except Exception as e:
            self.logger.error(f"Failed to click +Add plan button: {e}")
            raise
    
    async def is_add_plan_dialog_open(self) -> bool:
        """Check if Add plan dialog is open."""
        try:
            dialog = await self.page.query_selector(self.selectors["add_plan_dialog"])
            return dialog is not None and await dialog.is_visible()
        except Exception:
            return False
    
    async def wait_for_add_plan_dialog_open(self, timeout: int = 10000) -> None:
        """Wait for Add plan dialog to open."""
        try:
            await self.page.wait_for_selector(self.selectors["add_plan_dialog"], timeout=timeout)
            self.logger.info("Add plan dialog opened")
        except Exception as e:
            self.logger.error(f"Failed to wait for Add plan dialog: {e}")
            raise
    
    async def get_add_plan_dialog_title(self) -> str:
        """Get the title of Add plan dialog."""
        try:
            title_elem = await self.page.query_selector(self.selectors["add_plan_dialog_title"])
            if title_elem:
                return await title_elem.text_content()
            return ""
        except Exception as e:
            self.logger.error(f"Failed to get Add plan dialog title: {e}")
            return ""
    
    async def get_add_plan_dialog_content(self) -> str:
        """Get the content of Add plan dialog."""
        try:
            content_elem = await self.page.query_selector(self.selectors["add_plan_dialog_content"])
            if content_elem:
                return await content_elem.text_content()
            return ""
        except Exception as e:
            self.logger.error(f"Failed to get Add plan dialog content: {e}")
            return ""
    
    async def click_add_plan_submit(self) -> None:
        """Click the Add Plan submit button."""
        try:
            submit_button = await self.page.wait_for_selector(self.selectors["add_plan_submit_button"])
            await submit_button.click()
            self.logger.info("Clicked Add Plan submit button")
        except Exception as e:
            self.logger.error(f"Failed to click Add Plan submit button: {e}")
            raise
    
    async def click_add_plan_cancel(self) -> None:
        """Click the Cancel button in Add plan dialog."""
        try:
            cancel_button = await self.page.wait_for_selector(self.selectors["add_plan_cancel_button"])
            await cancel_button.click()
            self.logger.info("Clicked Add plan cancel button")
        except Exception as e:
            self.logger.error(f"Failed to click Add plan cancel button: {e}")
            raise
    
    async def add_plan(self, file_path: str = "") -> bool:
        """Add a new plan to the site by uploading a file."""
        try:
            # Click +Add plan button
            await self.click_add_plan_button()
            
            # Wait for file input to be available
            await self.wait_for_file_input()
            
            # Upload file if provided
            if file_path:
                await self.upload_plan_file(file_path)
            
            self.logger.info("Plan file uploaded successfully")
            return True
                
        except Exception as e:
            self.logger.error(f"Failed to add plan: {e}")
            return False
    
    async def wait_for_file_input(self, timeout: int = 10000) -> None:
        """Wait for file input to be available."""
        try:
            # 보이지 않는 파일 입력 요소도 찾기 (visible=False로 설정)
            file_input = await self.page.wait_for_selector(self.selectors["add_plan_file_input"], timeout=timeout, state="attached")
            self.logger.info("File input is available")
        except Exception as e:
            self.logger.error(f"Failed to wait for file input: {e}")
            raise
    
    async def upload_plan_file(self, file_path: str) -> None:
        """Upload a plan file."""
        try:
            # 파일 입력 요소가 보일 때까지 대기 (visible=False로 설정)
            file_input = await self.page.wait_for_selector(self.selectors["add_plan_file_input"], timeout=30000, state="attached")
            
            # 파일 업로드
            await file_input.set_input_files(file_path)
            self.logger.info(f"Plan file uploaded: {file_path}")
        except Exception as e:
            self.logger.error(f"Failed to upload plan file: {e}")
    
    async def click_add_plan_submit(self) -> bool:
        """Add Plan 모달 다이얼로그에서 최종 Add Plan 버튼 클릭"""
        try:
            # 모달 다이얼로그가 나타날 때까지 대기
            await self.page.wait_for_selector(self.selectors["add_plan_dialog"], timeout=15000)
            self.logger.info("Add Plan modal dialog appeared")
            
            # JavaScript로 Add Plan 버튼 클릭 시도 (다이얼로그 오버레이 문제 해결)
            try:
                await self.page.evaluate("""
                    () => {
                        // Add Plan 텍스트를 포함한 버튼 찾기
                        const buttons = document.querySelectorAll('button.el-button--primary');
                        for (let button of buttons) {
                            if (button.textContent && button.textContent.includes('Add Plan')) {
                                button.click();
                                return true;
                            }
                        }
                        return false;
                    }
                """)
                self.logger.info("Clicked Add Plan submit button via JavaScript")
                
                # 로딩 마스크가 사라질 때까지 대기
                try:
                    await self.page.wait_for_selector(".el-loading-mask", state="hidden", timeout=30000)
                    self.logger.info("Loading mask disappeared")
                except Exception as e:
                    self.logger.warning(f"Loading mask wait timeout: {e}")
                
                # 추가 대기
                await asyncio.sleep(3)
                return True
                
            except Exception as js_error:
                self.logger.warning(f"JavaScript click failed: {js_error}")
                
                # 일반 클릭으로 폴백
                submit_button = await self.page.query_selector("button.el-button--primary:has-text('Add Plan')")
                
                if submit_button:
                    await submit_button.click()
                    self.logger.info("Clicked Add Plan submit button via normal click")
                    
                    # 모달이 닫힐 때까지 대기
                    await asyncio.sleep(3)
                    return True
                else:
                    self.logger.warning("Add Plan submit button not found in modal")
                    return False
                
        except Exception as e:
            self.logger.error(f"Failed to click Add Plan submit: {e}")
            return False
    
    # Survey creation modal 관련 메서드들 (Add Plan 성공 후)
    async def is_survey_creation_modal_visible(self) -> bool:
        """Check if 'Create a new survey' modal is visible (Add Plan 성공 확인)"""
        try:
            modal = await self.page.query_selector(self.selectors["survey_creation_modal"])
            if modal:
                visible = await modal.is_visible()
                self.logger.info(f"Survey creation modal visible: {visible}")
                return visible
            return False
        except Exception as e:
            self.logger.error(f"Failed to check survey creation modal: {e}")
            return False
    
    async def close_survey_creation_modal(self) -> bool:
        """Close the 'Create a new survey' modal by clicking X button"""
        try:
            # X 버튼 클릭
            close_button = await self.page.query_selector(self.selectors["survey_creation_modal_close"])
            
            if close_button:
                await close_button.click()
                self.logger.info("Clicked X button to close survey creation modal")
                
                # 모달이 닫힐 때까지 대기
                await asyncio.sleep(2)
                return True
            else:
                self.logger.warning("Survey creation modal close button not found")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to close survey creation modal: {e}")
            return False
    
    # 갤러리 이미지 추가 관련 메서드들
    async def is_gallery_section_visible(self) -> bool:
        """Check if gallery section is visible."""
        try:
            gallery = await self.page.query_selector(self.selectors["gallery_section"])
            return gallery is not None and await gallery.is_visible()
        except Exception:
            return False
    
    async def click_gallery_add_button(self) -> None:
        """Click the gallery add image button."""
        try:
            add_button = await self.page.wait_for_selector(self.selectors["gallery_add_button"])
            await add_button.click()
            self.logger.info("Clicked gallery add image button")
        except Exception as e:
            self.logger.error(f"Failed to click gallery add button: {e}")
            raise
    
    async def is_gallery_dialog_open(self) -> bool:
        """Check if gallery upload dialog is open."""
        try:
            dialog = await self.page.query_selector(self.selectors["gallery_dialog"])
            return dialog is not None and await dialog.is_visible()
        except Exception:
            return False
    
    async def wait_for_gallery_dialog_open(self, timeout: int = 10000) -> None:
        """Wait for gallery upload dialog to open."""
        try:
            await self.page.wait_for_selector(self.selectors["gallery_dialog"], timeout=timeout)
            self.logger.info("Gallery upload dialog opened")
        except Exception as e:
            self.logger.error(f"Failed to wait for gallery dialog: {e}")
            raise
    
    async def get_gallery_dialog_title(self) -> str:
        """Get the title of gallery upload dialog."""
        try:
            title_elem = await self.page.query_selector(self.selectors["gallery_dialog_title"])
            if title_elem:
                return await title_elem.text_content()
            return ""
        except Exception as e:
            self.logger.error(f"Failed to get gallery dialog title: {e}")
            return ""
    
    async def wait_for_gallery_file_input(self, timeout: int = 10000) -> None:
        """Wait for gallery file input to be available."""
        try:
            # 보이지 않는 파일 입력 요소도 찾기 (visible=False로 설정)
            file_input = await self.page.wait_for_selector(self.selectors["gallery_file_input"], timeout=timeout, state="attached")
            self.logger.info("Gallery file input is available")
        except Exception as e:
            self.logger.error(f"Failed to wait for gallery file input: {e}")
            raise
    
    async def upload_gallery_image(self, file_path: str) -> None:
        """Upload an image to gallery."""
        try:
            # 파일 입력 요소가 보일 때까지 대기 (visible=False로 설정)
            file_input = await self.page.wait_for_selector(self.selectors["gallery_file_input"], timeout=30000, state="attached")
            
            # 파일 업로드
            await file_input.set_input_files(file_path)
            self.logger.info(f"Gallery image uploaded: {file_path}")
        except Exception as e:
            self.logger.error(f"Failed to upload gallery image: {e}")
            raise
    
    async def click_gallery_submit(self) -> None:
        """Click the gallery upload submit button."""
        try:
            submit_button = await self.page.wait_for_selector(self.selectors["gallery_submit_button"])
            await submit_button.click()
            self.logger.info("Clicked gallery upload submit button")
        except Exception as e:
            self.logger.error(f"Failed to click gallery submit button: {e}")
            raise
    
    async def click_gallery_cancel(self) -> None:
        """Click the Cancel button in gallery upload dialog."""
        try:
            cancel_button = await self.page.wait_for_selector(self.selectors["gallery_cancel_button"])
            await cancel_button.click()
            self.logger.info("Clicked gallery upload cancel button")
        except Exception as e:
            self.logger.error(f"Failed to click gallery cancel button: {e}")
            raise
    
    async def add_gallery_image(self, file_path: str = "") -> bool:
        """Add a new image to the gallery by uploading a file."""
        try:
            # Click gallery add button
            await self.click_gallery_add_button()
            
            # Wait for file input to be available
            await self.wait_for_gallery_file_input()
            
            # Upload file if provided
            if file_path:
                await self.upload_gallery_image(file_path)
            
            self.logger.info("Gallery image uploaded successfully")
            return True
                
        except Exception as e:
            self.logger.error(f"Failed to add gallery image: {e}")
            return False
    
    async def get_gallery_images_count(self) -> int:
        """Get the number of images in the gallery."""
        try:
            images = await self.page.query_selector_all(self.selectors["gallery_images"])
            return len(images)
        except Exception as e:
            self.logger.error(f"Failed to get gallery images count: {e}")
            return 0
    
    async def get_gallery_images(self) -> List[Dict]:
        """Get all gallery images information."""
        try:
            image_elements = await self.page.query_selector_all(self.selectors["gallery_image"])
            images = []
            
            for img in image_elements:
                try:
                    src = await img.get_attribute("src")
                    alt = await img.get_attribute("alt")
                    visible = await img.is_visible()
                    
                    images.append({
                        "src": src,
                        "alt": alt,
                        "visible": visible
                    })
                except Exception:
                    continue
            
            return images
        except Exception as e:
            self.logger.error(f"Failed to get gallery images: {e}")
            return []
    
    # New Survey Creation 메서드들
    async def click_new_survey_button(self) -> bool:
        """+ New survey 버튼 클릭"""
        try:
            # 1단계: 모든 숨겨진 모달 닫기
            await self.close_all_hidden_modals()
            
            # 2단계: + New survey 버튼 찾기 및 클릭
            new_survey_button = None
            
            # 방법 1: 기본 셀렉터로 찾기
            new_survey_button = await self.page.query_selector(self.selectors["new_survey_button"])
            
            # 방법 2: 정확한 셀렉터로 찾기
            if not new_survey_button:
                new_survey_button = await self.page.query_selector("button:has-text('New survey').el-button--primary.el-button--mini")
            
            # 방법 3: create-survey-button 클래스로 찾기
            if not new_survey_button:
                new_survey_button = await self.page.query_selector("button:has-text('New survey').create-survey-button")
            
            # 방법 4: 모든 버튼 중에서 찾기
            if not new_survey_button:
                buttons = await self.page.query_selector_all("button")
                for button in buttons:
                    text = await button.text_content()
                    class_name = await button.get_attribute("class")
                    is_visible = await button.is_visible()
                    if text and "new survey" in text.lower() and "primary" in class_name and is_visible:
                        new_survey_button = button
                        break
            
            if new_survey_button:
                # 버튼이 보이는지 확인
                is_visible = await new_survey_button.is_visible()
                if not is_visible:
                    self.logger.warning("+ New survey button found but not visible")
                    return False
                
                # 3단계: 버튼 클릭
                await new_survey_button.click()
                self.logger.info("Clicked + New survey button")
                
                # 4단계: 모달이 나타날 때까지 대기
                await asyncio.sleep(3)
                
                # 5단계: 모달이 나타났는지 확인
                if await self.is_new_survey_modal_visible():
                    self.logger.info("New Survey modal appeared after button click")
                    return True
                else:
                    self.logger.warning("New Survey modal did not appear after button click")
                    return False
            else:
                self.logger.warning("+ New survey button not found")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to click + New survey button: {e}")
            return False
    
    async def close_all_hidden_modals(self) -> bool:
        """모든 숨겨진 모달 닫기"""
        try:
            # 모든 모달 래퍼 찾기
            wrappers = await self.page.query_selector_all(".el-dialog__wrapper")
            
            for wrapper in wrappers:
                try:
                    # 모달이 보이는지 확인
                    is_visible = await wrapper.is_visible()
                    if not is_visible:
                        # 숨겨진 모달의 닫기 버튼 찾기
                        close_button = await wrapper.query_selector(".el-dialog__close, .el-dialog__headerbtn")
                        if close_button:
                            await close_button.click()
                            self.logger.info("Closed hidden modal")
                            await asyncio.sleep(0.5)
                except Exception as e:
                    continue
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to close hidden modals: {e}")
            return False
    
    async def is_new_survey_modal_visible(self) -> bool:
        """New Survey 모달이 보이는지 확인"""
        try:
            # 모달이 존재하고 보이는지 확인
            modal = await self.page.query_selector(self.selectors["new_survey_modal"])
            if modal:
                is_visible = await modal.is_visible()
                self.logger.info(f"New Survey modal found, visible: {is_visible}")
                return is_visible
            else:
                self.logger.warning("New Survey modal not found")
                return False
        except Exception as e:
            self.logger.error(f"Failed to check new survey modal visibility: {e}")
            return False
    
    async def create_new_survey(self, survey_name: str) -> bool:
        """새 서베이 생성"""
        try:
            # New Survey 모달이 나타날 때까지 대기 (여러 방법 시도)
            modal_found = False
            
            # 방법 1: 기본 셀렉터로 대기
            try:
                await self.page.wait_for_selector(self.selectors["new_survey_modal"], timeout=5000)
                modal_found = True
                self.logger.info("New Survey modal found with basic selector")
            except:
                pass
            
            # 방법 2: 모달이 보일 때까지 대기
            if not modal_found:
                for attempt in range(10):
                    if await self.is_new_survey_modal_visible():
                        modal_found = True
                        self.logger.info("New Survey modal found with visibility check")
                        break
                    await asyncio.sleep(1)
            
            if not modal_found:
                self.logger.error("New Survey modal not found after waiting")
                return False
            
            # 모달이 완전히 로드될 때까지 추가 대기
            await asyncio.sleep(3)
            
            # 서베이 이름 입력 (여러 방법 시도)
            name_input = None
            
            # 방법 1: placeholder로 찾기
            name_input = await self.page.query_selector("input[placeholder='Survey Title']")
            
            # 방법 2: 모달 내부에서 찾기
            if not name_input:
                name_input = await self.page.query_selector(".el-dialog.create-survey-dialog input[type='text']")
            
            # 방법 3: 모든 input 중에서 찾기
            if not name_input:
                inputs = await self.page.query_selector_all("input[type='text']")
                for input_elem in inputs:
                    placeholder = await input_elem.get_attribute("placeholder")
                    if placeholder and "survey" in placeholder.lower():
                        name_input = input_elem
                        break
            
            if name_input:
                await name_input.clear()
                await name_input.fill(survey_name)
                self.logger.info(f"Entered survey name: {survey_name}")
                await asyncio.sleep(1)
                
                # Add 버튼 클릭 (여러 방법 시도)
                add_button = None
                
                # 방법 1: 정확한 셀렉터로 찾기
                add_button = await self.page.query_selector(".el-dialog.create-survey-dialog button:has-text('Add').el-button--primary.el-button--small")
                
                # 방법 2: 모달 내부에서 찾기
                if not add_button:
                    add_button = await self.page.query_selector(".el-dialog.create-survey-dialog button:has-text('Add')")
                
                # 방법 3: 모든 버튼 중에서 찾기
                if not add_button:
                    buttons = await self.page.query_selector_all("button")
                    for button in buttons:
                        text = await button.text_content()
                        class_name = await button.get_attribute("class")
                        is_visible = await button.is_visible()
                        if text and "add" in text.lower() and "primary" in class_name and is_visible:
                            add_button = button
                            break
                
                if add_button:
                    await add_button.click()
                    self.logger.info("Clicked Add button to create survey")
                    await asyncio.sleep(3)
                    return True
                else:
                    self.logger.warning("Add button not found in new survey modal")
                    return False
            else:
                self.logger.warning("Survey name input not found")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to create new survey: {e}")
            return False
    
    async def close_new_survey_modal(self) -> bool:
        """New Survey 모달 닫기"""
        try:
            close_button = await self.page.query_selector(self.selectors["new_survey_modal_close"])
            if close_button:
                await close_button.click()
                self.logger.info("New survey modal closed")
                await asyncio.sleep(2)
                return True
            else:
                self.logger.warning("New survey modal close button not found")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to close new survey modal: {e}")
            return False
