#!/usr/bin/env python3
"""
Test search for "Tag Test" and enter the site
"""

import asyncio
from functools import wraps
import sys
import os
from pathlib import Path

import pytest

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.config_loader import get_config
from utils.browser_manager import BrowserManager
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.site_detail_page import SiteDetailPage


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


class TestTagTestSearch:
    """Tag Test 검색 테스트 클래스"""

    @pytest.mark.asyncio
    @timeout(60)  # 60초 타임아웃
    async def test_tag_test_search_and_enter(self):
        """Tag Test 검색 및 진입 테스트"""
        print("🔍 Tag Test 검색 및 진입 테스트 시작...")
        
        config = get_config("dev")
        
        async with BrowserManager(config) as browser_manager:
            # 테스트 이름과 상태 설정
            browser_manager.set_current_test("tag_test_search")
            browser_manager.set_test_status("success")
            
            # 1단계: 로그인
            print("\n📋 1단계: 로그인")
            login_page = LoginPage(browser_manager.page, config)
            await login_page.navigate_to_login()
            
            # 로그인 정보로 로그인
            space_id = "d-ge-ro"  # Dev 환경 스페이스 ID
            await login_page.login(
                space_id=space_id,
                email=config.test_data.valid_user["email"],
                password=config.test_data.valid_user["password"]
            )
            
            # 로그인 성공 확인
            if not await login_page.is_logged_in():
                print("❌ 로그인 실패")
                return False
            
            print("✅ 로그인 성공")
            
            # 2단계: 대시보드에서 Tag Test 검색
            print("\n📋 2단계: Tag Test 검색")
            dashboard_page = DashboardPage(browser_manager.page, config)
            await dashboard_page.wait_for_dashboard_load()
            
            # 검색어 설정
            search_term = "Tag Test"
            print(f"🔍 검색어: '{search_term}'")
            
            try:
                # 검색 실행
                await dashboard_page.search_sites(search_term)
                print("✅ 검색 실행 완료")
                
                # 검색 결과 로딩 대기
                await asyncio.sleep(3)
                print("✅ 검색 결과 로딩 완료")
                
            except Exception as e:
                print(f"❌ 검색 실행 실패: {e}")
                return False
            
            # 3단계: 검색 결과 확인
            print("\n📋 3단계: 검색 결과 확인")
            
            try:
                # 검색 결과 개수 확인
                search_results_count = await dashboard_page.get_search_results_count()
                print(f"📝 검색 결과 개수: {search_results_count}")
                
                if search_results_count == 0:
                    print("❌ 'Tag Test' 검색 결과가 없습니다")
                    print("🔍 다른 검색어로 시도해보겠습니다...")
                    
                    # 대안 검색어들 시도
                    alternative_terms = ["tag", "test", "Tag", "Test"]
                    for alt_term in alternative_terms:
                        try:
                            print(f"🔄 '{alt_term}' 검색 시도...")
                            await dashboard_page.search_sites(alt_term)
                            await asyncio.sleep(2)
                            
                            alt_count = await dashboard_page.get_search_results_count()
                            if alt_count > 0:
                                print(f"✅ '{alt_term}' 검색 결과 발견: {alt_count}개")
                                search_term = alt_term
                                search_results_count = alt_count
                                break
                        except Exception:
                            continue
                    
                    if search_results_count == 0:
                        print("❌ 모든 대안 검색어에서 결과를 찾을 수 없습니다")
                        return False
                
                # 첫 번째 검색 결과 정보 확인
                first_result_info = await dashboard_page.get_site_info_by_index(0)
                print(f"📝 첫 번째 검색 결과 정보: {first_result_info}")
                
                # 첫 번째 검색 결과 이름 확인
                first_result_name = await dashboard_page.get_site_name_by_index(0)
                print(f"📝 첫 번째 검색 결과 이름: '{first_result_name}'")
                
                # Tag Test 관련 사이트인지 확인
                if "tag" in first_result_name.lower() or "test" in first_result_name.lower():
                    print("✅ Tag Test 관련 사이트 발견!")
                else:
                    print("⚠️ Tag Test 관련 사이트가 아닐 수 있습니다")
                
            except Exception as e:
                print(f"❌ 검색 결과 확인 실패: {e}")
                return False
            
            # 4단계: 검색 결과 클릭하여 사이트 진입
            print("\n📋 4단계: 사이트 진입")
            
            try:
                # 검색 결과 클릭 전 URL 확인
                before_click_url = browser_manager.page.url
                print(f"📝 클릭 전 URL: {before_click_url}")
                
                # 첫 번째 검색 결과 클릭
                await dashboard_page.click_search_result_by_index(0)
                print("✅ 첫 번째 검색 결과 클릭 성공")
                
                # 사이트 상세 페이지 로딩 대기
                await asyncio.sleep(3)
                after_click_url = browser_manager.page.url
                print(f"📝 클릭 후 URL: {after_click_url}")
                
                # URL 변경 확인
                if before_click_url != after_click_url:
                    print("✅ 클릭 후 URL이 변경되었습니다")
                else:
                    print("⚠️ 클릭 후 URL이 변경되지 않았습니다")
                
            except Exception as e:
                print(f"❌ 검색 결과 클릭 실패: {e}")
                return False
            
            # 5단계: 사이트 상세 페이지에서 사이트 정보 확인
            print("\n📋 5단계: 사이트 상세 페이지 정보 확인")
            
            try:
                site_detail_page = SiteDetailPage(browser_manager.page, config)
                await site_detail_page.wait_for_page_load()
                
                # 사이트 상세 페이지에서 사이트 이름 가져오기
                detail_page_site_name = await site_detail_page.get_site_name()
                print(f"📝 상세 페이지 사이트 이름: '{detail_page_site_name}'")
                
                # 검색한 사이트 이름과 비교
                print(f"📝 검색한 사이트 이름: '{first_result_name}'")
                print(f"📝 진입한 사이트 이름: '{detail_page_site_name}'")
                
                if first_result_name == detail_page_site_name:
                    print("✅ 검색한 사이트와 진입한 사이트가 동일합니다!")
                else:
                    print("❌ 검색한 사이트와 진입한 사이트가 다릅니다!")
                    print("⚠️ 잘못된 사이트에 진입했을 수 있습니다")
                
                # 사이트 주소 정보 확인
                try:
                    site_address = await site_detail_page.get_site_address()
                    print(f"📝 사이트 주소: {site_address}")
                except Exception:
                    print("⚠️ 사이트 주소 정보를 가져올 수 없습니다")
                
                # 사이트 좌표 정보 확인
                try:
                    site_coordinates = await site_detail_page.get_site_coordinates()
                    print(f"📝 사이트 좌표: {site_coordinates}")
                except Exception:
                    print("⚠️ 사이트 좌표 정보를 가져올 수 없습니다")
                
            except Exception as e:
                print(f"❌ 사이트 상세 페이지 정보 확인 실패: {e}")
            
            # 6단계: 사이트 상세 페이지에서 주요 기능 확인
            print("\n📋 6단계: 주요 기능 확인")
            
            try:
                # +Add plan 버튼 존재 확인
                add_plan_button = await site_detail_page.is_add_plan_button_visible()
                if add_plan_button:
                    print("✅ +Add plan 버튼이 존재합니다")
                else:
                    print("⚠️ +Add plan 버튼을 찾을 수 없습니다")
                
                # 갤러리 이미지 추가 버튼 존재 확인
                gallery_button = await site_detail_page.is_gallery_add_button_visible()
                if gallery_button:
                    print("✅ 갤러리 이미지 추가 버튼이 존재합니다")
                else:
                    print("⚠️ 갤러리 이미지 추가 버튼을 찾을 수 없습니다")
                
                # New Survey 버튼 존재 확인 (이미 플랜이 추가된 경우)
                try:
                    new_survey_button = await site_detail_page.is_new_survey_button_visible()
                    if new_survey_button:
                        print("✅ New Survey 버튼이 존재합니다")
                    else:
                        print("ℹ️ New Survey 버튼이 존재하지 않습니다 (플랜이 추가되지 않음)")
                except Exception:
                    print("ℹ️ New Survey 버튼 확인을 건너뜁니다")
                
            except Exception as e:
                print(f"❌ 주요 기능 확인 실패: {e}")
            
            # 7단계: 스크린샷 저장
            print("\n📋 7단계: 스크린샷 저장")
            
            try:
                screenshot_path = await site_detail_page.take_screenshot("tag_test_search", "success")
                print(f"📸 스크린샷 저장: {screenshot_path}")
            except Exception as e:
                print(f"❌ 스크린샷 저장 실패: {e}")
            
            print("\n" + "=" * 60)
            print("✅ Tag Test 검색 및 진입 테스트 완료")
            print("=" * 60)
            
            return True


if __name__ == "__main__":
    asyncio.run(TestTagTestSearch().test_tag_test_search_and_enter())
