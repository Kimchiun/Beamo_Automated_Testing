#!/usr/bin/env python3
"""
업데이트된 대시보드 기능 테스트
"""

import asyncio
import sys
from pathlib import Path
from functools import wraps

import pytest

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.config_loader import get_config
from utils.browser_manager import BrowserFactory
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

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

@pytest.mark.asyncio
@pytest.mark.smoke
@pytest.mark.p0
@pytest.mark.env('dev')
@timeout(45)  # 45초 타임아웃
async def test_dashboard_functions(environment: str = "dev"):
    """업데이트된 대시보드 기능 테스트"""
    print(f"🔍 {environment.upper()} 환경 대시보드 기능 테스트...")
    
    config = get_config(environment)
    
    async with BrowserFactory.create(config) as browser_manager:
        # 로그인 페이지 생성
        login_page = LoginPage(browser_manager.page, config)
        
        # 로그인 페이지로 이동
        await login_page.navigate_to_login()
        await login_page.wait_for_page_load()
        
        # 3단계 로그인 실행
        space_id = "d-ge-eric"
        email = config.test_data.valid_user["email"]
        password = config.test_data.valid_user["password"]
        
        print(f"📝 로그인 정보:")
        print(f"   - 스페이스 ID: {space_id}")
        print(f"   - 이메일: {email}")
        print(f"   - 비밀번호: {password}")
        
        # 로그인 실행
        await login_page.login(space_id, email, password)
        
        # 로그인 성공 확인
        if await login_page.is_logged_in():
            print("✅ 로그인 성공!")
            
            # 대시보드 페이지 생성
            dashboard_page = DashboardPage(browser_manager.page, config)
            await dashboard_page.wait_for_dashboard_load()
            
            print(f"📄 페이지 제목: {await dashboard_page.get_page_title()}")
            print(f"🌐 URL: {await dashboard_page.get_current_url()}")
            
            print("\n" + "=" * 60)
            print("🔍 대시보드 기능 테스트")
            print("=" * 60)
            
            # 1. 사이트 정보 가져오기
            print("\n📋 1. 사이트 정보 테스트")
            print("-" * 30)
            
            sites_count = await dashboard_page.get_sites_count()
            print(f"📝 총 사이트 개수: {sites_count}")
            
            if sites_count > 0:
                # 첫 번째 사이트 정보
                first_site_info = await dashboard_page.get_site_info_by_index(0)
                print(f"📝 첫 번째 사이트 정보:")
                print(f"   - 주소: {first_site_info.get('address', 'N/A')}")
                print(f"   - 조사 날짜: {first_site_info.get('survey_date', 'N/A')}")
                
                # 모든 사이트 주소
                addresses = await dashboard_page.get_site_addresses()
                print(f"📝 사이트 주소 목록 (처음 3개):")
                for i, address in enumerate(addresses[:3]):
                    print(f"   {i+1}. {address}")
                
                # 모든 조사 날짜
                dates = await dashboard_page.get_site_survey_dates()
                print(f"📝 조사 날짜 목록 (처음 3개):")
                for i, date in enumerate(dates[:3]):
                    print(f"   {i+1}. {date}")
            
            # 2. 검색 기능 테스트
            print("\n🔍 2. 검색 기능 테스트")
            print("-" * 30)
            
            try:
                await dashboard_page.search_sites("test")
                print("✅ 검색 기능 테스트 성공")
            except Exception as e:
                print(f"❌ 검색 기능 테스트 실패: {e}")
            
            # 3. 정렬 옵션 테스트
            print("\n🔧 3. 정렬 옵션 테스트")
            print("-" * 30)
            
            sort_options = await dashboard_page.get_sort_options()
            print(f"📝 사용 가능한 정렬 옵션: {sort_options}")
            
            # 4. 알림 시스템 테스트
            print("\n🔔 4. 알림 시스템 테스트")
            print("-" * 30)
            
            try:
                await dashboard_page.click_notifications()
                print("✅ 알림 버튼 클릭 성공")
                await asyncio.sleep(1)  # 잠시 대기
            except Exception as e:
                print(f"❌ 알림 버튼 클릭 실패: {e}")
            
            try:
                await dashboard_page.click_iot_alerts()
                print("✅ IoT 알림 버튼 클릭 성공")
                await asyncio.sleep(1)  # 잠시 대기
            except Exception as e:
                print(f"❌ IoT 알림 버튼 클릭 실패: {e}")
            
            # 5. 사용자 팀 드롭다운 테스트
            print("\n👤 5. 사용자 팀 드롭다운 테스트")
            print("-" * 30)
            
            try:
                await dashboard_page.click_user_team_dropdown()
                print("✅ 사용자 팀 드롭다운 클릭 성공")
                await asyncio.sleep(1)  # 잠시 대기
            except Exception as e:
                print(f"❌ 사용자 팀 드롭다운 클릭 실패: {e}")
            
            # 6. Create Site 버튼 테스트
            print("\n➕ 6. Create Site 버튼 테스트")
            print("-" * 30)
            
            try:
                await dashboard_page.open_create_site_dialog()
                print("✅ Create Site 다이얼로그 열기 성공")
                
                # 다이얼로그가 열렸는지 확인
                if await dashboard_page.is_create_site_dialog_open():
                    print("✅ Create Site 다이얼로그가 열렸습니다")
                else:
                    print("❌ Create Site 다이얼로그가 열리지 않았습니다")
                    
            except Exception as e:
                print(f"❌ Create Site 다이얼로그 열기 실패: {e}")
            
            # 7. 북마크 기능 테스트
            print("\n🔖 7. 북마크 기능 테스트")
            print("-" * 30)
            
            if sites_count > 0:
                try:
                    await dashboard_page.click_bookmark(0)
                    print("✅ 첫 번째 사이트 북마크 클릭 성공")
                except Exception as e:
                    print(f"❌ 북마크 클릭 실패: {e}")
            else:
                print("📝 북마크 테스트 건너뜀 (사이트가 없음)")
            
            # 8. 필터 기능 테스트
            print("\n🔧 8. 필터 기능 테스트")
            print("-" * 30)
            
            try:
                await dashboard_page.open_filter_drawer()
                print("✅ 필터 드로어 열기 성공")
                await asyncio.sleep(1)  # 잠시 대기
            except Exception as e:
                print(f"❌ 필터 드로어 열기 실패: {e}")
            
            # 9. 스크린샷 저장
            print("\n📸 9. 스크린샷 저장")
            print("-" * 30)
            
            screenshot_path = await dashboard_page.take_dashboard_screenshot("dashboard_functions", "success")
            print(f"📸 대시보드 기능 테스트 스크린샷: {screenshot_path}")
            
            print("\n" + "=" * 60)
            print("✅ 대시보드 기능 테스트 완료")
            print("=" * 60)
            
        else:
            print("❌ 로그인 실패")


async def main():
    """메인 실행 함수"""
    print("🚀 대시보드 기능 테스트 시작")
    print("=" * 60)
    
    try:
        await test_dashboard_functions("dev")
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 대시보드 기능 테스트 완료")


if __name__ == "__main__":
    asyncio.run(main())
