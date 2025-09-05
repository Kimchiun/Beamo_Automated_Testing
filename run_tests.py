#!/usr/bin/env python3
"""
Main test runner for Beamo Automated Testing
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
from pages.components.global_navigation import GlobalNavigation


async def test_login():
    """Test login functionality"""
    print("🔍 로그인 테스트 시작...")
    
    config = get_config("dev")
    
    async with BrowserFactory.create(config) as browser_manager:
        login_page = LoginPage(browser_manager.page, config)
        await login_page.navigate_to_login()
        await login_page.wait_for_page_load()
        
        space_id = "d-ge-pr"
        email = config.test_data.valid_user["email"]
        password = config.test_data.valid_user["password"]
        
        await login_page.login(space_id, email, password)
        
        if await login_page.is_logged_in():
            print("✅ 로그인 테스트 성공")
            return True
        else:
            print("❌ 로그인 테스트 실패")
            return False


async def test_dashboard():
    """Test dashboard functionality"""
    print("🔍 대시보드 테스트 시작...")
    
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
            return False
        
        # 대시보드 테스트
        dashboard_page = DashboardPage(browser_manager.page, config)
        await dashboard_page.wait_for_dashboard_load()
        
        sites_count = await dashboard_page.get_sites_count()
        print(f"📝 사이트 개수: {sites_count}")
        
        print("✅ 대시보드 테스트 성공")
        return True


async def test_site_creation():
    """Test site creation functionality"""
    print("🔍 사이트 생성 테스트 시작...")
    
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
            return False
        
        # 대시보드
        dashboard_page = DashboardPage(browser_manager.page, config)
        await dashboard_page.wait_for_dashboard_load()
        
        initial_sites_count = await dashboard_page.get_sites_count()
        print(f"📝 초기 사이트 개수: {initial_sites_count}")
        
        # 사이트 생성
        test_site_name = f"Test Site {int(asyncio.get_event_loop().time())}"
        test_site_address = "123 Test Street, Seoul, South Korea"
        
        success = await dashboard_page.create_site(
            site_name=test_site_name,
            address=test_site_address,
            latitude="37.5665",
            longitude="126.9780"
        )
        
        if success:
            final_sites_count = await dashboard_page.get_sites_count()
            print(f"📝 최종 사이트 개수: {final_sites_count}")
            print("✅ 사이트 생성 테스트 성공")
            return True
        else:
            print("❌ 사이트 생성 테스트 실패")
            return False


async def test_global_navigation():
    """Test global navigation functionality"""
    print("🔍 글로벌 네비게이션 테스트 시작...")
    
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
            return False
        
        # 글로벌 네비게이션 테스트
        global_nav = GlobalNavigation(browser_manager.page, config)
        
        is_visible = await global_nav.is_visible()
        if not is_visible:
            print("❌ 글로벌 네비게이션 표시되지 않음")
            return False
        
        user_info = await global_nav.get_user_info()
        print(f"📝 사용자 정보: {user_info}")
        
        print("✅ 글로벌 네비게이션 테스트 성공")
        return True


async def test_add_plan_dialog():
    """Test Add a new plan dialog functionality"""
    print("🔍 Add a new plan 다이얼로그 테스트 시작...")
    
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
            return False
        
        # 대시보드
        dashboard_page = DashboardPage(browser_manager.page, config)
        await dashboard_page.wait_for_dashboard_load()
        
        # 사이트가 없으면 생성
        sites_count = await dashboard_page.get_sites_count()
        if sites_count == 0:
            test_site_name = f"Dialog Test Site {int(asyncio.get_event_loop().time())}"
            test_site_address = "123 Dialog Street, Seoul, South Korea"
            
            success = await dashboard_page.create_site(
                site_name=test_site_name,
                address=test_site_address,
                latitude="37.5665",
                longitude="126.9780"
            )
            
            if not success:
                print("❌ 사이트 생성 실패")
                return False
        
        # 첫 번째 사이트 클릭
        await dashboard_page.click_site_by_index(0)
        await asyncio.sleep(3)
        
        # 사이트 상세 페이지
        site_detail_page = SiteDetailPage(browser_manager.page, config)
        await site_detail_page.wait_for_page_load()
        
        # 다이얼로그 확인
        is_visible = await site_detail_page.is_add_plan_dialog_visible()
        if not is_visible:
            print("❌ Add a new plan 다이얼로그 표시되지 않음")
            return False
        
        title = await site_detail_page.get_add_plan_title()
        print(f"📝 다이얼로그 제목: {title}")
        
        print("✅ Add a new plan 다이얼로그 테스트 성공")
        return True


async def run_all_tests():
    """Run all tests"""
    print("🚀 Beamo 자동화 테스트 시작")
    print("=" * 60)
    
    tests = [
        ("로그인", test_login),
        ("대시보드", test_dashboard),
        ("사이트 생성", test_site_creation),
        ("글로벌 네비게이션", test_global_navigation),
        ("Add a new plan 다이얼로그", test_add_plan_dialog),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name} 테스트")
        print("-" * 30)
        
        try:
            success = await test_func()
            results[test_name] = "✅ 성공" if success else "❌ 실패"
        except Exception as e:
            print(f"❌ {test_name} 테스트 오류: {e}")
            results[test_name] = "❌ 오류"
    
    print("\n" + "=" * 60)
    print("📊 테스트 결과 요약")
    print("=" * 60)
    
    for test_name, result in results.items():
        print(f"{result} {test_name}")
    
    success_count = sum(1 for result in results.values() if "성공" in result)
    total_count = len(results)
    
    print(f"\n📈 성공률: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    if success_count == total_count:
        print("🎉 모든 테스트 통과!")
    else:
        print("⚠️ 일부 테스트 실패")
    
    print("=" * 60)


async def main():
    """Main function"""
    await run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
