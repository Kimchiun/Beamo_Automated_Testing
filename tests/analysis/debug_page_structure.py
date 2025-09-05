#!/usr/bin/env python3
"""
Debug Page Structure
페이지의 실제 HTML 구조를 확인하고 톱니바퀴 버튼의 정확한 위치를 파악하는 디버깅 테스트
"""

import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.config_loader import get_config
from utils.browser_manager import BrowserFactory
from pages.login_page import LoginPage

async def debug_page_structure(environment: str = "dev"):
    print(f"🔍 {environment.upper()} 환경에서 페이지 구조 디버깅...")
    config = get_config(environment)
    
    async with BrowserFactory.create(config) as browser_manager:
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
        
        await asyncio.sleep(3)
        
        print("\n" + "=" * 80)
        print("🔍 페이지 구조 상세 분석")
        print("=" * 80)
        
        # 1. 페이지 전체 HTML 구조 확인
        print("📄 페이지 전체 HTML 구조 분석...")
        page_html = await browser_manager.page.content()
        
        # HTML 파일로 저장
        with open("reports/dev/debug_page_structure.html", "w", encoding="utf-8") as f:
            f.write(page_html)
        print("📁 전체 HTML 저장: reports/dev/debug_page_structure.html")
        
        # 2. 톱니바퀴 이모지가 포함된 모든 요소 찾기
        print("\n🔍 톱니바퀴 이모지(⚙️) 검색...")
        gear_elements = await browser_manager.page.query_selector_all(":has-text('⚙️')")
        print(f"⚙️ 이모지가 포함된 요소: {len(gear_elements)}개")
        
        for i, elem in enumerate(gear_elements):
            try:
                tag_name = await elem.evaluate('el => el.tagName.toLowerCase()')
                text = await elem.text_content() or ""
                classes = await elem.get_attribute("class") or ""
                id_attr = await elem.get_attribute("id") or ""
                parent_classes = ""
                try:
                    parent = await elem.evaluate('el => el.parentElement.className')
                    parent_classes = parent or ""
                except:
                    pass
                
                print(f"   {i+1}. {tag_name} (id='{id_attr}', class='{classes}')")
                print(f"      텍스트: {text}")
                print(f"      부모 클래스: {parent_classes}")
                print(f"      HTML: {await elem.evaluate('el => el.outerHTML')}")
                print()
            except Exception as e:
                print(f"   {i+1}. 요소 분석 실패: {e}")
        
        # 3. 모든 버튼 요소 상세 분석
        print("\n🔍 모든 버튼 요소 상세 분석...")
        buttons = await browser_manager.page.query_selector_all("button")
        print(f"발견된 버튼 수: {len(buttons)}")
        
        for i, button in enumerate(buttons):
            try:
                if await button.is_visible():
                    text = await button.text_content() or ""
                    classes = await button.get_attribute("class") or ""
                    id_attr = await button.get_attribute("id") or ""
                    title = await button.get_attribute("title") or ""
                    aria_label = await button.get_attribute("aria-label") or ""
                    
                    # 톱니바퀴 관련 키워드가 포함된 버튼 강조
                    is_gear_related = any(keyword in (classes + text + title + aria_label).lower() 
                                        for keyword in ['gear', 'cog', 'settings', 'config', '⚙️'])
                    
                    marker = "⭐" if is_gear_related else "  "
                    print(f"{marker} {i+1:2d}. {tag_name} (id='{id_attr}', class='{classes}')")
                    print(f"      텍스트: {text}")
                    print(f"      title: {title}")
                    print(f"      aria-label: {aria_label}")
                    if is_gear_related:
                        print(f"      ⭐ 톱니바퀴 관련 버튼 발견!")
                        print(f"      HTML: {await button.evaluate('el => el.outerHTML')}")
                    print()
            except Exception as e:
                print(f"   {i+1}. 버튼 분석 실패: {e}")
        
        # 4. 모든 링크 요소 상세 분석
        print("\n🔍 모든 링크 요소 상세 분석...")
        links = await browser_manager.page.query_selector_all("a")
        print(f"발견된 링크 수: {len(links)}")
        
        for i, link in enumerate(links):
            try:
                if await link.is_visible():
                    text = await link.text_content() or ""
                    classes = await link.get_attribute("class") or ""
                    href = await link.get_attribute("href") or ""
                    title = await link.get_attribute("title") or ""
                    
                    # 톱니바퀴 관련 키워드가 포함된 링크 강조
                    is_gear_related = any(keyword in (classes + text + title).lower() 
                                        for keyword in ['gear', 'cog', 'settings', 'config', '⚙️'])
                    
                    marker = "⭐" if is_gear_related else "  "
                    print(f"{marker} {i+1:2d}. a (href='{href}', class='{classes}')")
                    print(f"      텍스트: {text}")
                    print(f"      title: {title}")
                    if is_gear_related:
                        print(f"      ⭐ 톱니바퀴 관련 링크 발견!")
                        print(f"      HTML: {await link.evaluate('el => el.outerHTML')}")
                    print()
            except Exception as e:
                print(f"   {i+1}. 링크 분석 실패: {e}")
        
        # 5. 모든 SVG 요소 상세 분석
        print("\n🔍 모든 SVG 요소 상세 분석...")
        svgs = await browser_manager.page.query_selector_all("svg")
        print(f"발견된 SVG 수: {len(svgs)}")
        
        for i, svg in enumerate(svgs):
            try:
                if await svg.is_visible():
                    classes = await svg.get_attribute("class") or ""
                    parent_classes = ""
                    parent_tag = ""
                    try:
                        parent = await svg.evaluate('el => el.parentElement')
                        parent_classes = parent.className or ""
                        parent_tag = parent.tagName.toLowerCase()
                    except:
                        pass
                    
                    # 톱니바퀴 관련 키워드가 포함된 SVG 강조
                    is_gear_related = any(keyword in (classes + parent_classes).lower() 
                                        for keyword in ['gear', 'cog', 'settings', 'config'])
                    
                    marker = "⭐" if is_gear_related else "  "
                    print(f"{marker} {i+1:2d}. svg (class='{classes}')")
                    print(f"      부모: {parent_tag} (class='{parent_classes}')")
                    if is_gear_related:
                        print(f"      ⭐ 톱니바퀴 관련 SVG 발견!")
                        print(f"      HTML: {await svg.evaluate('el => el.outerHTML')}")
                    print()
            except Exception as e:
                print(f"   {i+1}. SVG 분석 실패: {e}")
        
        # 6. 우측 상단 영역 특별 분석
        print("\n🔍 우측 상단 영역 특별 분석...")
        try:
            # 우측 상단 영역의 모든 요소 검색
            right_top_selectors = [
                "[class*='header']",
                "[class*='top']", 
                "[class*='right']",
                "[class*='nav']",
                "[class*='toolbar']",
                "[class*='actions']"
            ]
            
            for selector in right_top_selectors:
                elements = await browser_manager.page.query_selector_all(selector)
                for elem in elements:
                    try:
                        if await elem.is_visible():
                            classes = await elem.get_attribute("class") or ""
                            text = await elem.text_content() or ""
                            
                            # 톱니바퀴 관련 키워드가 포함된 요소 강조
                            if any(keyword in (classes + text).lower() 
                                   for keyword in ['gear', 'cog', 'settings', 'config', '⚙️']):
                                print(f"   ⭐ 우측 상단 톱니바퀴 관련 요소: {selector}")
                                print(f"      클래스: {classes}")
                                print(f"      텍스트: {text}")
                                print(f"      HTML: {await elem.evaluate('el => el.outerHTML')}")
                                print()
                    except:
                        continue
        except Exception as e:
            print(f"   우측 상단 영역 분석 실패: {e}")
        
        # 7. 스크린샷 저장
        print("\n📸 디버깅용 스크린샷 저장...")
        screenshot = await browser_manager.page.screenshot(path="reports/dev/screenshots/debug_page_structure.png")
        print(f"📸 스크린샷 저장: {screenshot}")
        
        # 8. 결과 요약
        print("\n" + "=" * 80)
        print("📊 페이지 구조 디버깅 결과")
        print("=" * 80)
        print(f"📄 전체 HTML: reports/dev/debug_page_structure.html")
        print(f"📸 스크린샷: reports/dev/screenshots/debug_page_structure.png")
        print(f"⚙️ 톱니바퀴 이모지 요소: {len(gear_elements)}개")
        print(f"🔘 버튼 요소: {len(buttons)}개")
        print(f"🔗 링크 요소: {len(links)}개")
        print(f"🎨 SVG 요소: {len(svgs)}개")
        
        return True

async def main():
    """메인 실행 함수"""
    try:
        result = await debug_page_structure("dev")
        if result:
            print("\n🎉 디버깅 완료!")
        else:
            print("\n❌ 디버깅 실패")
    except Exception as e:
        print(f"\n💥 디버깅 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
