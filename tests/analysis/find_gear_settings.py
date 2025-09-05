#!/usr/bin/env python3
"""
Find Gear Settings Button
톱니바퀴 아이콘(⚙️) 설정 버튼을 찾고 클릭했을 때 나타나는 요소들을 분석합니다.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.config_loader import get_config
from utils.browser_manager import BrowserFactory
from pages.login_page import LoginPage

async def find_gear_settings(environment: str = "dev"):
    """톱니바퀴 설정 버튼 찾기"""
    print(f"🔍 {environment.upper()} 환경에서 톱니바퀴 설정 버튼 찾기...")
    
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
        
        print("\n" + "=" * 60)
        print("🔍 톱니바퀴 설정 버튼 찾기")
        print("=" * 60)
        
        # 1. 톱니바퀴 아이콘 관련 셀렉터들
        print("\n📋 1. 톱니바퀴 아이콘 관련 셀렉터들")
        print("-" * 30)
        
        gear_selectors = [
            # 톱니바퀴 이모지
            "⚙️",
            "🔧",
            # 톱니바퀴 관련 텍스트
            "button:has-text('⚙️')",
            "button:has-text('🔧')",
            "a:has-text('⚙️')",
            "a:has-text('🔧')",
            # 설정 관련 텍스트
            "button:has-text('설정')",
            "button:has-text('Settings')",
            "button:has-text('Config')",
            "button:has-text('Configuration')",
            "a:has-text('설정')",
            "a:has-text('Settings')",
            "a:has-text('Config')",
            "a:has-text('Configuration')",
            # 클래스 기반
            "[class*='gear']",
            "[class*='settings']",
            "[class*='config']",
            "[class*='cog']",
            # 아이콘 관련
            "[class*='icon']",
            "[class*='fa']",
            "[class*='material']",
            # data-testid
            "[data-testid*='settings']",
            "[data-testid*='config']",
            "[data-testid*='gear']",
            "[data-testid*='cog']",
            # 우측 상단 영역
            ".header-right button",
            ".nav-right button",
            ".header-right a",
            ".nav-right a",
            ".header-right [class*='icon']",
            ".nav-right [class*='icon']",
            # 일반적인 버튼/링크
            "button[title*='설정']",
            "button[title*='Settings']",
            "button[title*='Config']",
            "a[title*='설정']",
            "a[title*='Settings']",
            "a[title*='Config']",
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
                            title_attr = await elem.get_attribute("title")
                            aria_label = await elem.get_attribute("aria-label")
                            
                            print(f"✅ 톱니바퀴/설정 관련 요소 발견: {selector}")
                            print(f"  - 태그: <{tag_name}>")
                            print(f"  - 클래스: {classes}")
                            print(f"  - 텍스트: {elem_text}")
                            print(f"  - title: {title_attr}")
                            print(f"  - aria-label: {aria_label}")
                            
                            # 클릭 가능한지 확인
                            is_clickable = await elem.evaluate("el => el.tagName === 'BUTTON' || el.tagName === 'A' || el.onclick || el.getAttribute('role') === 'button'")
                            print(f"  - 클릭 가능: {is_clickable}")
                            
                            if is_clickable:
                                print("  - 클릭 시도...")
                                try:
                                    await elem.click()
                                    await asyncio.sleep(2)
                                    print("  - 클릭 성공, 잠시 대기 후 페이지 상태 확인")
                                    
                                    # 클릭 후 나타나는 요소들 확인
                                    print("\n📋 2. 클릭 후 나타나는 요소들 확인")
                                    print("-" * 30)
                                    
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
                                        ".ant-menu",
                                        ".MuiMenu-root",
                                        ".MuiPopover-root"
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
                                                        
                                                        print(f"✅ 모달/드롭다운 발견: {modal_selector}")
                                                        print(f"  - 태그: <{modal_tag}>")
                                                        print(f"  - 클래스: {modal_classes}")
                                                        print(f"  - 텍스트: {modal_text[:200]}...")
                                                        
                                                        # 모달 내부의 메뉴 아이템들 찾기
                                                        menu_items = await modal_elem.query_selector_all("li, .menu-item, .dropdown-item, button, a, .el-menu-item, .ant-menu-item")
                                                        print(f"  - 메뉴 아이템 개수: {len(menu_items)}")
                                                        
                                                        for i, item in enumerate(menu_items[:20]):  # 처음 20개만
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
                                        print("❌ 모달/드롭다운을 찾을 수 없음")
                                    
                                    gear_found = True
                                    break
                                    
                                except Exception as click_error:
                                    print(f"  - 클릭 실패: {click_error}")
                            
                    except Exception as elem_error:
                        continue
                if gear_found:
                    break
            except:
                continue
        
        if not gear_found:
            print("❌ 톱니바퀴/설정 버튼을 찾을 수 없음")
            print("🔍 다른 방법으로 설정 관련 요소 찾기...")
            
            # 페이지 전체에서 톱니바퀴 관련 요소 찾기
            print("\n📋 3. 페이지 전체에서 톱니바퀴 관련 요소 찾기")
            print("-" * 30)
            
            # 모든 버튼과 링크 확인
            all_clickable = await browser_manager.page.query_selector_all("button, a, [role='button']")
            print(f"페이지의 클릭 가능한 요소 개수: {len(all_clickable)}")
            
            gear_candidates = []
            for i, elem in enumerate(all_clickable[:50]):  # 처음 50개만 확인
                try:
                    if await elem.is_visible():
                        elem_text = await elem.text_content()
                        elem_classes = await elem.get_attribute("class")
                        elem_title = await elem.get_attribute("title")
                        
                        # 톱니바퀴/설정 관련 키워드가 있는지 확인
                        keywords = ["⚙️", "🔧", "설정", "Settings", "Config", "gear", "cog", "settings", "config"]
                        for keyword in keywords:
                            if (elem_text and keyword in elem_text) or (elem_classes and keyword in elem_classes) or (elem_title and keyword in elem_title):
                                gear_candidates.append({
                                    "index": i,
                                    "text": elem_text,
                                    "classes": elem_classes,
                                    "title": elem_title
                                })
                                break
                except:
                    continue
            
            if gear_candidates:
                print(f"톱니바퀴/설정 관련 후보 요소들: {len(gear_candidates)}개")
                for candidate in gear_candidates:
                    print(f"  - {candidate['index']}: {candidate['text']} (클래스: {candidate['classes']}, title: {candidate['title']})")
            else:
                print("톱니바퀴/설정 관련 후보 요소를 찾을 수 없음")
        
        # 4. 스크린샷 저장
        print("\n📋 4. 스크린샷 저장")
        print("-" * 30)
        
        try:
            screenshot_path = await browser_manager.page.screenshot(path="reports/dev/screenshots/gear_settings_found.png")
            print(f"📸 스크린샷 저장: {screenshot_path}")
        except Exception as e:
            print(f"❌ 스크린샷 저장 실패: {e}")
        
        print("\n" + "=" * 60)
        print("✅ 톱니바퀴 설정 버튼 찾기 완료")
        print("=" * 60)
        
        return True

async def main():
    """메인 실행 함수"""
    print("🚀 톱니바퀴 설정 버튼 찾기 시작")
    print("=" * 60)
    
    try:
        success = await find_gear_settings("dev")
        if success:
            print("✅ 톱니바퀴 설정 버튼 찾기 성공!")
        else:
            print("❌ 톱니바퀴 설정 버튼 찾기 실패")
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 톱니바퀴 설정 버튼 찾기 완료")

if __name__ == "__main__":
    asyncio.run(main())
