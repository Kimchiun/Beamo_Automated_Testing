#!/usr/bin/env python3
"""
Cross Environment Integration Test
Tests the same functionality across different environments (dev, stage, live)
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

@timeout(30)  # 30초 타임아웃


async def test_login_across_environments():
    """Test login functionality across all environments"""
    print("🔍 환경 간 로그인 통합 테스트...")
    
    environments = ["dev", "stage", "live"]
    results = {}
    
    for env in environments:
        print(f"\n📋 {env.upper()} 환경 테스트")
        print("-" * 30)
        
        try:
            config = get_config(env)
            
            async with BrowserFactory.create(config) as browser_manager:
                login_page = LoginPage(browser_manager.page, config)
                await login_page.navigate_to_login()
                await login_page.wait_for_page_load()
                
                # 로그인 시도
                space_id = "d-ge-ro"  # Dev 환경용 Space ID
                email = config.test_data.valid_user["email"]
                password = config.test_data.valid_user["password"]
                
                await login_page.login(space_id, email, password)
                
                if await login_page.is_logged_in():
                    print(f"✅ {env.upper()} 환경 로그인 성공")
                    results[env] = "SUCCESS"
                else:
                    print(f"❌ {env.upper()} 환경 로그인 실패")
                    results[env] = "FAILED"
                    
        except Exception as e:
            print(f"❌ {env.upper()} 환경 테스트 오류: {e}")
            results[env] = "ERROR"
    
    # 결과 요약
    print("\n" + "=" * 60)
    print("📊 환경 간 테스트 결과 요약")
    print("=" * 60)
    
    for env, result in results.items():
        status_emoji = "✅" if result == "SUCCESS" else "❌"
        print(f"{status_emoji} {env.upper()}: {result}")
    
    return results


async def main():
    """메인 실행 함수"""
    print("🚀 환경 간 통합 테스트 시작")
    print("=" * 60)
    
    try:
        results = await test_login_across_environments()
        
        # 전체 결과 확인
        all_success = all(result == "SUCCESS" for result in results.values())
        
        if all_success:
            print("\n🎉 모든 환경에서 테스트 통과!")
        else:
            print("\n⚠️ 일부 환경에서 테스트 실패")
            
    except Exception as e:
        print(f"❌ 통합 테스트 실패: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 환경 간 통합 테스트 완료")


if __name__ == "__main__":
    asyncio.run(main())
