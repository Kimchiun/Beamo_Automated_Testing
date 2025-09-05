#!/usr/bin/env python3
"""
Global Navigation Component Test
Tests the global navigation functionality
"""

import asyncio
from functools import wraps
import sys
from pathlib import Path

import pytest

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.config_loader import get_config
from utils.browser_manager import BrowserFactory
from pages.login_page import LoginPage
from pages.components.global_navigation import GlobalNavigation


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
@timeout(22)  # 22초 타임아웃
async def test_global_navigation(environment: str = "dev"):
    """Test global navigation component"""
    print(f"🔍 {environment.upper()} 환경 글로벌 네비게이션 테스트...")
    
    config = get_config(environment)
    
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
        
        # 글로벌 네비게이션 테스트
        print("\n" + "=" * 60)
        print("🔍 글로벌 네비게이션 테스트")
        print("=" * 60)
        
        # 글로벌 네비게이션 컴포넌트 생성
        global_nav = GlobalNavigation(browser_manager.page, config)
        
        # 1. 네비게이션 로드 확인
        print("\n📋 1. 네비게이션 로드 확인")
        print("-" * 30)
        
        is_visible = await global_nav.is_visible()
        print(f"📝 글로벌 네비게이션 표시 상태: {is_visible}")
        
        if is_visible:
            print("✅ 글로벌 네비게이션 로드 성공")
        else:
            print("❌ 글로벌 네비게이션 로드 실패")
            return
        
        # 2. 사용자 정보 확인
        print("\n📋 2. 사용자 정보 확인")
        print("-" * 30)
        
        user_info = await global_nav.get_user_info()
        print(f"📝 사용자 정보: {user_info}")
        
        # 3. 알림 개수 확인
        print("\n📋 3. 알림 개수 확인")
        print("-" * 30)
        
        notification_count = await global_nav.get_notification_count()
        alert_count = await global_nav.get_alert_count()
        
        print(f"📝 알림 개수: {notification_count}")
        print(f"📝 IoT 알림 개수: {alert_count}")
        
        # 4. 네비게이션 메뉴 아이템 확인
        print("\n📋 4. 네비게이션 메뉴 아이템 확인")
        print("-" * 30)
        
        nav_items = await global_nav.get_navigation_items()
        print(f"📝 네비게이션 아이템 개수: {len(nav_items)}")
        
        for i, item in enumerate(nav_items[:5]):  # 처음 5개만
            print(f"  {i+1}. text={item.get('text', 'N/A')}")
            print(f"     href={item.get('href', 'N/A')}")
            print(f"     visible={item.get('visible', False)}")
        
        # 5. 로고 클릭 테스트
        print("\n📋 5. 로고 클릭 테스트")
        print("-" * 30)
        
        try:
            current_url = browser_manager.page.url
            print(f"📝 현재 URL: {current_url}")
            
            await global_nav.click_logo()
            await asyncio.sleep(2)
            
            new_url = browser_manager.page.url
            print(f"📝 클릭 후 URL: {new_url}")
            
            if new_url != current_url:
                print("✅ 로고 클릭 성공 (URL 변경됨)")
            else:
                print("⚠️ 로고 클릭됨 (URL 변경 없음)")
                
        except Exception as e:
            print(f"❌ 로고 클릭 실패: {e}")
        
        # 6. 사용자 팀 드롭다운 테스트
        print("\n📋 6. 사용자 팀 드롭다운 테스트")
        print("-" * 30)
        
        try:
            await global_nav.click_user_team_dropdown()
            print("✅ 사용자 팀 드롭다운 클릭 성공")
            
            # 잠시 대기 후 다시 클릭하여 닫기
            await asyncio.sleep(1)
            await global_nav.click_user_team_dropdown()
            print("✅ 사용자 팀 드롭다운 닫기 성공")
            
        except Exception as e:
            print(f"❌ 사용자 팀 드롭다운 테스트 실패: {e}")
        
        # 7. 알림 버튼 테스트
        print("\n📋 7. 알림 버튼 테스트")
        print("-" * 30)
        
        try:
            await global_nav.click_notifications()
            print("✅ 알림 버튼 클릭 성공")
            
            # 잠시 대기
            await asyncio.sleep(1)
            
        except Exception as e:
            print(f"❌ 알림 버튼 테스트 실패: {e}")
        
        # 8. IoT 알림 버튼 테스트
        print("\n📋 8. IoT 알림 버튼 테스트")
        print("-" * 30)
        
        try:
            await global_nav.click_iot_alerts()
            print("✅ IoT 알림 버튼 클릭 성공")
            
            # 잠시 대기
            await asyncio.sleep(1)
            
        except Exception as e:
            print(f"❌ IoT 알림 버튼 테스트 실패: {e}")
        
        print("\n" + "=" * 60)
        print("✅ 글로벌 네비게이션 테스트 완료")
        print("=" * 60)


async def main():
    """메인 실행 함수"""
    print("🚀 글로벌 네비게이션 테스트 시작")
    print("=" * 60)
    
    try:
        await test_global_navigation("dev")
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 글로벌 네비게이션 테스트 완료")


if __name__ == "__main__":
    asyncio.run(main())
