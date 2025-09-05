#!/usr/bin/env python3
"""
Analyze search result structure
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


async def analyze_search_result_structure():
    """Analyze search result structure"""
    print("🔍 검색 결과 구조 분석...")
    
    config = get_config("dev")
    
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
        
        # 검색 결과 구조 분석
        print("\n📋 검색 결과 구조 분석...")
        print("-" * 30)
        
        try:
            # 첫 번째 검색 결과 요소 찾기
            results = await browser_manager.page.query_selector_all(".building")
            if results:
                first_result = results[0]
                print(f"📝 첫 번째 검색 결과 요소 발견")
                
                # 요소의 속성들 확인
                print("\n📋 요소 속성 확인...")
                
                # href 속성 확인
                href = await first_result.get_attribute("href")
                print(f"📝 href: {href}")
                
                # onclick 속성 확인
                onclick = await first_result.get_attribute("onclick")
                print(f"📝 onclick: {onclick}")
                
                # data 속성들 확인
                data_attrs = await first_result.evaluate("""
                    (element) => {
                        const attrs = {};
                        for (let attr of element.attributes) {
                            if (attr.name.startsWith('data-')) {
                                attrs[attr.name] = attr.value;
                            }
                        }
                        return attrs;
                    }
                """)
                print(f"📝 data 속성들: {data_attrs}")
                
                # 클래스 확인
                class_name = await first_result.get_attribute("class")
                print(f"📝 class: {class_name}")
                
                # 태그명 확인
                tag_name = await first_result.evaluate("el => el.tagName")
                print(f"📝 tagName: {tag_name}")
                
                # 부모 요소 확인
                parent = await first_result.evaluate("el => el.parentElement.tagName")
                print(f"📝 parent tagName: {parent}")
                
                # 클릭 가능한지 확인
                is_clickable = await first_result.is_enabled()
                print(f"📝 clickable: {is_clickable}")
                
                # 전체 HTML 구조 확인
                html_structure = await first_result.evaluate("""
                    (element) => {
                        return {
                            outerHTML: element.outerHTML.substring(0, 500),
                            innerHTML: element.innerHTML.substring(0, 500)
                        };
                    }
                """)
                print(f"📝 outerHTML: {html_structure['outerHTML']}")
                print(f"📝 innerHTML: {html_structure['innerHTML']}")
                
                # 클릭 이벤트 리스너 확인
                event_listeners = await first_result.evaluate("""
                    (element) => {
                        // 간단한 클릭 이벤트 테스트
                        let clicked = false;
                        element.addEventListener('click', () => {
                            clicked = true;
                        });
                        element.click();
                        return clicked;
                    }
                """)
                print(f"📝 클릭 이벤트 응답: {event_listeners}")
                
            else:
                print("❌ 검색 결과를 찾을 수 없습니다")
                
        except Exception as e:
            print(f"❌ 검색 결과 구조 분석 실패: {e}")
        
        # 스크린샷 저장
        print("\n📋 스크린샷 저장...")
        print("-" * 30)
        
        try:
            screenshot_path = await browser_manager.take_screenshot("search_result_structure_analysis")
            print(f"📸 스크린샷 저장: {screenshot_path}")
        except Exception as e:
            print(f"❌ 스크린샷 저장 실패: {e}")
        
        print("\n" + "=" * 60)
        print("✅ 검색 결과 구조 분석 완료")
        print("=" * 60)


async def main():
    """메인 실행 함수"""
    print("🚀 검색 결과 구조 분석 시작")
    print("=" * 60)
    
    try:
        await analyze_search_result_structure()
    except Exception as e:
        print(f"❌ 분석 실패: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 검색 결과 구조 분석 완료")


if __name__ == "__main__":
    asyncio.run(main())
