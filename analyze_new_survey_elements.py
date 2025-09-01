#!/usr/bin/env python3
"""
+ New survey 버튼과 관련 요소들을 분석하는 스크립트
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

async def analyze_new_survey_elements():
    """+ New survey 버튼과 관련 요소들을 분석"""
    print("🔍 + New survey 버튼 분석 시작...")
    
    config = get_config("dev")
    
    async with BrowserFactory.create(config) as browser_manager:
        # 로그인
        login_page = LoginPage(browser_manager.page, config)
        await login_page.navigate_to_login()
        await login_page.wait_for_page_load()
        
        space_id = "d-ge-eric"
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
                
                print("\n📋 페이지 요소 분석")
                print("-" * 50)
                
                # 모든 버튼 찾기
                buttons = await browser_manager.page.query_selector_all("button")
                print(f"📝 총 {len(buttons)}개의 버튼 발견")
                
                for i, button in enumerate(buttons):
                    try:
                        text = await button.text_content()
                        class_name = await button.get_attribute("class")
                        is_visible = await button.is_visible()
                        
                        if text and ("survey" in text.lower() or "new" in text.lower() or "+" in text):
                            print(f"🔍 버튼 {i+1}: '{text}' (class: {class_name}, visible: {is_visible})")
                    except Exception as e:
                        continue
                
                # 모든 링크 찾기
                links = await browser_manager.page.query_selector_all("a")
                print(f"\n📝 총 {len(links)}개의 링크 발견")
                
                for i, link in enumerate(links):
                    try:
                        text = await link.text_content()
                        href = await link.get_attribute("href")
                        is_visible = await link.is_visible()
                        
                        if text and ("survey" in text.lower() or "new" in text.lower() or "+" in text):
                            print(f"🔍 링크 {i+1}: '{text}' (href: {href}, visible: {is_visible})")
                    except Exception as e:
                        continue
                
                # 모든 div 요소에서 "survey" 텍스트 찾기
                divs = await browser_manager.page.query_selector_all("div")
                print(f"\n📝 총 {len(divs)}개의 div 요소 중 'survey' 텍스트 검색...")
                
                survey_elements = []
                for i, div in enumerate(divs):
                    try:
                        text = await div.text_content()
                        if text and "survey" in text.lower():
                            class_name = await div.get_attribute("class")
                            is_visible = await div.is_visible()
                            survey_elements.append({
                                "index": i+1,
                                "text": text.strip()[:100],  # 처음 100자만
                                "class": class_name,
                                "visible": is_visible
                            })
                    except Exception as e:
                        continue
                
                print(f"\n📝 'survey' 텍스트가 포함된 div 요소 {len(survey_elements)}개:")
                for elem in survey_elements[:10]:  # 처음 10개만 출력
                    print(f"🔍 Div {elem['index']}: '{elem['text']}' (class: {elem['class']}, visible: {elem['visible']})")
                
                # + New survey 버튼 클릭 시도
                print("\n📋 + New survey 버튼 클릭 시도")
                print("-" * 30)
                
                try:
                    # 수정된 셀렉터로 버튼 클릭
                    new_survey_button = await browser_manager.page.query_selector("button:has-text('New survey').el-button--primary.el-button--mini")
                    if not new_survey_button:
                        new_survey_button = await browser_manager.page.query_selector("button:has-text('New survey').create-survey-button")
                    
                    if new_survey_button:
                        await new_survey_button.click()
                        print("✅ + New survey 버튼 클릭 성공")
                        
                        # 모달이 나타날 때까지 대기
                        await asyncio.sleep(3)
                        
                        # 모달 내부 요소 분석
                        print("\n📋 New Survey 모달 내부 요소 분석")
                        print("-" * 50)
                        
                        # 모든 input 요소 찾기
                        inputs = await browser_manager.page.query_selector_all("input")
                        print(f"📝 총 {len(inputs)}개의 input 요소 발견")
                        
                        for i, input_elem in enumerate(inputs):
                            try:
                                input_type = await input_elem.get_attribute("type")
                                placeholder = await input_elem.get_attribute("placeholder")
                                value = await input_elem.get_attribute("value")
                                class_name = await input_elem.get_attribute("class")
                                is_visible = await input_elem.is_visible()
                                
                                print(f"🔍 Input {i+1}: type='{input_type}', placeholder='{placeholder}', value='{value}', class='{class_name}', visible={is_visible}")
                            except Exception as e:
                                continue
                        
                        # 모든 버튼 찾기 (모달 내부)
                        modal_buttons = await browser_manager.page.query_selector_all("button")
                        print(f"\n📝 총 {len(modal_buttons)}개의 버튼 중 모달 내부 버튼:")
                        
                        for i, button in enumerate(modal_buttons):
                            try:
                                text = await button.text_content()
                                class_name = await button.get_attribute("class")
                                is_visible = await button.is_visible()
                                
                                if text and ("add" in text.lower() or "create" in text.lower() or "cancel" in text.lower() or "save" in text.lower()):
                                    print(f"🔍 버튼 {i+1}: '{text}' (class: {class_name}, visible: {is_visible})")
                            except Exception as e:
                                continue
                        
                        # 모든 div 요소에서 "New Survey" 텍스트 찾기
                        new_survey_divs = await browser_manager.page.query_selector_all("div")
                        print(f"\n📝 'New Survey' 텍스트가 포함된 div 요소:")
                        
                        for i, div in enumerate(new_survey_divs):
                            try:
                                text = await div.text_content()
                                if text and "new survey" in text.lower():
                                    class_name = await div.get_attribute("class")
                                    is_visible = await div.is_visible()
                                    print(f"🔍 Div {i+1}: '{text.strip()[:100]}' (class: {class_name}, visible: {is_visible})")
                            except Exception as e:
                                continue
                        
                    else:
                        print("❌ + New survey 버튼을 찾을 수 없음")
                        
                except Exception as e:
                    print(f"❌ + New survey 버튼 클릭 중 오류: {e}")
                
                # 스크린샷 저장
                await browser_manager.take_screenshot("new_survey_analysis")
                print("\n📸 분석 스크린샷 저장됨")
                
            else:
                print("❌ Add Plan 모달 확인 실패")
                
        except Exception as e:
            print(f"❌ Add Plan 실행 중 오류: {e}")

if __name__ == "__main__":
    asyncio.run(analyze_new_survey_elements())
