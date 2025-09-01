#!/usr/bin/env python3
"""
Test search and site selection
"""

import asyncio
from functools import wraps
import sys
import os
from pathlib import Path

import pytest

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.config_loader import get_config
from utils.browser_manager import BrowserFactory
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.site_detail_page import SiteDetailPage


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

@pytest.mark.env('dev')
@timeout(30)  # 30초 타임아웃
async def test_search_and_site_selection(environment: str = "dev"):
    """Test search and site selection"""
    print(f"🔍 {environment.upper()} 환경 검색 및 사이트 선택 테스트...")
    
    config = get_config(environment)
    
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
            return False
        
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
            
            # 검색 실행
            await dashboard_page.search_sites(search_term)
            print("✅ 검색 실행 완료")
            
            # 검색 결과 로딩 대기
            await asyncio.sleep(3)
            
            # URL 확인
            current_url = browser_manager.page.url
            print(f"📝 검색 후 URL: {current_url}")
            
        except Exception as e:
            print(f"❌ 검색 실행 실패: {e}")
            return False
        
        # 검색 결과 확인
        print("\n📋 검색 결과 확인...")
        print("-" * 30)
        
        try:
            search_results_count = await dashboard_page.get_search_results_count()
            print(f"📝 검색 결과 개수: {search_results_count}")
            
            if search_results_count > 0:
                print("✅ 검색 결과 발견")
                
                # 첫 번째 검색 결과 정보 확인
                first_result_info = await dashboard_page.get_site_info_by_index(0)
                print(f"📝 첫 번째 검색 결과 정보: {first_result_info}")
                
                # 첫 번째 검색 결과 이름 확인
                first_result_name = await dashboard_page.get_site_name_by_index(0)
                print(f"📝 첫 번째 검색 결과 이름: '{first_result_name}'")
                
            else:
                print("❌ 검색 결과 없음")
                return False
                
        except Exception as e:
            print(f"❌ 검색 결과 확인 실패: {e}")
            return False
        
        # 검색 결과 클릭
        print("\n📋 검색 결과 클릭...")
        print("-" * 30)
        
        try:
            # 검색 결과 클릭 전 URL 확인
            before_click_url = browser_manager.page.url
            print(f"📝 클릭 전 URL: {before_click_url}")
            
            # 첫 번째 검색 결과 클릭
            await dashboard_page.click_search_result_by_index(0)
            print("✅ 첫 번째 검색 결과 클릭 성공")
            
            # 클릭 후 URL 확인
            await asyncio.sleep(3)
            after_click_url = browser_manager.page.url
            print(f"📝 클릭 후 URL: {after_click_url}")
            
            # URL 변경 확인
            if before_click_url != after_click_url:
                print("✅ 클릭 후 URL이 변경되었습니다")
            else:
                print("⚠️ 클릭 후 URL이 변경되지 않았습니다")
            
        except Exception as e:
            print(f"❌ 검색 결과 클릭 실패: {e}")
            return False
        
        # 사이트 상세 페이지에서 사이트 이름 확인
        print("\n📋 사이트 상세 페이지에서 사이트 이름 확인...")
        print("-" * 30)
        
        try:
            site_detail_page = SiteDetailPage(browser_manager.page, config)
            await site_detail_page.wait_for_page_load()
            
            # 사이트 상세 페이지에서 사이트 이름 가져오기
            detail_page_site_name = await site_detail_page.get_site_name()
            print(f"📝 상세 페이지 사이트 이름: '{detail_page_site_name}'")
            
            # 검색한 사이트 이름과 비교
            print(f"📝 검색한 사이트 이름: '{first_result_name}'")
            print(f"📝 진입한 사이트 이름: '{detail_page_site_name}'")
            
            if first_result_name == detail_page_site_name:
                print("✅ 검색한 사이트와 진입한 사이트가 동일합니다!")
            else:
                print("❌ 검색한 사이트와 진입한 사이트가 다릅니다!")
                print("⚠️ 잘못된 사이트에 진입했을 수 있습니다")
            
        except Exception as e:
            print(f"❌ 사이트 상세 페이지 이름 확인 실패: {e}")
        
        # +Add plan 버튼 클릭
        print("\n📋 +Add plan 버튼 클릭...")
        print("-" * 30)
        
        try:
            await site_detail_page.click_add_plan_button()
            print("✅ +Add plan 버튼 클릭 성공")
        except Exception as e:
            print(f"❌ +Add plan 버튼 클릭 실패: {e}")
            return False
        
        # 파일 입력 대기
        print("\n📋 파일 입력 대기...")
        print("-" * 30)
        
        try:
            await site_detail_page.wait_for_file_input()
            print("✅ 파일 입력 요소 발견")
        except Exception as e:
            print(f"❌ 파일 입력 요소 대기 실패: {e}")
            return False
        
        # 스크린샷 저장
        print("\n📋 스크린샷 저장...")
        print("-" * 30)
        
        try:
            screenshot_path = await site_detail_page.take_screenshot("search_and_site_selection", "success")
            print(f"📸 스크린샷 저장: {screenshot_path}")
        except Exception as e:
            print(f"❌ 스크린샷 저장 실패: {e}")
        
        print("\n" + "=" * 60)
        print("✅ 검색 및 사이트 선택 테스트 완료")
        print("=" * 60)
        
        return True


async def main():
    """메인 실행 함수"""
    print("🚀 검색 및 사이트 선택 테스트 시작")
    print("=" * 60)
    
    try:
        success = await test_search_and_site_selection("dev")
        if success:
            print("✅ 검색 및 사이트 선택 테스트 성공!")
        else:
            print("❌ 검색 및 사이트 선택 테스트 실패")
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 검색 및 사이트 선택 테스트 완료")


if __name__ == "__main__":
    asyncio.run(main())
