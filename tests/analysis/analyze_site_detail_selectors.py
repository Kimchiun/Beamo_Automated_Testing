#!/usr/bin/env python3
"""
Analyze site detail selectors
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
from pages.dashboard_page import DashboardPage


async def analyze_site_detail_selectors():
    """Analyze site detail selectors"""
    print("🔍 사이트 상세 페이지 셀렉터 분석...")
    
    config = get_config("dev")
    
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
            return
        
        print("✅ 로그인 성공")
        
        # 대시보드로 이동
        dashboard_page = DashboardPage(browser_manager.page, config)
        await dashboard_page.wait_for_dashboard_load()
        
        # 검색 실행
        print("\n📋 검색 실행...")
        print("-" * 30)
        
        try:
            search_term = "Simple Search Test"
            print(f"📝 검색어: {search_term}")
            
            await dashboard_page.search_sites(search_term)
            print("✅ 검색 실행 완료")
            await asyncio.sleep(3)
            
        except Exception as e:
            print(f"❌ 검색 실행 실패: {e}")
            return
        
        # 검색 결과 클릭
        print("\n📋 검색 결과 클릭...")
        print("-" * 30)
        
        try:
            results = await browser_manager.page.query_selector_all(".building")
            if results:
                await results[0].click()
                print("✅ 검색 결과 클릭 완료")
                await asyncio.sleep(3)
            else:
                print("❌ 검색 결과를 찾을 수 없습니다")
                return
                
        except Exception as e:
            print(f"❌ 검색 결과 클릭 실패: {e}")
            return
        
        # 현재 URL 확인
        current_url = browser_manager.page.url
        print(f"📝 현재 URL: {current_url}")
        
        # 사이트 이름 셀렉터 분석
        print("\n📋 사이트 이름 셀렉터 분석...")
        print("-" * 30)
        
        try:
            # 다양한 셀렉터로 사이트 이름 찾기
            site_name_selectors = [
                ".site-name",
                ".site-title", 
                ".building-name",
                ".site-profile h1",
                ".site-profile h2",
                ".site-profile h3",
                ".site-header h1",
                ".site-header h2",
                ".site-header h3",
                ".page-title",
                ".main-title",
                ".content-title",
                "h1",
                "h2",
                "h3",
                "[class*='title']",
                "[class*='name']",
                "[class*='site']",
                "[class*='building']"
            ]
            
            found_site_name = False
            for selector in site_name_selectors:
                try:
                    element = await browser_manager.page.query_selector(selector)
                    if element and await element.is_visible():
                        text = await element.text_content()
                        if text and text.strip():
                            print(f"✅ 셀렉터 '{selector}'에서 사이트 이름 발견: '{text.strip()}'")
                            found_site_name = True
                            break
                except Exception:
                    continue
            
            if not found_site_name:
                print("❌ 사이트 이름을 찾을 수 없습니다")
                
                # 페이지의 모든 텍스트 요소 확인
                print("\n📋 페이지의 모든 텍스트 요소 확인...")
                all_text_elements = await browser_manager.page.evaluate("""
                    () => {
                        const elements = document.querySelectorAll('h1, h2, h3, h4, h5, h6, .title, .name, [class*="title"], [class*="name"]');
                        const results = [];
                        elements.forEach(el => {
                            if (el.textContent && el.textContent.trim()) {
                                results.push({
                                    tagName: el.tagName,
                                    className: el.className,
                                    text: el.textContent.trim(),
                                    visible: el.offsetParent !== null
                                });
                            }
                        });
                        return results;
                    }
                """)
                
                for elem in all_text_elements:
                    if elem['visible']:
                        print(f"📝 {elem['tagName']}.{elem['className']}: '{elem['text']}'")
                
        except Exception as e:
            print(f"❌ 사이트 이름 셀렉터 분석 실패: {e}")
        
        # +Add plan 버튼 셀렉터 분석
        print("\n📋 +Add plan 버튼 셀렉터 분석...")
        print("-" * 30)
        
        try:
            add_plan_selectors = [
                "button:has-text('Add plan')",
                "button:has-text('+Add plan')",
                "button:has-text('+ Add plan')",
                "[class*='add-plan']",
                "[class*='add_plan']",
                ".add-plan-button",
                ".add_plan_button"
            ]
            
            found_add_plan = False
            for selector in add_plan_selectors:
                try:
                    element = await browser_manager.page.query_selector(selector)
                    if element and await element.is_visible():
                        text = await element.text_content()
                        print(f"✅ 셀렉터 '{selector}'에서 +Add plan 버튼 발견: '{text.strip()}'")
                        found_add_plan = True
                        break
                except Exception:
                    continue
            
            if not found_add_plan:
                print("❌ +Add plan 버튼을 찾을 수 없습니다")
                
        except Exception as e:
            print(f"❌ +Add plan 버튼 셀렉터 분석 실패: {e}")
        
        # 스크린샷 저장
        print("\n📋 스크린샷 저장...")
        print("-" * 30)
        
        try:
            screenshot_path = await browser_manager.take_screenshot("site_detail_selectors_analysis")
            print(f"📸 스크린샷 저장: {screenshot_path}")
        except Exception as e:
            print(f"❌ 스크린샷 저장 실패: {e}")
        
        print("\n" + "=" * 60)
        print("✅ 사이트 상세 페이지 셀렉터 분석 완료")
        print("=" * 60)


async def main():
    """메인 실행 함수"""
    print("🚀 사이트 상세 페이지 셀렉터 분석 시작")
    print("=" * 60)
    
    try:
        await analyze_site_detail_selectors()
    except Exception as e:
        print(f"❌ 분석 실패: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 사이트 상세 페이지 셀렉터 분석 완료")


if __name__ == "__main__":
    asyncio.run(main())
