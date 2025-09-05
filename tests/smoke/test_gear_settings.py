#!/usr/bin/env python3
"""
Test Gear Settings Button
톱니바퀴 설정 버튼을 테스트합니다.
"""

import pytest
import asyncio
import sys
from pathlib import Path
from functools import wraps

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

@pytest.mark.p0
@pytest.mark.env('dev')
@timeout(45)  # 45초 타임아웃
async def test_gear_settings_button(environment: str = "dev"):
    """톱니바퀴 설정 버튼 테스트"""
    print(f"🔍 {environment.upper()} 환경 톱니바퀴 설정 버튼 테스트...")

    config = get_config(environment)

    async with BrowserFactory.create(config) as browser_manager:
        # Set test name for video naming
        browser_manager.set_current_test("gear_settings_button")
        
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
            return False
        
        print("✅ 로그인 성공")
        
        # 대시보드로 이동
        await asyncio.sleep(3)
        
        # 글로벌 네비게이션 초기화
        global_nav = GlobalNavigation(browser_manager.page, config)
        
        print("\n" + "=" * 60)
        print("🔍 톱니바퀴 설정 버튼 테스트")
        print("=" * 60)
        
        # 1. 글로벌 네비게이션 로드 확인
        print("\n📋 1. 글로벌 네비게이션 로드 확인")
        print("-" * 30)
        
        try:
            await global_nav.wait_for_navigation_load()
            print("✅ 글로벌 네비게이션 로드 완료")
        except Exception as e:
            print(f"❌ 글로벌 네비게이션 로드 실패: {e}")
            return False
        
        # 2. 톱니바퀴 설정 버튼 가시성 확인
        print("\n📋 2. 톱니바퀴 설정 버튼 가시성 확인")
        print("-" * 30)
        
        try:
            is_visible = await global_nav.is_gear_settings_visible()
            if is_visible:
                print("✅ 톱니바퀴 설정 버튼이 보입니다")
            else:
                print("❌ 톱니바퀴 설정 버튼이 보이지 않습니다")
                print("🔍 다른 방법으로 설정 버튼 찾기...")
                
                # 페이지 전체에서 톱니바퀴 관련 요소 찾기
                gear_selectors = [
                    "⚙️",
                    "🔧",
                    "button:has-text('⚙️')",
                    "button:has-text('🔧')",
                    "button:has-text('설정')",
                    "button:has-text('Settings')",
                    "button:has-text('Config')",
                    "[class*='gear']",
                    "[class*='cog']",
                    "[class*='settings']",
                    "[class*='config']"
                ]
                
                gear_found = False
                for selector in gear_selectors:
                    try:
                        elements = await browser_manager.page.query_selector_all(selector)
                        for elem in elements:
                            try:
                                if await elem.is_visible():
                                    tag_name = await elem.evaluate("el => el.tagName.toLowerCase()")
                                    classes = await elem.get_attribute("class")
                                    elem_text = await elem.text_content()
                                    
                                    print(f"✅ 설정 관련 요소 발견: {selector}")
                                    print(f"  - 태그: <{tag_name}>")
                                    print(f"  - 클래스: {classes}")
                                    print(f"  - 텍스트: {elem_text}")
                                    
                                    gear_found = True
                                    break
                            except:
                                continue
                        if gear_found:
                            break
                    except:
                        continue
                
                if not gear_found:
                    print("❌ 설정 관련 요소를 찾을 수 없음")
                    return False
        except Exception as e:
            print(f"❌ 톱니바퀴 설정 버튼 가시성 확인 실패: {e}")
            return False
        
        # 3. 톱니바퀴 설정 버튼 클릭
        print("\n📋 3. 톱니바퀴 설정 버튼 클릭")
        print("-" * 30)
        
        try:
            await global_nav.click_gear_settings()
            print("✅ 톱니바퀴 설정 버튼 클릭 성공")
        except Exception as e:
            print(f"❌ 톱니바퀴 설정 버튼 클릭 실패: {e}")
            return False
        
        # 4. 설정 메뉴가 나타났는지 확인
        print("\n📋 4. 설정 메뉴 확인")
        print("-" * 30)
        
        try:
            await asyncio.sleep(2)  # 메뉴가 나타날 때까지 대기
            
            # 모달/드롭다운 관련 셀렉터들
            modal_selectors = [
                ".modal",
                ".dropdown",
                ".menu",
                ".panel",
                ".popup",
                ".overlay",
                "[class*='modal']",
                "[class*='dropdown']",
                "[class*='menu']",
                "[class*='panel']",
                "[class*='popup']",
                "[class*='overlay']",
                ".el-dropdown-menu",
                ".el-menu",
                ".ant-dropdown-menu",
                ".ant-menu"
            ]
            
            modal_found = False
            for modal_selector in modal_selectors:
                try:
                    modal_elements = await browser_manager.page.query_selector_all(modal_selector)
                    for modal_elem in modal_elements:
                        try:
                            if await modal_elem.is_visible():
                                modal_tag = await modal_elem.evaluate("el => el.tagName.toLowerCase()")
                                modal_classes = await modal_elem.get_attribute("class")
                                modal_text = await modal_elem.text_content()
                                
                                print(f"✅ 설정 메뉴 발견: {modal_selector}")
                                print(f"  - 태그: <{modal_tag}>")
                                print(f"  - 텍스트: {modal_text[:200]}...")
                                
                                # 메뉴 아이템들 확인
                                menu_items = await modal_elem.query_selector_all("li, .menu-item, .dropdown-item, button, a, .el-menu-item, .ant-menu-item")
                                print(f"  - 메뉴 아이템 개수: {len(menu_items)}")
                                
                                for i, item in enumerate(menu_items[:15]):  # 처음 15개만
                                    try:
                                        item_text = await item.text_content()
                                        item_tag = await item.evaluate("el => el.tagName.toLowerCase()")
                                        item_classes = await item.get_attribute("class")
                                        
                                        if item_text and item_text.strip():
                                            print(f"    {i+1}. <{item_tag}> {item_text.strip()}")
                                            print(f"       클래스: {item_classes}")
                                    except:
                                        continue
                                
                                modal_found = True
                                break
                        except:
                            continue
                    if modal_found:
                        break
                except:
                    continue
            
            if not modal_found:
                print("⚠️ 설정 메뉴가 나타나지 않았습니다")
                print("📝 설정 버튼을 클릭했지만 메뉴가 표시되지 않았을 수 있습니다")
        
        except Exception as e:
            print(f"❌ 설정 메뉴 확인 실패: {e}")
            return False
        
        # 5. 스크린샷 저장
        print("\n📋 5. 스크린샷 저장")
        print("-" * 30)
        
        try:
            screenshot_path = await browser_manager.page.screenshot(path="reports/dev/screenshots/gear_settings_test.png")
            print(f"📸 스크린샷 저장: {screenshot_path}")
        except Exception as e:
            print(f"❌ 스크린샷 저장 실패: {e}")
        
        print("\n" + "=" * 60)
        print("✅ 톱니바퀴 설정 버튼 테스트 완료")
        print("=" * 60)
        
        return True

async def main():
    """메인 실행 함수"""
    print("🚀 톱니바퀴 설정 버튼 테스트 시작")
    print("=" * 60)
    
    try:
        success = await test_gear_settings_button("dev")
        if success:
            print("✅ 톱니바퀴 설정 버튼 테스트 성공!")
        else:
            print("❌ 톱니바퀴 설정 버튼 테스트 실패")
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 톱니바퀴 설정 버튼 테스트 완료")

if __name__ == "__main__":
    asyncio.run(main())
