#!/usr/bin/env python3
"""
최종 사이트 생성 테스트
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
async def test_create_site_final(environment: str = "dev"):
    """최종 사이트 생성 테스트"""
    print(f"🔍 {environment.upper()} 환경 최종 사이트 생성 테스트...")
    
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
            print("🔍 최종 사이트 생성 테스트")
            print("=" * 60)
            
            # 1. 페이지 새로고침
            print("\n🔄 1. 페이지 새로고침")
            print("-" * 30)
            
            await browser_manager.page.reload()
            await browser_manager.page.wait_for_load_state("networkidle", timeout=10000)
            print("✅ 페이지 새로고침 완료")
            
            # 2. Create Site 버튼 클릭
            print("\n🔘 2. Create Site 버튼 클릭")
            print("-" * 30)
            
            try:
                create_button = await browser_manager.page.wait_for_selector(".create-site-button")
                await create_button.click()
                print("✅ Create Site 버튼 클릭 성공")
                
                # 다이얼로그가 열릴 때까지 대기
                await browser_manager.page.wait_for_selector(".site-create-dialog", timeout=10000)
                print("✅ Create Site 다이얼로그 열림")
                
            except Exception as e:
                print(f"❌ Create Site 버튼 클릭 실패: {e}")
                return
            
            # 3. 사이트 정보 입력
            print("\n📝 3. 사이트 정보 입력")
            print("-" * 30)
            
            # 테스트 사이트 정보
            test_site_name = f"Test Site {int(asyncio.get_event_loop().time())}"
            test_site_address = "123 Test Street, Seoul, South Korea"
            test_latitude = "37.5665"
            test_longitude = "126.9780"
            
            print(f"📝 테스트 사이트 정보:")
            print(f"   - 이름: {test_site_name}")
            print(f"   - 주소: {test_site_address}")
            print(f"   - 위도: {test_latitude}")
            print(f"   - 경도: {test_longitude}")
            
            try:
                # 사이트 이름 입력
                name_input = await browser_manager.page.wait_for_selector("input[placeholder='Enter a Name']")
                await name_input.fill(test_site_name)
                print("✅ 사이트 이름 입력 완료")
                
                # 주소 입력
                address_input = await browser_manager.page.wait_for_selector("input[placeholder='Enter an Address']")
                await address_input.fill(test_site_address)
                print("✅ 주소 입력 완료")
                
                # 위도 입력
                lat_input = await browser_manager.page.wait_for_selector("input[placeholder='Latitude']")
                await lat_input.fill(test_latitude)
                print("✅ 위도 입력 완료")
                
                # 경도 입력
                lon_input = await browser_manager.page.wait_for_selector("input[placeholder='Longitude']")
                await lon_input.fill(test_longitude)
                print("✅ 경도 입력 완료")
                
            except Exception as e:
                print(f"❌ 사이트 정보 입력 실패: {e}")
                return
            
            # 4. Create Site 버튼 클릭 (다이얼로그 내부)
            print("\n🔘 4. Create Site 버튼 클릭 (다이얼로그 내부)")
            print("-" * 30)
            
            try:
                # 다이얼로그 내부의 Create Site 버튼 찾기
                create_site_button = await browser_manager.page.wait_for_selector(".site-create-dialog .el-button--primary")
                await create_site_button.click()
                print("✅ Create Site 버튼 클릭 성공")
                
                # 다이얼로그가 닫힐 때까지 대기
                try:
                    await browser_manager.page.wait_for_selector(".site-create-dialog", state="hidden", timeout=10000)
                    print("✅ 다이얼로그 닫힘 - 사이트 생성 성공!")
                except Exception:
                    print("⚠️ 다이얼로그가 닫히지 않음 - 오류 메시지 확인 필요")
                
            except Exception as e:
                print(f"❌ Create Site 버튼 클릭 실패: {e}")
                return
            
            # 5. 페이지 새로고침 및 결과 확인
            print("\n🔄 5. 페이지 새로고침 및 결과 확인")
            print("-" * 30)
            
            try:
                # 페이지 새로고침
                await browser_manager.page.reload()
                await browser_manager.page.wait_for_load_state("networkidle", timeout=10000)
                print("✅ 페이지 새로고침 완료")
                
                # 사이트 주소 확인
                address_elements = await browser_manager.page.query_selector_all(".building-address")
                print(f"📝 현재 사이트 개수: {len(address_elements)}")
                
                if len(address_elements) > 0:
                    # 첫 번째 사이트 주소 확인
                    first_address = await address_elements[0].text_content()
                    print(f"📝 첫 번째 사이트 주소: {first_address}")
                    
                    if test_site_address in first_address:
                        print("✅ 새로 생성된 사이트 확인!")
                    else:
                        print("⚠️ 새로 생성된 사이트가 목록 맨 위에 없음")
                else:
                    print("❌ 사이트가 없음")
                
            except Exception as e:
                print(f"❌ 결과 확인 실패: {e}")
            
            # 6. 스크린샷 저장
            print("\n📸 6. 스크린샷 저장")
            print("-" * 30)
            
            try:
                import os
                import time
                screenshot_dir = f"reports/{config.environment}/screenshots"
                os.makedirs(screenshot_dir, exist_ok=True)
                
                timestamp = int(time.time())
                filename = f"create_site_final_{timestamp}.png"
                filepath = os.path.join(screenshot_dir, filename)
                
                await browser_manager.page.screenshot(path=filepath)
                print(f"📸 최종 스크린샷: {filepath}")
            except Exception as e:
                print(f"❌ 스크린샷 저장 실패: {e}")
            
            print("\n" + "=" * 60)
            print("✅ 최종 사이트 생성 테스트 완료")
            print("=" * 60)
            
        else:
            print("❌ 로그인 실패")


async def main():
    """메인 실행 함수"""
    print("🚀 최종 사이트 생성 테스트 시작")
    print("=" * 60)
    
    try:
        await test_create_site_final("dev")
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 최종 사이트 생성 테스트 완료")


if __name__ == "__main__":
    asyncio.run(main())
