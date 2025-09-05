#!/usr/bin/env python3
"""
모달 상태를 확인하는 스크립트
"""

import asyncio
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.config_loader import get_config
from utils.browser_manager import BrowserFactory
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.site_detail_page import SiteDetailPage

async def check_modal_state():
    """모달 상태 확인"""
    print("🔍 모달 상태 확인 시작...")
    
    config = get_config("dev")
    
    async with BrowserFactory.create(config) as browser_manager:
        # 로그인
        login_page = LoginPage(browser_manager.page, config)
        await login_page.navigate_to_login()
        await login_page.wait_for_page_load()
        
        space_id = "d-ge-pr"
        email = config.test_data.valid_user["email"]
        password = config.test_data.valid_user["password"]
        
        await login_page.login(space_id, email, password)
        
        if not await login_page.is_logged_in():
            print("❌ 로그인 실패")
            return
        
        print("✅ 로그인 성공")
        
        # 대시보드로 이동
        dashboard_page = DashboardPage(browser_manager.page, config)
        await dashboard_page.wait_for_dashboard_load()
        
        # 사이트 검색 및 선택
        await dashboard_page.search_sites("Search Test Site")
        site_click_success = await dashboard_page.click_first_available_site()
        
        if not site_click_success:
            print("❌ 사이트 클릭 실패")
            return
        
        print("✅ 사이트 선택 완료")
        
        # 사이트 상세 페이지로 이동
        site_detail_page = SiteDetailPage(browser_manager.page, config)
        await site_detail_page.wait_for_page_load()
        
        print("✅ 사이트 상세 페이지 로드 완료")
        
        # Add Plan 실행
        try:
            await site_detail_page.click_add_plan_button()
            print("✅ Add Plan 버튼 클릭 성공")
            
            # 파일 업로드 (자동 처리됨)
            print("✅ 이미지 파일 자동 업로드 완료")
            
            # Add Plan 모달에서 최종 확인
            add_plan_submitted = await site_detail_page.click_add_plan_submit()
            
            if add_plan_submitted:
                print("✅ Add Plan 모달에서 최종 확인 완료")
                
                # 페이지 새로고침
                await browser_manager.page.reload()
                await asyncio.sleep(5)
                
                print("\n📋 모달 상태 확인")
                print("-" * 50)
                
                # 모든 모달 관련 요소 찾기
                modals = await browser_manager.page.query_selector_all(".el-dialog")
                print(f"📝 총 {len(modals)}개의 모달 발견")
                
                for i, modal in enumerate(modals):
                    try:
                        class_name = await modal.get_attribute("class")
                        is_visible = await modal.is_visible()
                        aria_modal = await modal.get_attribute("aria-modal")
                        aria_label = await modal.get_attribute("aria-label")
                        
                        print(f"🔍 모달 {i+1}: class='{class_name}', visible={is_visible}, aria-modal='{aria_modal}', aria-label='{aria_label}'")
                        
                        # 모달 내부 요소 확인
                        if "create-survey-dialog" in class_name:
                            print(f"  📝 New Survey 모달 내부 요소:")
                            
                            # input 요소
                            inputs = await modal.query_selector_all("input")
                            for j, input_elem in enumerate(inputs):
                                input_type = await input_elem.get_attribute("type")
                                placeholder = await input_elem.get_attribute("placeholder")
                                is_input_visible = await input_elem.is_visible()
                                print(f"    Input {j+1}: type='{input_type}', placeholder='{placeholder}', visible={is_input_visible}")
                            
                            # 버튼 요소
                            buttons = await modal.query_selector_all("button")
                            for j, button in enumerate(buttons):
                                text = await button.text_content()
                                button_class = await button.get_attribute("class")
                                is_button_visible = await button.is_visible()
                                print(f"    Button {j+1}: '{text}', class='{button_class}', visible={is_button_visible}")
                        
                    except Exception as e:
                        continue
                
                # 모달 래퍼 확인
                wrappers = await browser_manager.page.query_selector_all(".el-dialog__wrapper")
                print(f"\n📝 총 {len(wrappers)}개의 모달 래퍼 발견")
                
                for i, wrapper in enumerate(wrappers):
                    try:
                        class_name = await wrapper.get_attribute("class")
                        is_visible = await wrapper.is_visible()
                        style = await wrapper.get_attribute("style")
                        
                        print(f"🔍 래퍼 {i+1}: class='{class_name}', visible={is_visible}, style='{style}'")
                        
                    except Exception as e:
                        continue
                
                # 스크린샷 저장
                await browser_manager.take_screenshot("modal_state_check")
                print("\n📸 모달 상태 확인 스크린샷 저장됨")
                
            else:
                print("❌ Add Plan 모달 확인 실패")
                
        except Exception as e:
            print(f"❌ Add Plan 실행 중 오류: {e}")

if __name__ == "__main__":
    asyncio.run(check_modal_state())
