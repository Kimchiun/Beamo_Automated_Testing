#!/usr/bin/env python3
"""
사이트 상세 페이지 요소 분석 스크립트
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

async def analyze_site_detail_elements():
    config = get_config('dev')
    
    async with BrowserFactory.create(config) as browser_manager:
        # 로그인
        login_page = LoginPage(browser_manager.page, config)
        await login_page.navigate_to_login()
        await login_page.wait_for_page_load()
        
        space_id = 'd-ge-ro'
        email = config.test_data.valid_user['email']
        password = config.test_data.valid_user['password']
        
        await login_page.login(space_id, email, password)
        
        if not await login_page.is_logged_in():
            print('❌ 로그인 실패')
            return
        
        print('✅ 로그인 성공')
        
        # 대시보드로 이동
        dashboard_page = DashboardPage(browser_manager.page, config)
        await dashboard_page.wait_for_dashboard_load()
        
        # 사이트 클릭
        site_click_success = await dashboard_page.click_first_available_site()
        if not site_click_success:
            print('❌ 사이트 클릭 실패')
            return
        
        print('✅ 사이트 클릭 성공!')
        await asyncio.sleep(3)
        
        # 페이지 요소 분석
        print('\n🔍 사이트 상세 페이지 요소 분석')
        print('=' * 50)
        
        # 모든 버튼 요소 찾기
        buttons = await browser_manager.page.query_selector_all('button')
        print(f'📋 총 {len(buttons)}개의 버튼 발견')
        
        for i, button in enumerate(buttons):
            try:
                text = await button.text_content()
                classes = await button.get_attribute('class')
                visible = await button.is_visible()
                
                if text and visible:
                    print(f'  {i+1}. 버튼 텍스트: "{text.strip()}"')
                    print(f'     클래스: {classes}')
                    print(f'     위치: {await button.bounding_box()}')
                    print()
            except Exception as e:
                continue
        
        # Add plan 관련 요소 찾기
        print('🔍 Add plan 관련 요소 검색')
        print('-' * 30)
        
        add_plan_selectors = [
            'button:has-text("+ Add plan")',
            'button:has-text("+Add plan")', 
            'button:has-text("Add plan")',
            '.el-button--primary:has-text("+ Add plan")',
            '[class*="add-plan"]',
            '[class*="add_plan"]'
        ]
        
        for selector in add_plan_selectors:
            try:
                elements = await browser_manager.page.query_selector_all(selector)
                if elements:
                    print(f'✅ 셀렉터 "{selector}"로 {len(elements)}개 요소 발견')
                    for j, elem in enumerate(elements):
                        text = await elem.text_content()
                        classes = await elem.get_attribute('class')
                        visible = await elem.is_visible()
                        print(f'   {j+1}. 텍스트: "{text.strip()}", 클래스: {classes}, 보임: {visible}')
                else:
                    print(f'❌ 셀렉터 "{selector}"로 요소 없음')
            except Exception as e:
                print(f'❌ 셀렉터 "{selector}" 오류: {e}')
        
        # 갤러리 관련 요소 찾기
        print('\n🔍 갤러리 관련 요소 검색')
        print('-' * 30)
        
        gallery_selectors = [
            '[class*="gallery"]',
            '[class*="camera"]',
            'button[class*="upload"]',
            'input[type="file"]'
        ]
        
        for selector in gallery_selectors:
            try:
                elements = await browser_manager.page.query_selector_all(selector)
                if elements:
                    print(f'✅ 셀렉터 "{selector}"로 {len(elements)}개 요소 발견')
                    for j, elem in enumerate(elements):
                        if elem.tag_name == 'button':
                            text = await elem.text_content()
                            classes = await elem.get_attribute('class')
                            visible = await elem.is_visible()
                            print(f'   {j+1}. 버튼 텍스트: "{text.strip()}", 클래스: {classes}, 보임: {visible}')
                        elif elem.tag_name == 'input':
                            accept = await elem.get_attribute('accept')
                            classes = await elem.get_attribute('class')
                            visible = await elem.is_visible()
                            print(f'   {j+1}. 파일 입력, accept: {accept}, 클래스: {classes}, 보임: {visible}')
            except Exception as e:
                print(f'❌ 셀렉터 "{selector}" 오류: {e}')
        
        # 스크린샷 저장
        await browser_manager.page.screenshot(path='reports/dev/screenshots/site_detail_analysis.png')
        print('\n📸 분석 스크린샷 저장: reports/dev/screenshots/site_detail_analysis.png')

if __name__ == "__main__":
    asyncio.run(analyze_site_detail_elements())
