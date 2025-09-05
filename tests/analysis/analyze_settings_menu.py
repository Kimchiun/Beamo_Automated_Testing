#!/usr/bin/env python3
"""
Settings Menu Analysis Test
글로벌 네비게이션의 설정 메뉴를 클릭했을 때 나타나는 요소들을 분석합니다.
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

async def analyze_settings_menu(environment: str = "dev"):
    """설정 메뉴 요소 분석"""
    print(f"🔍 {environment.upper()} 환경 설정 메뉴 분석 시작...")
    
    config = get_config(environment)
    
    async with BrowserFactory.create(config) as browser_manager:
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
        
        # 글로벌 네비게이션 컴포넌트 생성
        global_nav = GlobalNavigation(browser_manager.page, config)
        
        print("\n" + "=" * 60)
        print("🔍 설정 메뉴 요소 분석")
        print("=" * 60)
        
        # 1. 설정 메뉴 버튼 찾기
        print("\n📋 1. 설정 메뉴 버튼 찾기")
        print("-" * 30)
        
        try:
            # 설정 메뉴 버튼이 있는지 확인
            settings_button = await browser_manager.page.query_selector(".settings-menu, .config-menu, .settings, .config")
            
            if settings_button:
                button_text = await settings_button.text_content()
                button_visible = await settings_button.is_visible()
                print(f"✅ 설정 메뉴 버튼 발견: '{button_text}' (가시성: {button_visible})")
                
                # 버튼의 HTML 속성들 확인
                button_attrs = await settings_button.evaluate("el => Object.fromEntries(Object.entries(el.attributes).map(([k,v]) => [k, v.value]))")
                print(f"📝 버튼 속성: {button_attrs}")
                
            else:
                print("❌ 설정 메뉴 버튼을 찾을 수 없음")
                # 대안 셀렉터들 시도
                alternative_selectors = [
                    "[data-testid*='settings']",
                    "[data-testid*='config']",
                    ".gear-icon",
                    ".settings-icon",
                    ".config-icon",
                    "button:has-text('설정')",
                    "button:has-text('Settings')",
                    "button:has-text('Config')"
                ]
                
                print("🔍 대안 셀렉터들 시도...")
                for selector in alternative_selectors:
                    try:
                        alt_button = await browser_manager.page.query_selector(selector)
                        if alt_button:
                            alt_text = await alt_button.text_content()
                            print(f"✅ 대안 셀렉터로 발견: '{selector}' -> '{alt_text}'")
                            settings_button = alt_button
                            break
                    except:
                        continue
                
                if not settings_button:
                    print("❌ 모든 대안 셀렉터 실패")
                    return False
                    
        except Exception as e:
            print(f"❌ 설정 메뉴 버튼 찾기 실패: {e}")
            return False
        
        # 2. 설정 메뉴 클릭
        print("\n📋 2. 설정 메뉴 클릭")
        print("-" * 30)
        
        try:
            # 클릭 전 스크린샷
            await browser_manager.page.screenshot(path="reports/dev/screenshots/before_settings_click.png")
            print("📸 클릭 전 스크린샷 저장")
            
            # 설정 메뉴 클릭
            await settings_button.click()
            print("✅ 설정 메뉴 클릭 성공")
            
            # 메뉴가 나타날 때까지 대기
            await asyncio.sleep(2)
            
            # 클릭 후 스크린샷
            await browser_manager.page.screenshot(path="reports/dev/screenshots/after_settings_click.png")
            print("📸 클릭 후 스크린샷 저장")
            
        except Exception as e:
            print(f"❌ 설정 메뉴 클릭 실패: {e}")
            return False
        
        # 3. 설정 메뉴 요소들 분석
        print("\n📋 3. 설정 메뉴 요소들 분석")
        print("-" * 30)
        
        try:
            # 드롭다운/팝오버 메뉴 찾기
            menu_selectors = [
                ".settings-dropdown",
                ".config-dropdown", 
                ".settings-menu",
                ".config-menu",
                ".settings-popover",
                ".config-popover",
                ".el-dropdown-menu",
                ".el-menu",
                "[role='menu']",
                "[data-testid*='settings-menu']",
                "[data-testid*='config-menu']"
            ]
            
            settings_menu = None
            for selector in menu_selectors:
                try:
                    menu = await browser_manager.page.query_selector(selector)
                    if menu and await menu.is_visible():
                        settings_menu = menu
                        print(f"✅ 설정 메뉴 발견: {selector}")
                        break
                except:
                    continue
            
            if not settings_menu:
                print("⚠️ 설정 메뉴를 찾을 수 없음 (드롭다운이 나타나지 않았을 수 있음)")
                
                # 페이지 전체에서 새로 나타난 요소들 찾기
                print("🔍 새로 나타난 요소들 찾기...")
                
                # 모든 버튼, 링크, 메뉴 아이템 찾기
                all_elements = await browser_manager.page.query_selector_all("button, a, .menu-item, .dropdown-item, .el-menu-item")
                
                visible_elements = []
                for elem in all_elements:
                    try:
                        if await elem.is_visible():
                            text = await elem.text_content()
                            tag_name = await elem.evaluate("el => el.tagName.toLowerCase()")
                            classes = await elem.get_attribute("class")
                            
                            if text and text.strip():
                                visible_elements.append({
                                    "tag": tag_name,
                                    "text": text.strip(),
                                    "classes": classes,
                                    "element": elem
                                })
                    except:
                        continue
                
                print(f"📝 가시적인 요소들 ({len(visible_elements)}개):")
                for i, elem_info in enumerate(visible_elements[:10]):  # 처음 10개만
                    print(f"  {i+1}. <{elem_info['tag']}> {elem_info['text']} (클래스: {elem_info['classes']})")
                
            else:
                # 메뉴 내부 요소들 분석
                print("🔍 설정 메뉴 내부 요소들 분석...")
                
                menu_items = await settings_menu.query_selector_all("li, .menu-item, .dropdown-item, .el-menu-item")
                print(f"📝 메뉴 아이템 개수: {len(menu_items)}")
                
                for i, item in enumerate(menu_items):
                    try:
                        text = await item.text_content()
                        tag_name = await item.evaluate("el => el.tagName.toLowerCase()")
                        classes = await item.get_attribute("class")
                        href = await item.get_attribute("href")
                        
                        if text and text.strip():
                            print(f"  {i+1}. <{tag_name}> {text.strip()}")
                            print(f"     클래스: {classes}")
                            if href:
                                print(f"     링크: {href}")
                            
                            # 하위 요소들도 확인
                            sub_elements = await item.query_selector_all("*")
                            if sub_elements:
                                sub_texts = []
                                for sub in sub_elements[:3]:  # 처음 3개만
                                    try:
                                        sub_text = await sub.text_content()
                                        if sub_text and sub_text.strip():
                                            sub_texts.append(sub_text.strip())
                                    except:
                                        continue
                                if sub_texts:
                                    print(f"     하위 요소: {', '.join(sub_texts)}")
                            print()
                            
                    except Exception as e:
                        print(f"    ⚠️ 아이템 {i+1} 분석 실패: {e}")
                        continue
                
        except Exception as e:
            print(f"❌ 설정 메뉴 요소 분석 실패: {e}")
        
        # 4. 설정 관련 페이지 요소들 찾기
        print("\n📋 4. 설정 관련 페이지 요소들 찾기")
        print("-" * 30)
        
        try:
            # 페이지에서 설정 관련 텍스트나 요소들 찾기
            settings_related = await browser_manager.page.query_selector_all(":has-text('설정'), :has-text('Settings'), :has-text('Config'), :has-text('Preferences')")
            
            print(f"📝 설정 관련 요소들 ({len(settings_related)}개):")
            for i, elem in enumerate(settings_related[:5]):  # 처음 5개만
                try:
                    text = await elem.text_content()
                    tag_name = await elem.evaluate("el => el.tagName.toLowerCase()")
                    if text and text.strip():
                        print(f"  {i+1}. <{tag_name}> {text.strip()}")
                except:
                    continue
                    
        except Exception as e:
            print(f"❌ 설정 관련 요소 찾기 실패: {e}")
        
        # 5. 최종 스크린샷
        print("\n📋 5. 최종 스크린샷")
        print("-" * 30)
        
        try:
            final_screenshot = await browser_manager.page.screenshot(path="reports/dev/screenshots/settings_analysis_final.png")
            print("📸 최종 분석 스크린샷 저장됨")
        except Exception as e:
            print(f"❌ 최종 스크린샷 저장 실패: {e}")
        
        print("\n" + "=" * 60)
        print("✅ 설정 메뉴 요소 분석 완료")
        print("=" * 60)
        
        return True

async def main():
    """메인 실행 함수"""
    print("🚀 설정 메뉴 요소 분석 시작")
    print("=" * 60)
    
    try:
        success = await analyze_settings_menu("dev")
        if success:
            print("✅ 설정 메뉴 분석 성공!")
        else:
            print("❌ 설정 메뉴 분석 실패")
    except Exception as e:
        print(f"❌ 분석 실패: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 설정 메뉴 요소 분석 완료")

if __name__ == "__main__":
    asyncio.run(main())
