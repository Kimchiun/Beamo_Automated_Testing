#!/usr/bin/env python3
"""
Settings Menu Elements Analysis
설정 메뉴를 클릭했을 때 나타나는 요소들을 분석합니다.
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
from pages.components.global_navigation import GlobalNavigation

async def analyze_settings_menu_elements(environment: str = "dev"):
    """설정 메뉴 요소 분석"""
    print(f"🔍 {environment.upper()} 환경에서 설정 메뉴 요소 분석...")
    
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
        
        print("\n" + "=" * 60)
        print("🔍 설정 메뉴 요소 분석")
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
        
        # 2. 설정 메뉴 버튼 찾기
        print("\n📋 2. 설정 메뉴 버튼 찾기")
        print("-" * 30)
        
        try:
            # 설정 메뉴 셀렉터들
            settings_selectors = [
                ".settings-menu",
                ".config-menu", 
                ".settings",
                ".config",
                ".gear",
                ".cog",
                ".fa-cog",
                ".fa-gear",
                ".material-icons",
                "[class*='settings']",
                "[class*='config']",
                "[title*='설정']",
                "[title*='Settings']",
                "[aria-label*='설정']",
                "[aria-label*='Settings']"
            ]
            
            settings_found = False
            for selector in settings_selectors:
                try:
                    element = await browser_manager.page.query_selector(selector)
                    if element and await element.is_visible():
                        print(f"✅ 설정 메뉴 발견: {selector}")
                        
                        # 요소 정보 수집
                        tag_name = await element.evaluate("el => el.tagName.toLowerCase()")
                        classes = await element.get_attribute("class")
                        text_content = await element.text_content()
                        
                        print(f"  - 태그: <{tag_name}>")
                        print(f"  - 클래스: {classes}")
                        print(f"  - 텍스트: {text_content}")
                        
                        settings_found = True
                        break
                except:
                    continue
            
            if not settings_found:
                print("❌ 설정 메뉴를 찾을 수 없음")
                print("🔍 다른 방법으로 설정 관련 요소 찾기...")
                
                # 텍스트 기반으로 설정 관련 요소 찾기
                settings_texts = ["설정", "Settings", "Config", "Configuration", "Preferences", "옵션", "Options"]
                for text in settings_texts:
                    try:
                        elements = await browser_manager.page.query_selector_all(f":has-text('{text}')")
                        for elem in elements:
                            try:
                                if await elem.is_visible():
                                    tag_name = await elem.evaluate("el => el.tagName.toLowerCase()")
                                    classes = await elem.get_attribute("class")
                                    elem_text = await elem.text_content()
                                    
                                    print(f"✅ 설정 관련 텍스트 발견: {text}")
                                    print(f"  - 태그: <{tag_name}>")
                                    print(f"  - 클래스: {classes}")
                                    print(f"  - 텍스트: {elem_text}")
                                    
                                    settings_found = True
                                    break
                            except:
                                continue
                        if settings_found:
                            break
                    except:
                        continue
                
        except Exception as e:
            print(f"❌ 설정 메뉴 찾기 실패: {e}")
        
        # 3. 설정 메뉴 클릭 시도
        print("\n📋 3. 설정 메뉴 클릭 시도")
        print("-" * 30)
        
        try:
            # 글로벌 네비게이션의 click_settings 메서드 사용
            await global_nav.click_settings()
            print("✅ 설정 메뉴 클릭 성공")
            
            # 클릭 후 잠시 대기
            await asyncio.sleep(2)
            
            # 4. 설정 메뉴 클릭 후 나타나는 요소들 분석
            print("\n📋 4. 설정 메뉴 클릭 후 나타나는 요소들 분석")
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
                "[class*='overlay']"
            ]
            
            modal_found = False
            for selector in modal_selectors:
                try:
                    elements = await browser_manager.page.query_selector_all(selector)
                    for elem in elements:
                        try:
                            if await elem.is_visible():
                                tag_name = await elem.evaluate("el => el.tagName.toLowerCase()")
                                classes = await elem.get_attribute("class")
                                text_content = await elem.text_content()
                                
                                print(f"✅ 모달/드롭다운 발견: {selector}")
                                print(f"  - 태그: <{tag_name}>")
                                print(f"  - 클래스: {classes}")
                                print(f"  - 텍스트: {text_content[:100]}...")
                                
                                # 모달 내부의 메뉴 아이템들 찾기
                                menu_items = await elem.query_selector_all("li, .menu-item, .dropdown-item, button, a")
                                print(f"  - 메뉴 아이템 개수: {len(menu_items)}")
                                
                                for i, item in enumerate(menu_items[:10]):  # 처음 10개만
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
                
        except Exception as e:
            print(f"❌ 설정 메뉴 클릭 실패: {e}")
            print("🔍 직접 설정 관련 요소 찾기...")
            
            # 직접 설정 관련 요소 찾기
            try:
                # 페이지 전체에서 설정 관련 요소 찾기
                settings_keywords = ["설정", "Settings", "Config", "Configuration", "Preferences", "옵션", "Options"]
                for keyword in settings_keywords:
                    try:
                        elements = await browser_manager.page.query_selector_all(f":has-text('{keyword}')")
                        for elem in elements:
                            try:
                                if await elem.is_visible():
                                    tag_name = await elem.evaluate("el => el.tagName.toLowerCase()")
                                    classes = await elem.get_attribute("class")
                                    elem_text = await elem.text_content()
                                    
                                    print(f"✅ 설정 관련 요소 발견: {keyword}")
                                    print(f"  - 태그: <{tag_name}>")
                                    print(f"  - 클래스: {classes}")
                                    print(f"  - 텍스트: {elem_text}")
                                    
                                    # 클릭 가능한지 확인
                                    is_clickable = await elem.evaluate("el => el.tagName === 'BUTTON' || el.tagName === 'A' || el.onclick || el.getAttribute('role') === 'button'")
                                    print(f"  - 클릭 가능: {is_clickable}")
                                    
                                    if is_clickable:
                                        print("  - 클릭 시도...")
                                        try:
                                            await elem.click()
                                            await asyncio.sleep(2)
                                            print("  - 클릭 성공, 잠시 대기 후 페이지 상태 확인")
                                        except Exception as click_error:
                                            print(f"  - 클릭 실패: {click_error}")
                                    
                            except Exception as elem_error:
                                continue
                    except:
                        continue
                        
            except Exception as search_error:
                print(f"❌ 설정 관련 요소 검색 실패: {search_error}")
        
        # 5. 스크린샷 저장
        print("\n📋 5. 스크린샷 저장")
        print("-" * 30)
        
        try:
            screenshot_path = await browser_manager.page.screenshot(path="reports/dev/screenshots/settings_menu_analysis.png")
            print(f"📸 스크린샷 저장: {screenshot_path}")
        except Exception as e:
            print(f"❌ 스크린샷 저장 실패: {e}")
        
        print("\n" + "=" * 60)
        print("✅ 설정 메뉴 요소 분석 완료")
        print("=" * 60)
        
        return True

async def main():
    """메인 실행 함수"""
    print("🚀 설정 메뉴 요소 분석 시작")
    print("=" * 60)
    
    try:
        success = await analyze_settings_menu_elements("dev")
        if success:
            print("✅ 설정 메뉴 요소 분석 성공!")
        else:
            print("❌ 설정 메뉴 요소 분석 실패")
    except Exception as e:
        print(f"❌ 분석 실패: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 설정 메뉴 요소 분석 완료")

if __name__ == "__main__":
    asyncio.run(main())
