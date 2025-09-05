#!/usr/bin/env python3
"""
Analyze search filtering
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


async def analyze_search_filtering():
    """Analyze search filtering"""
    print("🔍 검색 필터링 분석...")
    
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
        
        # 검색 전 전체 사이트 개수 확인
        print("\n📋 검색 전 전체 사이트 개수 확인...")
        print("-" * 30)
        
        try:
            all_sites = await browser_manager.page.query_selector_all(".building")
            print(f"📝 전체 사이트 개수: {len(all_sites)}")
            
            # 처음 5개 사이트 이름 확인
            print("\n📝 처음 5개 사이트 이름:")
            for i in range(min(5, len(all_sites))):
                site_name_elem = await all_sites[i].query_selector(".building-name")
                if site_name_elem:
                    site_name = await site_name_elem.text_content()
                    print(f"   {i+1}. {site_name}")
                else:
                    print(f"   {i+1}. 이름 없음")
                    
        except Exception as e:
            print(f"❌ 전체 사이트 개수 확인 실패: {e}")
            return
        
        # 다양한 검색어로 테스트
        search_terms = [
            "Simple Search Test",
            "Simple Search Test Site 73517",  # 정확한 사이트 이름
            "73517",  # 사이트 ID
            "Test Site",  # 부분 검색
            "Simple",  # 부분 검색
            "존재하지 않는 사이트",  # 존재하지 않는 검색어
            "Test Site 64806",  # 다른 사이트 이름
        ]
        
        for search_term in search_terms:
            print(f"\n🔍 검색어: '{search_term}'")
            print("-" * 30)
            
            try:
                # 검색 실행
                await dashboard_page.search_sites(search_term)
                await asyncio.sleep(3)
                
                # 검색 결과 개수 확인
                search_results = await browser_manager.page.query_selector_all(".building")
                print(f"📝 검색 결과 개수: {len(search_results)}")
                
                if len(search_results) > 0:
                    # 검색 결과 이름들 확인
                    print("📝 검색 결과 사이트 이름들:")
                    for i in range(min(5, len(search_results))):
                        site_name_elem = await search_results[i].query_selector(".building-name")
                        if site_name_elem:
                            site_name = await site_name_elem.text_content()
                            print(f"   {i+1}. {site_name}")
                        else:
                            print(f"   {i+1}. 이름 없음")
                    
                    # 검색어가 결과에 포함되는지 확인
                    matching_results = 0
                    for result in search_results:
                        site_name_elem = await result.query_selector(".building-name")
                        if site_name_elem:
                            site_name = await site_name_elem.text_content()
                            if search_term.lower() in site_name.lower():
                                matching_results += 1
                    
                    print(f"📝 검색어와 일치하는 결과: {matching_results}개")
                    
                    if matching_results == 0:
                        print("⚠️ 검색어와 일치하는 결과가 없습니다!")
                    elif matching_results == len(search_results):
                        print("✅ 모든 결과가 검색어와 일치합니다")
                    else:
                        print(f"⚠️ 일부 결과만 검색어와 일치합니다 ({matching_results}/{len(search_results)})")
                        
                else:
                    print("📝 검색 결과 없음")
                    
            except Exception as e:
                print(f"❌ 검색 실패: {e}")
        
        # 검색 입력 필드 상태 확인
        print(f"\n📋 검색 입력 필드 상태 확인...")
        print("-" * 30)
        
        try:
            search_input = await browser_manager.page.query_selector("input[placeholder='검색'], input[placeholder*='search'], input[placeholder*='Search']")
            if search_input:
                current_value = await search_input.input_value()
                print(f"📝 현재 검색 입력값: '{current_value}'")
                
                # 검색 입력 필드의 속성 확인
                placeholder = await search_input.get_attribute("placeholder")
                print(f"📝 placeholder: '{placeholder}'")
                
                is_enabled = await search_input.is_enabled()
                print(f"📝 enabled: {is_enabled}")
                
                is_visible = await search_input.is_visible()
                print(f"📝 visible: {is_visible}")
            else:
                print("❌ 검색 입력 필드를 찾을 수 없습니다")
                
        except Exception as e:
            print(f"❌ 검색 입력 필드 상태 확인 실패: {e}")
        
        # 스크린샷 저장
        print("\n📋 스크린샷 저장...")
        print("-" * 30)
        
        try:
            screenshot_path = await browser_manager.take_screenshot("search_filtering_analysis")
            print(f"📸 스크린샷 저장: {screenshot_path}")
        except Exception as e:
            print(f"❌ 스크린샷 저장 실패: {e}")
        
        print("\n" + "=" * 60)
        print("✅ 검색 필터링 분석 완료")
        print("=" * 60)


async def main():
    """메인 실행 함수"""
    print("🚀 검색 필터링 분석 시작")
    print("=" * 60)
    
    try:
        await analyze_search_filtering()
    except Exception as e:
        print(f"❌ 분석 실패: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 검색 필터링 분석 완료")


if __name__ == "__main__":
    asyncio.run(main())

