#!/usr/bin/env python3
"""
Analyze search click behavior
"""

import asyncio
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.config_loader import get_config
from utils.browser_manager import BrowserFactory
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


async def analyze_search_click_behavior():
    """Analyze search click behavior"""
    print("🔍 검색 결과 클릭 동작 분석...")
    
    config = get_config("dev")
    
    async with BrowserFactory.create(config) as browser_manager:
        # 로그인
        login_page = LoginPage(browser_manager.page, config)
        await login_page.navigate_to_login()
        await login_page.wait_for_page_load()
        
        space_id = "d-ge-ro"
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
        
        # 검색 실행
        print("\n📋 검색 실행...")
        print("-" * 30)
        
        try:
            search_term = "Simple Search Test"
            print(f"📝 검색어: {search_term}")
            
            await dashboard_page.search_sites(search_term)
            print("✅ 검색 실행 완료")
            await asyncio.sleep(3)
            
        except Exception as e:
            print(f"❌ 검색 실행 실패: {e}")
            return
        
        # 클릭 전 상태 확인
        print("\n📋 클릭 전 상태 확인...")
        print("-" * 30)
        
        try:
            # 현재 URL 확인
            before_url = browser_manager.page.url
            print(f"📝 클릭 전 URL: {before_url}")
            
            # 검색 결과 개수 확인
            results = await browser_manager.page.query_selector_all(".building")
            print(f"📝 검색 결과 개수: {len(results)}")
            
            if len(results) > 0:
                # 첫 번째 검색 결과 정보 확인
                first_result = results[0]
                
                # 사이트 이름 확인
                site_name_element = await first_result.query_selector(".building-name")
                if site_name_element:
                    site_name = await site_name_element.text_content()
                    print(f"📝 클릭할 사이트 이름: '{site_name}'")
                
                # 클릭 전 페이지 제목 확인
                page_title = await browser_manager.page.title()
                print(f"📝 클릭 전 페이지 제목: {page_title}")
                
            else:
                print("❌ 검색 결과를 찾을 수 없습니다")
                return
                
        except Exception as e:
            print(f"❌ 클릭 전 상태 확인 실패: {e}")
            return
        
        # 검색 결과 클릭
        print("\n📋 검색 결과 클릭...")
        print("-" * 30)
        
        try:
            # 클릭 실행
            await first_result.click()
            print("✅ 검색 결과 클릭 완료")
            
            # 클릭 후 대기
            await asyncio.sleep(3)
            
        except Exception as e:
            print(f"❌ 검색 결과 클릭 실패: {e}")
            return
        
        # 클릭 후 상태 확인
        print("\n📋 클릭 후 상태 확인...")
        print("-" * 30)
        
        try:
            # URL 변경 확인
            after_url = browser_manager.page.url
            print(f"📝 클릭 후 URL: {after_url}")
            
            if before_url != after_url:
                print("✅ URL이 변경되었습니다!")
            else:
                print("⚠️ URL이 변경되지 않았습니다")
            
            # 페이지 제목 변경 확인
            after_page_title = await browser_manager.page.title()
            print(f"📝 클릭 후 페이지 제목: {after_page_title}")
            
            if page_title != after_page_title:
                print("✅ 페이지 제목이 변경되었습니다!")
            else:
                print("⚠️ 페이지 제목이 변경되지 않았습니다")
            
            # 현재 페이지의 주요 요소들 확인
            print("\n📋 현재 페이지 요소 확인...")
            
            # 사이트 이름 요소 확인
            current_site_name = await browser_manager.page.query_selector(".site-name, .building-name, h1, h2")
            if current_site_name:
                current_site_name_text = await current_site_name.text_content()
                print(f"📝 현재 페이지 사이트 이름: '{current_site_name_text}'")
            else:
                print("📝 현재 페이지에서 사이트 이름을 찾을 수 없습니다")
            
            # +Add plan 버튼 확인
            add_plan_button = await browser_manager.page.query_selector("button:has-text('Add plan'), button:has-text('+Add plan'), button:has-text('+ Add plan')")
            if add_plan_button:
                print("✅ +Add plan 버튼 발견!")
            else:
                print("❌ +Add plan 버튼을 찾을 수 없습니다")
            
            # URL 경로 분석
            if "/list" in after_url:
                print("📝 여전히 사이트 목록 페이지(/list)에 있습니다")
            elif "/site/" in after_url or "/building/" in after_url:
                print("📝 사이트 상세 페이지로 이동했습니다!")
            else:
                print(f"📝 다른 페이지로 이동했습니다: {after_url}")
            
        except Exception as e:
            print(f"❌ 클릭 후 상태 확인 실패: {e}")
        
        # 스크린샷 저장
        print("\n📋 스크린샷 저장...")
        print("-" * 30)
        
        try:
            screenshot_path = await browser_manager.take_screenshot("search_click_behavior_analysis")
            print(f"📸 스크린샷 저장: {screenshot_path}")
        except Exception as e:
            print(f"❌ 스크린샷 저장 실패: {e}")
        
        print("\n" + "=" * 60)
        print("✅ 검색 결과 클릭 동작 분석 완료")
        print("=" * 60)


async def main():
    """메인 실행 함수"""
    print("🚀 검색 결과 클릭 동작 분석 시작")
    print("=" * 60)
    
    try:
        await analyze_search_click_behavior()
    except Exception as e:
        print(f"❌ 분석 실패: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 검색 결과 클릭 동작 분석 완료")


if __name__ == "__main__":
    asyncio.run(main())
