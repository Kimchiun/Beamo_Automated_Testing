#!/usr/bin/env python3
"""
Settings Text Analysis Test
"Settings" 텍스트가 포함된 요소를 자세히 분석하여 톱니바퀴 버튼을 찾는 테스트
"""

import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.config_loader import get_config
from utils.browser_manager import BrowserFactory
from pages.login_page import LoginPage

async def test_settings_text_analysis(environment: str = "dev"):
    print(f"🔍 {environment.upper()} 환경에서 Settings 텍스트 분석 테스트...")
    config = get_config(environment)
    
    async with BrowserFactory.create(config) as browser_manager:
        # 1. 로그인
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
        
        await asyncio.sleep(5)
        
        # 2. "Settings" 텍스트가 포함된 모든 요소 찾기
        print("\n🔍 'Settings' 텍스트가 포함된 모든 요소 찾기...")
        settings_elements = await browser_manager.page.query_selector_all(":has-text('Settings')")
        print(f"발견된 'Settings' 요소: {len(settings_elements)}개")
        
        for i, elem in enumerate(settings_elements):
            try:
                if await elem.is_visible():
                    tag_name = await elem.evaluate('el => el.tagName.toLowerCase()')
                    text = await elem.text_content() or ""
                    classes = await elem.get_attribute("class") or ""
                    id_attr = await elem.get_attribute("id") or ""
                    
                    print(f"\n--- {i+1}번째 Settings 요소 ---")
                    print(f"태그: {tag_name}")
                    print(f"클래스: {classes}")
                    print(f"ID: {id_attr}")
                    print(f"텍스트: {text}")
                    
                    # 부모 요소 정보
                    try:
                        parent = await elem.evaluate('el => el.parentElement')
                        parent_tag = parent.tagName.toLowerCase()
                        parent_classes = parent.className or ""
                        print(f"부모 태그: {parent_tag}")
                        print(f"부모 클래스: {parent_classes}")
                    except:
                        pass
                    
                    # HTML 구조
                    try:
                        html = await elem.evaluate('el => el.outerHTML')
                        print(f"HTML: {html}")
                    except:
                        pass
                    
                    # 클릭 가능한지 확인
                    try:
                        is_clickable = await elem.evaluate('''(el) => {
                            const style = window.getComputedStyle(el);
                            return style.cursor === 'pointer' || 
                                   el.onclick || 
                                   el.getAttribute('onclick') ||
                                   el.tagName.toLowerCase() === 'button' ||
                                   el.tagName.toLowerCase() === 'a' ||
                                   el.getAttribute('role') === 'button';
                        }''')
                        print(f"클릭 가능: {is_clickable}")
                    except:
                        print("클릭 가능 여부 확인 실패")
                    
            except Exception as e:
                print(f"   {i+1}. 요소 분석 실패: {e}")
        
        # 3. "Settings" 텍스트 주변의 클릭 가능한 요소 찾기
        print("\n🔍 'Settings' 텍스트 주변의 클릭 가능한 요소 찾기...")
        
        # 헤더 영역에서 클릭 가능한 요소들 찾기
        header_selectors = [
            "[class*='header']",
            "[class*='nav']",
            "[class*='toolbar']"
        ]
        
        for selector in header_selectors:
            try:
                elements = await browser_manager.page.query_selector_all(selector)
                for elem in elements:
                    try:
                        if await elem.is_visible():
                            text = await elem.text_content() or ""
                            if "Settings" in text:
                                print(f"\n⭐ 헤더 영역에서 'Settings' 포함 요소 발견: {selector}")
                                print(f"클래스: {await elem.get_attribute('class') or ''}")
                                print(f"텍스트: {text}")
                                
                                # 이 요소 내부의 클릭 가능한 요소들 찾기
                                clickable_children = await elem.query_selector_all("button, a, [role='button'], [onclick], [class*='clickable'], [class*='button']")
                                print(f"클릭 가능한 자식 요소: {len(clickable_children)}개")
                                
                                for j, child in enumerate(clickable_children):
                                    try:
                                        if await child.is_visible():
                                            child_text = await child.text_content() or ""
                                            child_classes = await child.get_attribute("class") or ""
                                            if "Settings" in child_text:
                                                print(f"   ⭐ {j+1}. Settings 관련 클릭 가능한 요소:")
                                                print(f"      태그: {await child.evaluate('el => el.tagName.toLowerCase')}")
                                                print(f"      클래스: {child_classes}")
                                                print(f"      텍스트: {child_text}")
                                                print(f"      HTML: {await child.evaluate('el => el.outerHTML')}")
                                    except:
                                        continue
                    except:
                        continue
            except Exception as e:
                continue
        
        # 4. "Settings" 텍스트를 포함하는 가장 작은 클릭 가능한 요소 찾기
        print("\n🔍 'Settings' 텍스트를 포함하는 가장 작은 클릭 가능한 요소 찾기...")
        
        # 모든 클릭 가능한 요소에서 "Settings" 검색
        clickable_selectors = [
            "button",
            "a", 
            "[role='button']",
            "[onclick]",
            "[class*='clickable']",
            "[class*='button']",
            "[class*='link']"
        ]
        
        for selector in clickable_selectors:
            try:
                elements = await browser_manager.page.query_selector_all(selector)
                for elem in elements:
                    try:
                        if await elem.is_visible():
                            text = await elem.text_content() or ""
                            if "Settings" in text:
                                classes = await elem.get_attribute("class") or ""
                                tag_name = await elem.evaluate('el => el.tagName.toLowerCase()')
                                
                                print(f"\n⭐ Settings 포함 클릭 가능한 요소 발견:")
                                print(f"셀렉터: {selector}")
                                print(f"태그: {tag_name}")
                                print(f"클래스: {classes}")
                                print(f"텍스트: {text}")
                                print(f"HTML: {await elem.evaluate('el => el.outerHTML')}")
                                
                                # 이 요소가 실제로 클릭 가능한지 확인
                                try:
                                    is_clickable = await elem.evaluate('''(el) => {
                                        const style = window.getComputedStyle(el);
                                        return style.cursor === 'pointer' || 
                                               el.onclick || 
                                               el.getAttribute('onclick') ||
                                               el.tagName.toLowerCase() === 'button' ||
                                               el.tagName.toLowerCase() === 'a' ||
                                               el.getAttribute('role') === 'button';
                                    }''')
                                    print(f"클릭 가능 여부: {is_clickable}")
                                except:
                                    print("클릭 가능 여부 확인 실패")
                                
                    except:
                        continue
            except Exception as e:
                continue
        
        # 5. 스크린샷 저장
        print("\n📸 분석 결과 스크린샷 저장...")
        await browser_manager.page.screenshot(path="reports/dev/screenshots/settings_text_analysis.png")
        
        # 6. 결과 요약
        print("\n" + "=" * 80)
        print("📊 Settings 텍스트 분석 결과")
        print("=" * 80)
        print(f"📸 스크린샷: reports/dev/screenshots/settings_text_analysis.png")
        print(f"🔍 발견된 Settings 요소: {len(settings_elements)}개")
        
        return True

async def main():
    """메인 실행 함수"""
    try:
        result = await test_settings_text_analysis("dev")
        if result:
            print("\n🎉 테스트 완료!")
        else:
            print("\n❌ 테스트 실패")
    except Exception as e:
        print(f"\n💥 테스트 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
