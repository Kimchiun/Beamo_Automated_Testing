#!/usr/bin/env python3
"""
Global Navigation Elements Analysis
글로벌 네비게이션의 모든 요소들을 분석합니다.
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

async def analyze_global_navigation_elements(environment: str = "dev"):
    """글로벌 네비게이션 요소 분석"""
    print(f"🔍 {environment.upper()} 환경에서 글로벌 네비게이션 요소 분석...")
    
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
        print("🔍 글로벌 네비게이션 요소 분석")
        print("=" * 80)
        
        # 1. 글로벌 네비게이션 로드 확인
        print("\n📋 1. 글로벌 네비게이션 로드 확인")
        print("-" * 50)
        
        try:
            await global_nav.wait_for_navigation_load()
            print("✅ 글로벌 네비게이션 로드 완료")
        except Exception as e:
            print(f"❌ 글로벌 네비게이션 로드 실패: {e}")
            return False
        
        # 2. 글로벌 네비게이션 영역 찾기
        print("\n📋 2. 글로벌 네비게이션 영역 찾기")
        print("-" * 50)
        
        nav_selectors = [
            "nav",
            ".navigation",
            ".global-nav",
            ".header",
            ".top-bar",
            ".main-nav",
            "[class*='nav']",
            "[class*='header']",
            "[class*='top']",
            "[class*='menu']"
        ]
        
        nav_found = False
        for selector in nav_selectors:
            try:
                nav_elements = await browser_manager.page.query_selector_all(selector)
                for nav_elem in nav_elements:
                    try:
                        if await nav_elem.is_visible():
                            nav_tag = await nav_elem.evaluate("el => el.tagName.toLowerCase()")
                            nav_classes = await nav_elem.get_attribute("class")
                            nav_text = await nav_elem.text_content()
                            
                            print(f"✅ 네비게이션 영역 발견: {selector}")
                            print(f"  - 태그: <{nav_tag}>")
                            print(f"  - 클래스: {nav_classes}")
                            print(f"  - 텍스트: {nav_text[:100]}...")
                            
                            nav_found = True
                            break
                    except:
                        continue
                if nav_found:
                    break
            except:
                continue
        
        if not nav_found:
            print("❌ 네비게이션 영역을 찾을 수 없음")
        
        # 3. 모든 클릭 가능한 요소 찾기
        print("\n📋 3. 글로벌 네비게이션의 모든 클릭 가능한 요소 찾기")
        print("-" * 50)
        
        clickable_selectors = [
            "button",
            "a",
            "[role='button']",
            "[onclick]",
            "[class*='btn']",
            "[class*='button']",
            "[class*='link']",
            "[class*='nav-item']",
            "[class*='menu-item']"
        ]
        
        all_clickable = []
        for selector in clickable_selectors:
            try:
                elements = await browser_manager.page.query_selector_all(selector)
                for elem in elements:
                    try:
                        if await elem.is_visible():
                            # 부모가 글로벌 네비게이션 영역인지 확인
                            parent_nav = await elem.evaluate("""
                                el => {
                                    let parent = el.parentElement;
                                    while (parent) {
                                        if (parent.tagName === 'NAV' || 
                                            parent.className.includes('nav') || 
                                            parent.className.includes('header') ||
                                            parent.className.includes('top')) {
                                            return true;
                                        }
                                        parent = parent.parentElement;
                                    }
                                    return false;
                                }
                            """)
                            
                            if parent_nav:
                                tag_name = await elem.evaluate("el => el.tagName.toLowerCase()")
                                classes = await elem.get_attribute("class")
                                elem_text = await elem.text_content()
                                href = await elem.get_attribute("href")
                                title = await elem.get_attribute("title")
                                aria_label = await elem.get_attribute("aria-label")
                                
                                all_clickable.append({
                                    "tag": tag_name,
                                    "classes": classes,
                                    "text": elem_text,
                                    "href": href,
                                    "title": title,
                                    "aria_label": aria_label,
                                    "selector": selector
                                })
                    except:
                        continue
            except:
                continue
        
        print(f"📊 글로벌 네비게이션에서 발견된 클릭 가능한 요소: {len(all_clickable)}개")
        
        if all_clickable:
            print("\n📋 발견된 요소들:")
            for i, elem in enumerate(all_clickable):
                print(f"\n{i+1}. <{elem['tag']}>")
                print(f"   - 텍스트: {elem['text']}")
                print(f"   - 클래스: {elem['classes']}")
                print(f"   - href: {elem['href']}")
                print(f"   - title: {elem['title']}")
                print(f"   - aria-label: {elem['aria_label']}")
                print(f"   - 셀렉터: {elem['selector']}")
        
        # 4. 특정 패턴의 요소들 찾기
        print("\n📋 4. 특정 패턴의 요소들 찾기")
        print("-" * 50)
        
        # 로고 관련
        logo_selectors = [
            "[class*='logo']",
            "[class*='brand']",
            "img[alt*='logo']",
            "img[alt*='brand']",
            "a[href='/']",
            "a[href='/dashboard']"
        ]
        
        print("🔍 로고 관련 요소:")
        for selector in logo_selectors:
            try:
                elements = await browser_manager.page.query_selector_all(selector)
                for elem in elements:
                    if await elem.is_visible():
                        tag_name = await elem.evaluate("el => el.tagName.toLowerCase()")
                        classes = await elem.get_attribute("class")
                        alt = await elem.get_attribute("alt")
                        href = await elem.get_attribute("href")
                        print(f"  ✅ {selector}: <{tag_name}> 클래스:{classes} alt:{alt} href:{href}")
            except:
                continue
        
        # 사용자 관련
        user_selectors = [
            "[class*='user']",
            "[class*='profile']",
            "[class*='avatar']",
            "[class*='account']",
            "img[alt*='user']",
            "img[alt*='profile']"
        ]
        
        print("\n🔍 사용자 관련 요소:")
        for selector in user_selectors:
            try:
                elements = await browser_manager.page.query_selector_all(selector)
                for elem in elements:
                    if await elem.is_visible():
                        tag_name = await elem.evaluate("el => el.tagName.toLowerCase()")
                        classes = await elem.get_attribute("class")
                        alt = await elem.get_attribute("alt")
                        print(f"  ✅ {selector}: <{tag_name}> 클래스:{classes} alt:{alt}")
            except:
                continue
        
        # 알림 관련
        notification_selectors = [
            "[class*='notification']",
            "[class*='alert']",
            "[class*='bell']",
            "[class*='message']",
            "[class*='badge']"
        ]
        
        print("\n🔍 알림 관련 요소:")
        for selector in notification_selectors:
            try:
                elements = await browser_manager.page.query_selector_all(selector)
                for elem in elements:
                    if await elem.is_visible():
                        tag_name = await elem.evaluate("el => el.tagName.toLowerCase()")
                        classes = await elem.get_attribute("class")
                        elem_text = await elem.text_content()
                        print(f"  ✅ {selector}: <{tag_name}> 클래스:{classes} 텍스트:{elem_text}")
            except:
                continue
        
        # 5. 페이지 전체에서 글로벌 네비게이션 관련 요소 찾기
        print("\n📋 5. 페이지 전체에서 글로벌 네비게이션 관련 요소 찾기")
        print("-" * 50)
        
        # 모든 버튼과 링크 확인
        all_elements = await browser_manager.page.query_selector_all("button, a, [role='button'], [class*='btn'], [class*='nav'], [class*='menu']")
        print(f"페이지의 총 요소 개수: {len(all_elements)}")
        
        nav_related = []
        for i, elem in enumerate(all_elements[:100]):  # 처음 100개만 확인
            try:
                if await elem.is_visible():
                    elem_text = await elem.text_content()
                    elem_classes = await elem.get_attribute("class")
                    elem_tag = await elem.evaluate("el => el.tagName.toLowerCase()")
                    
                    # 네비게이션 관련 키워드가 있는지 확인
                    nav_keywords = ["nav", "menu", "header", "top", "logo", "user", "profile", "settings", "config", "gear", "cog", "notification", "alert", "search", "home", "dashboard"]
                    
                    for keyword in nav_keywords:
                        if (elem_text and keyword.lower() in elem_text.lower()) or (elem_classes and keyword.lower() in elem_classes.lower()):
                            nav_related.append({
                                "index": i,
                                "tag": elem_tag,
                                "text": elem_text,
                                "classes": elem_classes
                            })
                            break
            except:
                continue
        
        if nav_related:
            print(f"\n📊 네비게이션 관련 후보 요소들: {len(nav_related)}개")
            for elem in nav_related:
                print(f"  - {elem['index']}: <{elem['tag']}> {elem['text']} (클래스: {elem['classes']})")
        
        # 6. 스크린샷 저장
        print("\n📋 6. 스크린샷 저장")
        print("-" * 50)
        
        try:
            screenshot_path = await browser_manager.page.screenshot(path="reports/dev/screenshots/global_navigation_analysis.png")
            print(f"📸 스크린샷 저장: {screenshot_path}")
        except Exception as e:
            print(f"❌ 스크린샷 저장 실패: {e}")
        
        print("\n" + "=" * 80)
        print("✅ 글로벌 네비게이션 요소 분석 완료")
        print("=" * 80)
        
        return True

async def main():
    """메인 실행 함수"""
    print("🚀 글로벌 네비게이션 요소 분석 시작")
    print("=" * 80)
    
    try:
        success = await analyze_global_navigation_elements("dev")
        if success:
            print("✅ 글로벌 네비게이션 요소 분석 성공!")
        else:
            print("❌ 글로벌 네비게이션 요소 분석 실패")
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
    
    print("\n" + "=" * 80)
    print("✅ 글로벌 네비게이션 요소 분석 완료")

if __name__ == "__main__":
    asyncio.run(main())
