#!/usr/bin/env python3
"""
Add plan 버튼 디버깅 스크립트
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

async def debug_add_plan_button():
    config = get_config('dev')
    
    async with BrowserFactory.create(config) as browser_manager:
        # 로그인
        login_page = LoginPage(browser_manager.page, config)
        await login_page.navigate_to_login()
        await login_page.wait_for_page_load()
        
        space_id = 'd-ge-eric'
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
        print('\n🔍 Add plan 버튼 디버깅')
        print('=' * 50)
        
        # 모든 버튼 요소 찾기
        buttons = await browser_manager.page.query_selector_all('button')
        print(f'📋 총 {len(buttons)}개의 버튼 발견')
        
        add_plan_candidates = []
        for i, button in enumerate(buttons):
            try:
                text = await button.text_content()
                classes = await button.get_attribute('class')
                visible = await button.is_visible()
                
                if text and visible and ('add' in text.lower() or 'plan' in text.lower()):
                    print(f'  🎯 후보 {len(add_plan_candidates)+1}: "{text.strip()}"')
                    print(f'     클래스: {classes}')
                    print(f'     위치: {await button.bounding_box()}')
                    print()
                    add_plan_candidates.append((text.strip(), classes, button))
                    
            except Exception as e:
                continue
        
        # el-upload 관련 요소 찾기
        print('\n🔍 el-upload 관련 요소 검색')
        print('-' * 30)
        
        upload_elements = await browser_manager.page.query_selector_all('[class*="el-upload"]')
        print(f'📋 총 {len(upload_elements)}개의 el-upload 요소 발견')
        
        for i, elem in enumerate(upload_elements):
            try:
                classes = await elem.get_attribute('class')
                visible = await elem.is_visible()
                text = await elem.text_content()
                
                print(f'  {i+1}. 클래스: {classes}')
                print(f'     텍스트: "{text.strip() if text else "N/A"}"')
                print(f'     보임: {visible}')
                print()
                
            except Exception as e:
                continue
        
        # 스크린샷 저장
        await browser_manager.page.screenshot(path='reports/dev/screenshots/add_plan_debug.png')
        print('\n📸 디버깅 스크린샷 저장: reports/dev/screenshots/add_plan_debug.png')

if __name__ == "__main__":
    asyncio.run(debug_add_plan_button())
