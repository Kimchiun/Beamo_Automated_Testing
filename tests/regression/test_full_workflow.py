#!/usr/bin/env python3
"""
Full Workflow Regression Test
Tests the complete user journey: Login → Dashboard → Site Creation → Site Detail
"""

import asyncio
from functools import wraps
import sys
from pathlib import Path

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

@timeout(45)  # 45초 타임아웃


async def test_full_workflow(environment: str = "dev"):
    """Test complete user workflow"""
    print(f"🔍 {environment.upper()} 환경 전체 워크플로우 테스트...")
    
    config = get_config(environment)
    
    async with BrowserFactory.create(config) as browser_manager:
        # 1. 로그인
        print("\n📋 1. 로그인 테스트")
        print("-" * 30)
        
        login_page = LoginPage(browser_manager.page, config)
        await login_page.navigate_to_login()
        await login_page.wait_for_page_load()
        
        space_id = "d-ge-pr"
        email = config.test_data.valid_user["email"]
        password = config.test_data.valid_user["password"]
        
        await login_page.login(space_id, email, password)
        
        if not await login_page.is_logged_in():
            print("❌ 로그인 실패")
            return False
        
        print("✅ 로그인 성공")
        
        # 2. 대시보드 기능
        print("\n📋 2. 대시보드 기능 테스트")
        print("-" * 30)
        
        dashboard_page = DashboardPage(browser_manager.page, config)
        await dashboard_page.wait_for_dashboard_load()
        
        # 사이트 개수 확인
        initial_sites_count = await dashboard_page.get_sites_count()
        print(f"📝 초기 사이트 개수: {initial_sites_count}")
        
        # 3. 사이트 생성
        print("\n📋 3. 사이트 생성 테스트")
        print("-" * 30)
        
        test_site_name = f"Regression Test Site {int(asyncio.get_event_loop().time())}"
        test_site_address = "123 Regression Street, Seoul, South Korea"
        
        success = await dashboard_page.create_site(
            site_name=test_site_name,
            address=test_site_address,
            latitude="37.5665",
            longitude="126.9780"
        )
        
        if not success:
            print("❌ 사이트 생성 실패")
            return False
        
        print("✅ 사이트 생성 성공")
        
        # 4. 사이트 상세 페이지
        print("\n📋 4. 사이트 상세 페이지 테스트")
        print("-" * 30)
        
        # 첫 번째 사이트 클릭
        await dashboard_page.click_site_by_index(0)
        await asyncio.sleep(2)
        
        site_detail_page = SiteDetailPage(browser_manager.page, config)
        await site_detail_page.wait_for_page_load()
        
        # 사이트 정보 확인
        site_name = await site_detail_page.get_site_name()
        site_address = await site_detail_page.get_site_address()
        
        print(f"📝 사이트 이름: {site_name}")
        print(f"📝 사이트 주소: {site_address}")
        
        # 측정 도구 확인
        measure_tools = await site_detail_page.get_measure_tools()
        print(f"📝 측정 도구 개수: {len(measure_tools)}")
        
        print("✅ 사이트 상세 페이지 테스트 성공")
        
        # 5. 스크린샷 저장
        print("\n📋 5. 스크린샷 저장")
        print("-" * 30)
        
        screenshot_path = await site_detail_page.take_screenshot("full_workflow_regression")
        print(f"📸 전체 워크플로우 스크린샷: {screenshot_path}")
        
        print("\n" + "=" * 60)
        print("✅ 전체 워크플로우 테스트 완료")
        print("=" * 60)
        
        return True


async def main():
    """메인 실행 함수"""
    print("🚀 전체 워크플로우 회귀 테스트 시작")
    print("=" * 60)
    
    try:
        success = await test_full_workflow("dev")
        if success:
            print("✅ 모든 테스트 통과!")
        else:
            print("❌ 일부 테스트 실패")
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 전체 워크플로우 회귀 테스트 완료")


if __name__ == "__main__":
    asyncio.run(main())
