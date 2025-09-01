#!/usr/bin/env python3
"""
간단한 사이트 상세 페이지 POM 테스트
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
@timeout(37)  # 37초 타임아웃
async def test_site_detail_pom_simple(environment: str = "dev"):
    """간단한 사이트 상세 페이지 POM 테스트"""
    print(f"🔍 {environment.upper()} 환경 간단한 사이트 상세 페이지 POM 테스트...")
    
    config = get_config(environment)
    
    async with BrowserFactory.create(config) as browser_manager:
        # 로그인 페이지 생성
        login_page = LoginPage(browser_manager.page, config)
        
        # 로그인 페이지로 이동
        await login_page.navigate_to_login()
        await login_page.wait_for_page_load()
        
        # 로그인 실행
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
            
            print(f"📄 페이지 제목: {await browser_manager.page.title()}")
            print(f"🌐 URL: {browser_manager.page.url}")
            
            # 페이지 로드 대기
            await browser_manager.page.wait_for_load_state("networkidle", timeout=10000)
            
            print("\n" + "=" * 60)
            print("🔍 간단한 사이트 상세 페이지 POM 테스트")
            print("=" * 60)
            
            # 1. 페이지 새로고침
            print("\n🔄 1. 페이지 새로고침")
            print("-" * 30)
            
            await browser_manager.page.reload()
            await browser_manager.page.wait_for_load_state("networkidle", timeout=10000)
            print("✅ 페이지 새로고침 완료")
            
            # 2. 사이트 개수 확인
            print("\n📋 2. 사이트 개수 확인")
            print("-" * 30)
            
            address_elements = await browser_manager.page.query_selector_all(".building-address")
            sites_count = len(address_elements)
            print(f"📝 사이트 개수: {sites_count}")
            
            if sites_count == 0:
                print("❌ 사이트가 없습니다")
                return
            
            # 3. 첫 번째 사이트 클릭
            print("\n📋 3. 첫 번째 사이트 클릭")
            print("-" * 30)
            
            try:
                # 첫 번째 사이트 주소 확인
                first_address = await address_elements[0].text_content()
                print(f"📝 첫 번째 사이트 주소: {first_address}")
                
                # 첫 번째 사이트 클릭
                await address_elements[0].click()
                print("✅ 첫 번째 사이트 클릭 성공")
                
                # 잠시 대기
                await asyncio.sleep(3)
                
                # URL 변경 확인
                new_url = browser_manager.page.url
                print(f"🌐 새로운 URL: {new_url}")
                
                # 페이지 제목 확인
                new_title = await browser_manager.page.title()
                print(f"📄 새로운 페이지 제목: {new_title}")
                
            except Exception as e:
                print(f"❌ 사이트 클릭 실패: {e}")
                return
            
            # 4. 사이트 상세 페이지 POM 테스트
            print("\n📋 4. 사이트 상세 페이지 POM 테스트")
            print("-" * 30)
            
            # 사이트 상세 페이지 생성
            site_detail_page = SiteDetailPage(browser_manager.page, config)
            
            # 페이지 로드 확인
            is_loaded = await site_detail_page.is_page_loaded()
            print(f"📝 페이지 로드 상태: {is_loaded}")
            
            if is_loaded:
                # 페이지 정보 확인
                page_title = await site_detail_page.get_page_title()
                current_url = await site_detail_page.get_current_url()
                
                print(f"📄 페이지 제목: {page_title}")
                print(f"🌐 URL: {current_url}")
                
                # 사이트 정보 확인
                site_name = await site_detail_page.get_site_name()
                site_address = await site_detail_page.get_site_address()
                
                print(f"📝 사이트 이름: {site_name}")
                print(f"📝 사이트 주소: {site_address}")
                
                # 측정 도구 확인
                measure_tools = await site_detail_page.get_measure_tools()
                print(f"📝 측정 도구 개수: {len(measure_tools)}")
                
                # 3D 뷰어 상태 확인
                viewer_loaded = await site_detail_page.is_viewer_loaded()
                print(f"📝 3D 뷰어 로드 상태: {viewer_loaded}")
                
                # 로딩 상태 확인
                is_loading = await site_detail_page.is_loading()
                print(f"📝 현재 로딩 상태: {is_loading}")
                
                # 오류/성공 메시지 확인
                error_message = await site_detail_page.get_error_message()
                success_message = await site_detail_page.get_success_message()
                
                if error_message:
                    print(f"❌ 오류 메시지: {error_message}")
                else:
                    print("✅ 오류 메시지 없음")
                
                if success_message:
                    print(f"✅ 성공 메시지: {success_message}")
                else:
                    print("📝 성공 메시지 없음")
                
                # 스크린샷 저장
                screenshot_path = await site_detail_page.take_screenshot("site_detail_pom", "success")
                print(f"📸 사이트 상세 페이지 POM 테스트 스크린샷: {screenshot_path}")
                
            else:
                print("❌ 사이트 상세 페이지가 로드되지 않았습니다")
            
            print("\n" + "=" * 60)
            print("✅ 간단한 사이트 상세 페이지 POM 테스트 완료")
            print("=" * 60)
            
        else:
            print("❌ 로그인 실패")


async def main():
    """메인 실행 함수"""
    print("🚀 간단한 사이트 상세 페이지 POM 테스트 시작")
    print("=" * 60)
    
    try:
        await test_site_detail_pom_simple("dev")
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 간단한 사이트 상세 페이지 POM 테스트 완료")


if __name__ == "__main__":
    asyncio.run(main())
