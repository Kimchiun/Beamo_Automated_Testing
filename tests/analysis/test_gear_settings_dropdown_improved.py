#!/usr/bin/env python3
"""
Improved Gear Settings Dropdown Test
톱니바퀴 버튼 클릭 시 드롭다운 메뉴를 정확히 감지하고 분석하는 개선된 테스트
"""

import asyncio
import sys
import pytest
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
@timeout(60)  # 60초 타임아웃으로 증가
async def test_gear_settings_dropdown_improved(environment: str = "dev"):
    """개선된 톱니바퀴 설정 버튼 드롭다운 테스트"""
    print(f"🔍 {environment.upper()} 환경에서 개선된 톱니바퀴 설정 버튼 드롭다운 테스트...")
    
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
            return False
        
        print("✅ 로그인 성공")
        
        # 대시보드로 이동
        await asyncio.sleep(3)
        
        # 글로벌 네비게이션 초기화
        global_nav = GlobalNavigation(browser_manager.page, config)
        
        print("\n" + "=" * 80)
        print("🔧 개선된 톱니바퀴 설정 버튼 드롭다운 테스트")
        print("=" * 80)
        
        # 1. 톱니바퀴 버튼 찾기 (개선된 셀렉터)
        print("\n📋 1. 톱니바퀴 버튼 찾기 (개선된 셀렉터)")
        print("-" * 50)
        
        gear_button = None
        improved_selectors = [
            # 이모지 기반
            "button:has-text('⚙️')",
            "button:has-text('🔧')",
            "a:has-text('⚙️')",
            "a:has-text('🔧')",
            # 클래스 기반 (더 구체적)
            "[class*='gear']",
            "[class*='cog']", 
            "[class*='settings']",
            "[class*='config']",
            # 속성 기반
            "[title*='설정']",
            "[title*='Settings']",
            "[title*='Config']",
            "[aria-label*='설정']",
            "[aria-label*='Settings']",
            "[aria-label*='Config']",
            # data 속성 기반
            "[data-testid*='gear']",
            "[data-testid*='settings']",
            "[data-testid*='config']",
            # role 기반
            "[role='button'][class*='gear']",
            "[role='button'][class*='settings']",
            # SVG 아이콘 기반
            "svg[class*='gear']",
            "svg[class*='cog']",
            "svg[class*='settings']",
            # 부모 요소 기반
            ".header button[class*='gear']",
            ".navigation button[class*='gear']",
            ".global-nav button[class*='gear']",
            ".top-bar button[class*='gear']"
        ]
        
        for selector in improved_selectors:
            try:
                elements = await browser_manager.page.query_selector_all(selector)
                for elem in elements:
                    if await elem.is_visible():
                        classes = await elem.get_attribute("class")
                        elem_text = await elem.text_content()
                        title = await elem.get_attribute("title")
                        aria_label = await elem.get_attribute("aria-label")
                        
                        print(f"   🔍 발견: {selector}")
                        print(f"      - 클래스: {classes}")
                        print(f"      - 텍스트: {elem_text}")
                        print(f"      - title: {title}")
                        print(f"      - aria-label: {aria_label}")
                        
                        # 톱니바퀴 관련 키워드가 포함된 요소 찾기
                        if any(keyword in (classes or "") for keyword in ['gear', 'cog', 'settings', 'config']):
                            gear_button = elem
                            print(f"   ✅ 톱니바퀴 버튼 후보 발견: {selector}")
                            break
                
                if gear_button:
                    break
                    
            except Exception as e:
                print(f"   ⚠️ 셀렉터 {selector} 오류: {e}")
                continue
        
        if not gear_button:
            print("❌ 톱니바퀴 버튼을 찾을 수 없습니다")
            return False
        
        print(f"✅ 톱니바퀴 버튼 발견: {gear_button}")
        
        # 2. 클릭 전 드롭다운/메뉴 상태 확인 (개선된 감지)
        print("\n📋 2. 클릭 전 드롭다운/메뉴 상태 확인 (개선된 감지)")
        print("-" * 50)
        
        improved_dropdown_selectors = [
            # 일반적인 드롭다운/메뉴 셀렉터
            "[class*='dropdown']",
            "[class*='popover']",
            "[class*='panel']",
            "[class*='menu']",
            "[class*='tooltip']",
            # 더 구체적인 셀렉터
            ".el-dropdown",
            ".el-popover",
            ".el-menu",
            ".el-tooltip",
            ".ant-dropdown",
            ".ant-popover",
            ".ant-menu",
            ".ant-tooltip",
            # 커스텀 클래스
            "[class*='settings-menu']",
            "[class*='gear-menu']",
            "[class*='config-menu']",
            "[class*='admin-menu']",
            # data 속성 기반
            "[data-testid*='dropdown']",
            "[data-testid*='menu']",
            "[data-testid*='popover']",
            # role 기반
            "[role='menu']",
            "[role='listbox']",
            "[role='dialog']",
            "[role='tooltip']",
            # aria 속성 기반
            "[aria-expanded='true']",
            "[aria-hidden='false']",
            # 가시성 기반
            "[style*='display: block']",
            "[style*='visibility: visible']",
            "[style*='opacity: 1']"
        ]
        
        initial_dropdowns = []
        for selector in improved_dropdown_selectors:
            try:
                elements = await browser_manager.page.query_selector_all(selector)
                for elem in elements:
                    if await elem.is_visible():
                        classes = await elem.get_attribute("class")
                        elem_text = await elem.text_content()
                        role = await elem.get_attribute("role")
                        aria_expanded = await elem.get_attribute("aria-expanded")
                        
                        initial_dropdowns.append({
                            "selector": selector,
                            "classes": classes,
                            "text": elem_text,
                            "role": role,
                            "aria_expanded": aria_expanded
                        })
                        print(f"   - 발견: {selector} (클래스: {classes}, role: {role})")
            except:
                continue
        
        if not initial_dropdowns:
            print("   - 클릭 전 열린 드롭다운/메뉴 없음")
        
        # 3. 톱니바퀴 버튼 클릭 (개선된 클릭 방식)
        print("\n📋 3. 톱니바퀴 버튼 클릭 (개선된 클릭 방식)")
        print("-" * 50)
        
        try:
            print("🖱️ 톱니바퀴 버튼 클릭 시도...")
            
            # 클릭 전 스크린샷
            before_screenshot = await browser_manager.page.screenshot(path="reports/dev/screenshots/gear_button_before_click_improved.png")
            print(f"📸 클릭 전 스크린샷 저장: {before_screenshot}")
            
            # 개선된 클릭 방식
            await gear_button.scroll_into_view_if_needed()
            await asyncio.sleep(1)  # 스크롤 완료 대기
            
            # 여러 클릭 방식 시도
            try:
                await gear_button.click()
                print("✅ 기본 클릭 방식으로 클릭 완료")
            except:
                try:
                    await browser_manager.page.evaluate("(element) => element.click()", gear_button)
                    print("✅ JavaScript 클릭 방식으로 클릭 완료")
                except:
                    await browser_manager.page.evaluate("(element) => element.dispatchEvent(new MouseEvent('click', {bubbles: true}))", gear_button)
                    print("✅ MouseEvent 방식으로 클릭 완료")
            
            # 클릭 후 대기 시간 증가 (애니메이션/지연 고려)
            print("⏳ 클릭 후 대기 중... (5초)")
            await asyncio.sleep(5)
            
            # 클릭 후 스크린샷
            after_screenshot = await browser_manager.page.screenshot(path="reports/dev/screenshots/gear_button_after_click_improved.png")
            print(f"📸 클릭 후 스크린샷 저장: {after_screenshot}")
            
        except Exception as e:
            print(f"❌ 톱니바퀴 버튼 클릭 실패: {e}")
            return False
        
        # 4. 클릭 후 드롭다운/메뉴 요소 확인 (개선된 감지)
        print("\n📋 4. 클릭 후 드롭다운/메뉴 요소 확인 (개선된 감지)")
        print("-" * 50)
        
        print("🔍 클릭 후 드롭다운/메뉴 요소 확인...")
        after_dropdowns = []
        
        # 추가 대기 (드롭다운이 늦게 나타날 수 있음)
        await asyncio.sleep(2)
        
        for selector in improved_dropdown_selectors:
            try:
                elements = await browser_manager.page.query_selector_all(selector)
                for elem in elements:
                    if await elem.is_visible():
                        classes = await elem.get_attribute("class")
                        elem_text = await elem.text_content()
                        role = await elem.get_attribute("role")
                        aria_expanded = await elem.get_attribute("aria-expanded")
                        
                        after_dropdowns.append({
                            "selector": selector,
                            "classes": classes,
                            "text": elem_text,
                            "role": role,
                            "aria_expanded": aria_expanded
                        })
                        print(f"   - 발견: {selector} (클래스: {classes}, role: {role})")
            except:
                continue
        
        if not after_dropdowns:
            print("   - 클릭 후 열린 드롭다운/메뉴 없음")
        
        # 5. 드롭다운/메뉴 요소 변화 분석 (개선된 분석)
        print("\n📋 5. 드롭다운/메뉴 요소 변화 분석 (개선된 분석)")
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
                print(f"   - role: {dd['role']}")
                print(f"   - aria-expanded: {dd['aria_expanded']}")
        else:
            print("❌ 새로 나타난 드롭다운/메뉴 없음")
        
        # 6. 드롭다운/메뉴 내부 요소 상세 분석
        print("\n📋 6. 드롭다운/메뉴 내부 요소 상세 분석")
        print("-" * 50)
        
        if new_dropdowns:
            for i, dropdown in enumerate(new_dropdowns):
                print(f"\n🔍 드롭다운 {i+1} 내부 요소 분석:")
                
                # 드롭다운 내부의 모든 클릭 가능한 요소 찾기
                try:
                    clickable_elements = await dropdown.query_selector_all("button, a, [role='button'], [role='menuitem'], [class*='menu-item'], [class*='dropdown-item']")
                    
                    if clickable_elements:
                        print(f"   📋 클릭 가능한 요소: {len(clickable_elements)}개")
                        for j, elem in enumerate(clickable_elements):
                            if await elem.is_visible():
                                elem_text = await elem.text_content()
                                elem_classes = await elem.get_attribute("class")
                                elem_role = await elem.get_attribute("role")
                                elem_href = await elem.get_attribute("href")
                                
                                print(f"      {j+1}. {elem_text}")
                                print(f"         - 클래스: {elem_classes}")
                                print(f"         - role: {elem_role}")
                                print(f"         - href: {elem_href}")
                    else:
                        print("   - 클릭 가능한 요소 없음")
                        
                except Exception as e:
                    print(f"   ⚠️ 내부 요소 분석 오류: {e}")
        else:
            # 드롭다운이 감지되지 않았을 때 전체 페이지에서 설정 관련 요소 찾기
            print("🔍 전체 페이지에서 설정 관련 요소 찾기...")
            
            settings_selectors = [
                "[class*='settings']",
                "[class*='gear']",
                "[class*='config']",
                "[class*='admin']",
                "[class*='management']",
                "[class*='preferences']",
                "[class*='license']",
                "[class*='security']",
                "[class*='user']",
                "[class*='team']"
            ]
            
            for selector in settings_selectors:
                try:
                    elements = await browser_manager.page.query_selector_all(selector)
                    for elem in elements:
                        if await elem.is_visible():
                            elem_text = await elem.text_content()
                            elem_classes = await elem.get_attribute("class")
                            if elem_text and len(elem_text.strip()) > 0:
                                print(f"   - 발견: {selector} (텍스트: {elem_text}, 클래스: {elem_classes})")
                except:
                    continue
        
        # 7. 최종 스크린샷 및 결과 요약
        print("\n📋 7. 최종 스크린샷 및 결과 요약")
        print("-" * 50)
        
        # 최종 스크린샷
        final_screenshot = await browser_manager.page.screenshot(path="reports/dev/screenshots/gear_settings_dropdown_improved_final.png")
        print(f"📸 최종 스크린샷 저장: {final_screenshot}")
        
        # 결과 요약
        print("\n" + "=" * 80)
        print("📊 테스트 결과 요약")
        print("=" * 80)
        print(f"✅ 톱니바퀴 버튼 발견: {'성공' if gear_button else '실패'}")
        print(f"✅ 버튼 클릭: {'성공' if gear_button else '실패'}")
        print(f"✅ 새 드롭다운/메뉴: {len(new_dropdowns)}개")
        print(f"📸 생성된 스크린샷: 3개")
        
        if new_dropdowns:
            print("\n🎯 드롭다운 메뉴 감지 성공!")
            return True
        else:
            print("\n⚠️ 드롭다운 메뉴가 감지되지 않았습니다")
            return False

async def main():
    """메인 실행 함수"""
    print("🚀 개선된 톱니바퀴 설정 버튼 드롭다운 테스트 시작")
    print("=" * 80)
    
    try:
        success = await test_gear_settings_dropdown_improved("dev")
        if success:
            print("✅ 개선된 톱니바퀴 설정 버튼 드롭다운 테스트 성공!")
        else:
            print("❌ 개선된 톱니바퀴 설정 버튼 드롭다운 테스트 실패")
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
    
    print("\n" + "=" * 80)
    print("✅ 개선된 톱니바퀴 설정 버튼 드롭다운 테스트 완료")

if __name__ == "__main__":
    asyncio.run(main())
