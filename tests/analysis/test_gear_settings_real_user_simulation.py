#!/usr/bin/env python3
"""
Real User Simulation Test
실제 사용자와 동일한 상태를 시뮬레이션하여 톱니바퀴 버튼을 찾는 테스트
"""

import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.config_loader import get_config
from utils.browser_manager import BrowserFactory
from pages.login_page import LoginPage

async def test_gear_settings_real_user_simulation(environment: str = "dev"):
    print(f"🔍 {environment.upper()} 환경에서 실제 사용자 시뮬레이션 테스트...")
    config = get_config(environment)
    
    async with BrowserFactory.create(config) as browser_manager:
        # 1. 브라우저 초기화 및 사용자 에이전트 설정
        print("🌐 브라우저 초기화 및 사용자 에이전트 설정...")
        await browser_manager.page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # 2. 로그인 페이지로 이동
        login_page = LoginPage(browser_manager.page, config)
        await login_page.navigate_to_login()
        await login_page.wait_for_page_load()
        
        # 3. 로그인 전 스크린샷
        print("📸 로그인 전 스크린샷 저장...")
        await browser_manager.page.screenshot(path="reports/dev/screenshots/real_user_login_before.png")
        
        # 4. 로그인 수행
        space_id = "d-ge-pr"
        email = config.test_data.valid_user["email"]
        password = config.test_data.valid_user["password"]
        
        print(f"🔐 로그인 시도: {email}")
        await login_page.login(space_id, email, password)
        
        # 5. 로그인 성공 확인
        if not await login_page.is_logged_in():
            print("❌ 로그인 실패")
            return False
        print("✅ 로그인 성공")
        
        # 6. 로그인 후 충분한 대기 시간
        print("⏳ 로그인 후 페이지 완전 로딩 대기...")
        await asyncio.sleep(5)
        
        # 7. 로그인 후 스크린샷
        print("📸 로그인 후 스크린샷 저장...")
        await browser_manager.page.screenshot(path="reports/dev/screenshots/real_user_login_after.png")
        
        # 8. 페이지 제목과 URL 확인
        page_title = await browser_manager.page.title()
        page_url = browser_manager.page.url
        print(f"📄 페이지 제목: {page_title}")
        print(f"🔗 페이지 URL: {page_url}")
        
        # 9. 페이지 전체 HTML 저장
        print("📄 페이지 전체 HTML 저장...")
        page_html = await browser_manager.page.content()
        with open("reports/dev/real_user_page_structure.html", "w", encoding="utf-8") as f:
            f.write(page_html)
        
        # 10. 톱니바퀴 버튼 검색 (다양한 방법)
        print("\n🔍 톱니바퀴 버튼 검색 시작...")
        
        # 10-1. 이모지 검색
        print("   🔍 이모지(⚙️) 검색...")
        gear_emoji_elements = await browser_manager.page.query_selector_all(":has-text('⚙️')")
        print(f"      발견된 이모지 요소: {len(gear_emoji_elements)}개")
        
        for i, elem in enumerate(gear_emoji_elements):
            try:
                if await elem.is_visible():
                    tag_name = await elem.evaluate('el => el.tagName.toLowerCase()')
                    text = await elem.text_content() or ""
                    classes = await elem.get_attribute("class") or ""
                    print(f"         {i+1}. {tag_name} (class='{classes}') - 텍스트: {text}")
            except Exception as e:
                print(f"         {i+1}. 요소 분석 실패: {e}")
        
        # 10-2. 모든 버튼 요소 검색
        print("   🔍 모든 버튼 요소 검색...")
        all_buttons = await browser_manager.page.query_selector_all("button")
        print(f"      발견된 버튼 수: {len(all_buttons)}개")
        
        gear_related_buttons = []
        for i, button in enumerate(all_buttons):
            try:
                if await button.is_visible():
                    text = await button.text_content() or ""
                    classes = await button.get_attribute("class") or ""
                    title = await button.get_attribute("title") or ""
                    aria_label = await button.get_attribute("aria-label") or ""
                    
                    # 톱니바퀴 관련 키워드가 포함된 버튼 찾기
                    if any(keyword in (classes + text + title + aria_label).lower() 
                           for keyword in ['gear', 'cog', 'settings', 'config', '⚙️']):
                        gear_related_buttons.append(button)
                        print(f"         ⭐ {i+1}. 톱니바퀴 관련 버튼 발견!")
                        print(f"            텍스트: {text}")
                        print(f"            클래스: {classes}")
                        print(f"            title: {title}")
                        print(f"            aria-label: {aria_label}")
            except Exception as e:
                continue
        
        # 10-3. 모든 링크 요소 검색
        print("   🔍 모든 링크 요소 검색...")
        all_links = await browser_manager.page.query_selector_all("a")
        print(f"      발견된 링크 수: {len(all_links)}개")
        
        gear_related_links = []
        for i, link in enumerate(all_links):
            try:
                if await link.is_visible():
                    text = await link.text_content() or ""
                    classes = await link.get_attribute("class") or ""
                    href = await link.get_attribute("href") or ""
                    
                    if any(keyword in (classes + text).lower() 
                           for keyword in ['gear', 'cog', 'settings', 'config', '⚙️']):
                        gear_related_links.append(link)
                        print(f"         ⭐ {i+1}. 톱니바퀴 관련 링크 발견!")
                        print(f"            텍스트: {text}")
                        print(f"            클래스: {classes}")
                        print(f"            href: {href}")
            except Exception as e:
                continue
        
        # 10-4. 모든 SVG 요소 검색
        print("   🔍 모든 SVG 요소 검색...")
        all_svgs = await browser_manager.page.query_selector_all("svg")
        print(f"      발견된 SVG 수: {len(all_svgs)}개")
        
        gear_related_svgs = []
        for i, svg in enumerate(all_svgs):
            try:
                if await svg.is_visible():
                    classes = await svg.get_attribute("class") or ""
                    parent_classes = ""
                    try:
                        parent = await svg.evaluate('el => el.parentElement.className')
                        parent_classes = parent or ""
                    except:
                        pass
                    
                    if any(keyword in (classes + parent_classes).lower() 
                           for keyword in ['gear', 'cog', 'settings', 'config']):
                        gear_related_svgs.append(svg)
                        print(f"         ⭐ {i+1}. 톱니바퀴 관련 SVG 발견!")
                        print(f"            클래스: {classes}")
                        print(f"            부모 클래스: {parent_classes}")
            except Exception as e:
                continue
        
        # 10-5. 페이지 전체에서 특정 텍스트 검색
        print("   🔍 페이지 전체에서 특정 텍스트 검색...")
        
        # 톱니바퀴 관련 키워드로 검색
        search_keywords = ['⚙️', 'gear', 'cog', 'settings', 'config', '설정', '기어']
        for keyword in search_keywords:
            try:
                elements = await browser_manager.page.query_selector_all(f":has-text('{keyword}')")
                if elements:
                    print(f"         '{keyword}' 포함 요소: {len(elements)}개")
                    for j, elem in enumerate(elements[:3]):  # 처음 3개만 표시
                        try:
                            if await elem.is_visible():
                                tag_name = await elem.evaluate('el => el.tagName.toLowerCase()')
                                text = await elem.text_content() or ""
                                classes = await elem.get_attribute("class") or ""
                                print(f"            {j+1}. {tag_name} (class='{classes}') - 텍스트: {text[:50]}...")
                        except:
                            continue
            except Exception as e:
                continue
        
        # 11. 우측 상단 영역 특별 검색
        print("\n🔍 우측 상단 영역 특별 검색...")
        
        # 우측 상단 영역의 모든 요소 검색
        right_top_selectors = [
            "[class*='header']",
            "[class*='top']", 
            "[class*='right']",
            "[class*='nav']",
            "[class*='toolbar']",
            "[class*='actions']",
            "[class*='menu']"
        ]
        
        for selector in right_top_selectors:
            try:
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
                    except:
                        continue
            except Exception as e:
                continue
        
        # 12. 결과 요약
        print("\n" + "=" * 80)
        print("📊 실제 사용자 시뮬레이션 테스트 결과")
        print("=" * 80)
        print(f"📄 전체 HTML: reports/dev/real_user_page_structure.html")
        print(f"📸 로그인 전: reports/dev/screenshots/real_user_login_before.png")
        print(f"📸 로그인 후: reports/dev/screenshots/real_user_login_after.png")
        print(f"⚙️ 톱니바퀴 이모지 요소: {len(gear_emoji_elements)}개")
        print(f"🔘 톱니바퀴 관련 버튼: {len(gear_related_buttons)}개")
        print(f"🔗 톱니바퀴 관련 링크: {len(gear_related_links)}개")
        print(f"🎨 톱니바퀴 관련 SVG: {len(gear_related_svgs)}개")
        
        # 13. 최종 스크린샷
        print("\n📸 최종 스크린샷 저장...")
        await browser_manager.page.screenshot(path="reports/dev/screenshots/real_user_simulation_final.png")
        
        if len(gear_related_buttons) > 0 or len(gear_related_links) > 0 or len(gear_related_svgs) > 0:
            print("🎉 톱니바퀴 관련 요소 발견!")
            return True
        else:
            print("❌ 톱니바퀴 관련 요소를 찾을 수 없습니다")
            return False

async def main():
    """메인 실행 함수"""
    try:
        result = await test_gear_settings_real_user_simulation("dev")
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
