#!/usr/bin/env python3
"""
Gear Settings Dropdown Test
톱니바퀴 버튼을 클릭했을 때 드롭다운 요소들이 나타나는지 테스트합니다.
"""

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

async def test_gear_settings_dropdown(environment: str = "dev"):
    """톱니바퀴 설정 버튼 드롭다운 테스트"""
    print(f"🔍 {environment.upper()} 환경에서 톱니바퀴 설정 버튼 드롭다운 테스트...")
    
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
        await asyncio.sleep(3)
        
        # 글로벌 네비게이션 초기화
        global_nav = GlobalNavigation(browser_manager.page, config)
        
        print("\n" + "=" * 80)
        print("🔍 톱니바퀴 설정 버튼 드롭다운 테스트")
        print("=" * 80)
        
        # 1. 톱니바퀴 버튼 찾기
        print("\n📋 1. 톱니바퀴 버튼 찾기")
        print("-" * 50)
        
        gear_selectors = [
            "button:has-text('⚙️')",
            "button:has-text('🔧')",
            "a:has-text('⚙️')",
            "a:has-text('🔧')",
            "[class*='gear']",
            "[class*='cog']",
            "[class*='settings']",
            "[class*='config']",
            "[title*='설정']",
            "[title*='Settings']",
            "[title*='Config']",
            "[aria-label*='설정']",
            "[aria-label*='Settings']",
            "[aria-label*='Config']",
            ".gear-settings",
            ".settings-gear",
            ".cog-settings",
            ".settings-cog"
        ]
        
        gear_button = None
        gear_button_info = {}
        
        for selector in gear_selectors:
            try:
                elements = await browser_manager.page.query_selector_all(selector)
                for elem in elements:
                    if await elem.is_visible():
                        tag_name = await elem.evaluate("el => el.tagName.toLowerCase()")
                        classes = await elem.get_attribute("class")
                        elem_text = await elem.text_content()
                        title = await elem.get_attribute("title")
                        aria_label = await elem.get_attribute("aria-label")
                        
                        print(f"✅ 톱니바퀴 버튼 발견!")
                        print(f"   - 셀렉터: {selector}")
                        print(f"   - 태그: <{tag_name}>")
                        print(f"   - 텍스트: {elem_text}")
                        print(f"   - 클래스: {classes}")
                        print(f"   - title: {title}")
                        print(f"   - aria-label: {aria_label}")
                        
                        gear_button = elem
                        gear_button_info = {
                            "selector": selector,
                            "tag": tag_name,
                            "text": elem_text,
                            "classes": classes,
                            "title": title,
                            "aria_label": aria_label
                        }
                        break
                if gear_button:
                    break
            except Exception as e:
                continue
        
        if not gear_button:
            print("❌ 톱니바퀴 버튼을 찾을 수 없습니다.")
            print("📋 페이지 전체에서 톱니바퀴 관련 요소 검색...")
            
            # 페이지 전체에서 톱니바퀴 관련 요소 검색
            try:
                all_elements = await browser_manager.page.query_selector_all("*")
                for elem in all_elements:
                    try:
                        if await elem.is_visible():
                            elem_text = await elem.text_content()
                            classes = await elem.get_attribute("class")
                            title = await elem.get_attribute("title")
                            aria_label = await elem.get_attribute("aria-label")
                            
                            if (elem_text and ('⚙️' in elem_text or '🔧' in elem_text or 'gear' in (elem_text or '').lower() or 'cog' in (elem_text or '').lower() or 'settings' in (elem_text or '').lower())) or \
                               (classes and ('gear' in classes.lower() or 'cog' in classes.lower() or 'settings' in classes.lower())) or \
                               (title and ('gear' in title.lower() or 'cog' in title.lower() or 'settings' in title.lower())) or \
                               (aria_label and ('gear' in aria_label.lower() or 'cog' in aria_label.lower() or 'settings' in aria_label.lower())):
                                
                                tag_name = await elem.evaluate("el => el.tagName.toLowerCase()")
                                print(f"🔍 톱니바퀴 관련 요소 발견:")
                                print(f"   - 태그: <{tag_name}>")
                                print(f"   - 텍스트: {elem_text}")
                                print(f"   - 클래스: {classes}")
                                print(f"   - title: {title}")
                                print(f"   - aria-label: {aria_label}")
                                
                                if tag_name in ['button', 'a', 'div', 'span']:
                                    gear_button = elem
                                    gear_button_info = {
                                        "selector": f"found element with {tag_name}",
                                        "tag": tag_name,
                                        "text": elem_text,
                                        "classes": classes,
                                        "title": title,
                                        "aria_label": aria_label
                                    }
                                    print(f"✅ 이 요소를 톱니바퀴 버튼으로 사용하겠습니다.")
                                    break
                    except:
                        continue
            except Exception as e:
                print(f"❌ 페이지 전체 검색 실패: {e}")
        
        if not gear_button:
            print("❌ 톱니바퀴 버튼을 찾을 수 없습니다. 테스트를 종료합니다.")
            return False
        
        # 2. 톱니바퀴 버튼 클릭 전 상태 확인
        print("\n📋 2. 톱니바퀴 버튼 클릭 전 상태 확인")
        print("-" * 50)
        
        # 드롭다운/메뉴 요소가 이미 열려있는지 확인
        dropdown_selectors = [
            "[class*='dropdown']",
            "[class*='menu']",
            "[class*='popover']",
            "[class*='panel']",
            "[class*='drawer']",
            "[class*='sidebar']",
            "[class*='overlay']",
            "[class*='modal']",
            "[class*='dialog']"
        ]
        
        print("🔍 클릭 전 드롭다운/메뉴 요소 확인...")
        initial_dropdowns = []
        for selector in dropdown_selectors:
            try:
                elements = await browser_manager.page.query_selector_all(selector)
                for elem in elements:
                    if await elem.is_visible():
                        classes = await elem.get_attribute("class")
                        elem_text = await elem.text_content()
                        initial_dropdowns.append({
                            "selector": selector,
                            "classes": classes,
                            "text": elem_text
                        })
                        print(f"   - 발견: {selector} (클래스: {classes})")
            except:
                continue
        
        if not initial_dropdowns:
            print("   - 클릭 전 열린 드롭다운/메뉴 없음")
        
        # 3. 톱니바퀴 버튼 클릭
        print("\n📋 3. 톱니바퀴 버튼 클릭")
        print("-" * 50)
        
        try:
            print("🖱️ 톱니바퀴 버튼 클릭 시도...")
            
            # 클릭 전 스크린샷
            before_screenshot = await browser_manager.page.screenshot(path="reports/dev/screenshots/gear_button_before_click.png")
            print(f"📸 클릭 전 스크린샷 저장: {before_screenshot}")
            
            # 버튼 클릭
            await gear_button.click()
            print("✅ 톱니바퀴 버튼 클릭 완료")
            
            # 클릭 후 대기
            await asyncio.sleep(2)
            
            # 클릭 후 스크린샷
            after_screenshot = await browser_manager.page.screenshot(path="reports/dev/screenshots/gear_button_after_click.png")
            print(f"📸 클릭 후 스크린샷 저장: {after_screenshot}")
            
        except Exception as e:
            print(f"❌ 톱니바퀴 버튼 클릭 실패: {e}")
            return False
        
        # 4. 클릭 후 드롭다운/메뉴 요소 확인
        print("\n📋 4. 클릭 후 드롭다운/메뉴 요소 확인")
        print("-" * 50)
        
        print("🔍 클릭 후 드롭다운/메뉴 요소 확인...")
        after_dropdowns = []
        for selector in dropdown_selectors:
            try:
                elements = await browser_manager.page.query_selector_all(selector)
                for elem in elements:
                    if await elem.is_visible():
                        classes = await elem.get_attribute("class")
                        elem_text = await elem.text_content()
                        after_dropdowns.append({
                            "selector": selector,
                            "classes": classes,
                            "text": elem_text
                        })
                        print(f"   - 발견: {selector} (클래스: {classes})")
            except:
                continue
        
        if not after_dropdowns:
            print("   - 클릭 후 열린 드롭다운/메뉴 없음")
        
        # 5. 드롭다운/메뉴 요소 변화 분석
        print("\n📋 5. 드롭다운/메뉴 요소 변화 분석")
        print("-" * 50)
        
        # 새로 나타난 드롭다운/메뉴 찾기
        new_dropdowns = []
        for after_dd in after_dropdowns:
            is_new = True
            for initial_dd in initial_dropdowns:
                if (after_dd["selector"] == initial_dd["selector"] and 
                    after_dd["classes"] == initial_dd["classes"] and
                    after_dd["text"] == initial_dd["text"]):
                    is_new = False
                    break
            if is_new:
                new_dropdowns.append(after_dd)
        
        if new_dropdowns:
            print(f"✅ 새로 나타난 드롭다운/메뉴: {len(new_dropdowns)}개")
            for i, dd in enumerate(new_dropdowns):
                print(f"\n{i+1}. {dd['selector']}")
                print(f"   - 클래스: {dd['classes']}")
                print(f"   - 텍스트: {dd['text']}")
        else:
            print("❌ 새로 나타난 드롭다운/메뉴 없음")
        
        # 6. 드롭다운/메뉴 내부 요소 분석
        print("\n📋 6. 드롭다운/메뉴 내부 요소 분석")
        print("-" * 50)
        
        if new_dropdowns:
            for i, dropdown in enumerate(new_dropdowns):
                print(f"\n🔍 드롭다운 {i+1} 내부 요소 분석:")
                
                # 드롭다운 내부의 클릭 가능한 요소들 찾기
                try:
                    clickable_elements = await browser_manager.page.query_selector_all(f"{dropdown['selector']} button, {dropdown['selector']} a, {dropdown['selector']} [role='button']")
                    
                    if clickable_elements:
                        print(f"   📋 클릭 가능한 요소: {len(clickable_elements)}개")
                        for j, elem in enumerate(clickable_elements):
                            try:
                                elem_text = await elem.text_content()
                                elem_tag = await elem.evaluate("el => el.tagName.toLowerCase()")
                                elem_classes = await elem.get_attribute("class")
                                elem_href = await elem.get_attribute("href")
                                
                                print(f"      {j+1}. <{elem_tag}> {elem_text}")
                                print(f"         - 클래스: {elem_classes}")
                                if elem_href:
                                    print(f"         - href: {elem_href}")
                            except:
                                continue
                    else:
                        print("   - 클릭 가능한 요소 없음")
                        
                except Exception as e:
                    print(f"   ❌ 드롭다운 내부 분석 실패: {e}")
        else:
            print("분석할 드롭다운/메뉴가 없습니다.")
        
        # 7. 최종 스크린샷 저장
        print("\n📋 7. 최종 스크린샷 저장")
        print("-" * 50)
        
        try:
            final_screenshot = await browser_manager.page.screenshot(path="reports/dev/screenshots/gear_settings_dropdown_test_final.png")
            print(f"📸 최종 스크린샷 저장: {final_screenshot}")
        except Exception as e:
            print(f"❌ 최종 스크린샷 저장 실패: {e}")
        
        print("\n" + "=" * 80)
        print("✅ 톱니바퀴 설정 버튼 드롭다운 테스트 완료")
        print("=" * 80)
        
        return True

async def main():
    """메인 실행 함수"""
    print("🚀 톱니바퀴 설정 버튼 드롭다운 테스트 시작")
    print("=" * 80)
    
    try:
        success = await test_gear_settings_dropdown("dev")
        if success:
            print("✅ 톱니바퀴 설정 버튼 드롭다운 테스트 성공!")
        else:
            print("❌ 톱니바퀴 설정 버튼 드롭다운 테스트 실패")
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
    
    print("\n" + "=" * 80)
    print("✅ 톱니바퀴 설정 버튼 드롭다운 테스트 완료")

if __name__ == "__main__":
    asyncio.run(main())
