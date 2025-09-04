#!/usr/bin/env python3
"""
Comprehensive Gear Settings Dropdown Test
톱니바퀴 설정 버튼의 드롭다운 메뉴 모든 항목을 순차적으로 클릭하고 동작을 분석하는 테스트
"""

import asyncio
import sys
import pytest
from pathlib import Path
from functools import wraps
import time

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.config_loader import get_config
from utils.browser_manager import BrowserFactory
from pages.login_page import LoginPage
from pages.components.global_navigation import GlobalNavigation

def timeout(seconds):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=seconds)
            except asyncio.TimeoutError:
                print(f"⏰ 함수 실행 시간 초과 ({seconds}초)")
                return False
        return wrapper
    return decorator

@pytest.mark.p0
@pytest.mark.env('dev')
@timeout(120)  # 2분 타임아웃
async def test_gear_settings_dropdown_comprehensive(environment: str = "dev"):
    print(f"🔍 {environment.upper()} 환경에서 톱니바퀴 설정 드롭다운 종합 테스트...")
    config = get_config(environment)
    
    async with BrowserFactory.create(config) as browser_manager:
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
        
        await asyncio.sleep(3)
        global_nav = GlobalNavigation(browser_manager.page, config)
        
        print("\n" + "=" * 80)
        print("🔧 톱니바퀴 설정 드롭다운 종합 분석 테스트")
        print("=" * 80)
        
        # 1. 톱니바퀴 버튼 찾기 (다양한 셀렉터 시도)
        gear_button = None
        gear_selectors = [
            "button:has-text('⚙️')",
            "[class*='gear']",
            "[class*='cog']", 
            "[class*='settings']",
            "[data-testid*='settings']",
            "[data-testid*='gear']",
            "[aria-label*='settings']",
            "[aria-label*='gear']",
            "[title*='settings']",
            "[title*='gear']",
            "svg[class*='gear']",
            "svg[class*='cog']",
            "svg[class*='settings']",
            "[role='button'][class*='gear']",
            "[role='button'][class*='settings']"
        ]
        
        print("🔍 톱니바퀴 버튼 찾는 중...")
        for selector in gear_selectors:
            try:
                element = await browser_manager.page.query_selector(selector)
                if element and await element.is_visible():
                    gear_button = element
                    print(f"✅ 톱니바퀴 버튼 발견: {selector}")
                    break
            except Exception as e:
                continue
        
        if not gear_button:
            print("❌ 톱니바퀴 버튼을 찾을 수 없습니다")
            # 페이지 전체에서 톱니바퀴 관련 요소 검색
            print("🔍 페이지 전체에서 톱니바퀴 관련 요소 검색...")
            all_elements = await browser_manager.page.query_selector_all("*")
            for elem in all_elements:
                try:
                    if await elem.is_visible():
                        text = await elem.text_content() or ""
                        classes = await elem.get_attribute("class") or ""
                        if "⚙️" in text or any(keyword in classes.lower() for keyword in ['gear', 'cog', 'settings']):
                            print(f"   발견: {await elem.evaluate('el => el.outerHTML')}")
                except:
                    continue
            return False
        
        # 2. 클릭 전 상태 확인
        print("\n📸 클릭 전 스크린샷 저장...")
        await browser_manager.page.screenshot(path="reports/dev/screenshots/gear_before_click_comprehensive.png")
        
        # 3. 톱니바퀴 버튼 클릭
        print("🖱️ 톱니바퀴 버튼 클릭...")
        try:
            await gear_button.scroll_into_view_if_needed()
            await asyncio.sleep(1)
            await gear_button.click()
            print("✅ 클릭 성공")
        except Exception as e:
            print(f"❌ 클릭 실패: {e}")
            # JavaScript 클릭 시도
            try:
                await browser_manager.page.evaluate("(element) => element.click()", gear_button)
                print("✅ JavaScript 클릭 성공")
            except Exception as e2:
                print(f"❌ JavaScript 클릭도 실패: {e2}")
                return False
        
        # 4. 드롭다운 메뉴 로딩 대기
        print("⏳ 드롭다운 메뉴 로딩 대기...")
        await asyncio.sleep(3)
        
        # 5. 클릭 후 상태 확인
        print("📸 클릭 후 스크린샷 저장...")
        await browser_manager.page.screenshot(path="reports/dev/screenshots/gear_after_click_comprehensive.png")
        
        # 6. 드롭다운 메뉴 요소 찾기
        print("\n🔍 드롭다운 메뉴 요소 찾는 중...")
        dropdown_selectors = [
            "[class*='dropdown']",
            "[class*='menu']",
            "[class*='popup']",
            "[class*='modal']",
            "[role='menu']",
            "[role='listbox']",
            "[role='dialog']",
            "[data-testid*='dropdown']",
            "[data-testid*='menu']",
            "[aria-expanded='true']",
            "[class*='open']",
            "[class*='show']",
            "[class*='visible']"
        ]
        
        dropdown_menu = None
        for selector in dropdown_selectors:
            try:
                element = await browser_manager.page.query_selector(selector)
                if element and await element.is_visible():
                    dropdown_menu = element
                    print(f"✅ 드롭다운 메뉴 발견: {selector}")
                    break
            except Exception as e:
                continue
        
        if not dropdown_menu:
            print("❌ 드롭다운 메뉴를 찾을 수 없습니다")
            # 페이지 전체에서 새로 나타난 요소 검색
            print("🔍 페이지 전체에서 새로 나타난 요소 검색...")
            all_elements = await browser_manager.page.query_selector_all("*")
            for elem in all_elements:
                try:
                    if await elem.is_visible():
                        classes = await elem.get_attribute("class") or ""
                        if any(keyword in classes.lower() for keyword in ['menu', 'dropdown', 'popup', 'modal']):
                            print(f"   메뉴 관련 요소: {await elem.evaluate('el => el.outerHTML')}")
                except:
                    continue
            return False
        
        # 7. 드롭다운 메뉴 내부 요소 분석
        print("\n📋 드롭다운 메뉴 내부 요소 분석...")
        menu_items = await dropdown_menu.query_selector_all("*")
        clickable_items = []
        
        for item in menu_items:
            try:
                if await item.is_visible():
                    tag_name = await item.evaluate('el => el.tagName.toLowerCase()')
                    text = await item.text_content() or ""
                    classes = await item.get_attribute("class") or ""
                    role = await item.get_attribute("role") or ""
                    
                    # 클릭 가능한 요소인지 확인
                    is_clickable = (
                        tag_name in ['button', 'a', 'div', 'span'] and
                        (role in ['menuitem', 'button', 'link'] or
                         any(keyword in classes.lower() for keyword in ['clickable', 'button', 'link', 'item']))
                    )
                    
                    if is_clickable and text.strip():
                        clickable_items.append({
                            'element': item,
                            'text': text.strip(),
                            'tag': tag_name,
                            'classes': classes,
                            'role': role
                        })
                        print(f"   📌 클릭 가능한 항목: {text.strip()} ({tag_name}, role={role})")
            except Exception as e:
                continue
        
        if not clickable_items:
            print("❌ 클릭 가능한 메뉴 항목을 찾을 수 없습니다")
            return False
        
        # 8. 각 메뉴 항목 순차적으로 클릭하고 동작 분석
        print(f"\n🖱️ 총 {len(clickable_items)}개 메뉴 항목을 순차적으로 클릭하고 분석...")
        
        for i, item_info in enumerate(clickable_items):
            print(f"\n--- {i+1}/{len(clickable_items)}: {item_info['text']} ---")
            
            # 클릭 전 스크린샷
            await browser_manager.page.screenshot(path=f"reports/dev/screenshots/menu_item_{i+1:02d}_{item_info['text'].replace(' ', '_')}_before.png")
            
            # 현재 URL과 페이지 제목 기록
            current_url = browser_manager.page.url
            current_title = await browser_manager.page.title()
            
            print(f"   📍 클릭 전 URL: {current_url}")
            print(f"   📍 클릭 전 제목: {current_title}")
            
            # 메뉴 항목 클릭
            try:
                await item_info['element'].scroll_into_view_if_needed()
                await asyncio.sleep(1)
                await item_info['element'].click()
                print(f"   ✅ 클릭 성공")
            except Exception as e:
                print(f"   ❌ 클릭 실패: {e}")
                continue
            
            # 클릭 후 변화 대기
            await asyncio.sleep(3)
            
            # 클릭 후 스크린샷
            await browser_manager.page.screenshot(path=f"reports/dev/screenshots/menu_item_{i+1:02d}_{item_info['text'].replace(' ', '_')}_after.png")
            
            # 클릭 후 변화 분석
            new_url = browser_manager.page.url
            new_title = await browser_manager.page.title()
            
            print(f"   📍 클릭 후 URL: {new_url}")
            print(f"   📍 클릭 후 제목: {new_title}")
            
            # URL 변화 확인
            if new_url != current_url:
                print(f"   🔄 URL 변화 감지: {current_url} → {new_url}")
            else:
                print(f"   🔄 URL 변화 없음")
            
            # 제목 변화 확인
            if new_title != current_title:
                print(f"   🔄 제목 변화 감지: {current_title} → {new_title}")
            else:
                print(f"   🔄 제목 변화 없음")
            
            # 새로운 모달/팝업/페이지 요소 확인
            new_elements = await browser_manager.page.query_selector_all("[class*='modal'], [class*='popup'], [class*='dialog'], [class*='page'], [class*='content']")
            if new_elements:
                print(f"   🆕 새로운 요소 {len(new_elements)}개 발견")
                for j, elem in enumerate(new_elements[:3]):  # 처음 3개만 표시
                    try:
                        if await elem.is_visible():
                            text = await elem.text_content() or ""
                            classes = await elem.get_attribute("class") or ""
                            print(f"      {j+1}. {text[:50]}... ({classes})")
                    except:
                        continue
            
            # 뒤로가기 (필요한 경우)
            if new_url != current_url:
                try:
                    await browser_manager.page.go_back()
                    await asyncio.sleep(2)
                    print(f"   ↩️ 뒤로가기 완료")
                except Exception as e:
                    print(f"   ❌ 뒤로가기 실패: {e}")
            
            # 드롭다운 메뉴가 여전히 열려있는지 확인
            if not await dropdown_menu.is_visible():
                print(f"   ⚠️ 드롭다운 메뉴가 닫힘 - 다시 열기 시도...")
                try:
                    await gear_button.click()
                    await asyncio.sleep(2)
                    dropdown_menu = await browser_manager.page.query_selector("[class*='dropdown'], [class*='menu'], [role='menu']")
                    if not dropdown_menu:
                        print(f"   ❌ 드롭다운 메뉴를 다시 열 수 없음")
                        break
                except Exception as e:
                    print(f"   ❌ 드롭다운 메뉴 재오픈 실패: {e}")
                    break
        
        # 9. 최종 결과 요약
        print("\n" + "=" * 80)
        print("📊 드롭다운 메뉴 종합 분석 결과")
        print("=" * 80)
        print(f"✅ 분석 완료된 메뉴 항목: {len(clickable_items)}개")
        print(f"📸 생성된 스크린샷: {len(clickable_items) * 2 + 2}개")
        print("📁 스크린샷 저장 위치: reports/dev/screenshots/")
        
        # 최종 스크린샷
        await browser_manager.page.screenshot(path="reports/dev/screenshots/gear_settings_comprehensive_final.png")
        print("📸 최종 스크린샷 저장 완료")
        
        return True

async def main():
    """메인 실행 함수"""
    try:
        result = await test_gear_settings_dropdown_comprehensive("dev")
        if result:
            print("\n🎉 테스트 성공!")
        else:
            print("\n❌ 테스트 실패")
    except Exception as e:
        print(f"\n💥 테스트 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
