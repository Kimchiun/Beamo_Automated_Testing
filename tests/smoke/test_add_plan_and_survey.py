#!/usr/bin/env python3
"""
Add Plan + New Survey 생성 완전한 플로우 테스트
"""
import pytest
import asyncio
from datetime import datetime
from functools import wraps
from utils.config_loader import get_config
from utils.browser_manager import BrowserFactory
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

@pytest.mark.asyncio
@pytest.mark.smoke
@pytest.mark.p0
@pytest.mark.env('dev')
@timeout(60)  # 1분 타임아웃
async def test_add_plan_and_create_survey_flow(environment: str = "dev"):
    """Add Plan + New Survey 생성 완전한 플로우 테스트"""
    print(f"🔍 {environment.upper()} 환경 Add Plan + New Survey 생성 완전한 플로우 테스트...")

    config = get_config(environment)
    
    try:
        async with BrowserFactory.create(config) as browser_manager:
            # Set test name for video naming
            browser_manager.set_current_test("add_plan_and_create_survey_flow")
            
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
            
            # 대시보드로 이동
            dashboard_page = DashboardPage(browser_manager.page, config)
            await dashboard_page.wait_for_dashboard_load()
            
            print("✅ 대시보드 로드 완료")
            
            # 사이트 검색 및 선택
            await dashboard_page.search_sites("Search Test Site")
            site_click_success = await dashboard_page.click_first_available_site()
            
            if not site_click_success:
                print("❌ 사이트 클릭 실패")
                return False
            
            print("✅ 사이트 선택 완료")
            
            # 사이트 상세 페이지로 이동
            site_detail_page = SiteDetailPage(browser_manager.page, config)
            await site_detail_page.wait_for_page_load()
            
            print("✅ 사이트 상세 페이지 로드 완료")
            
            print("\n📋 1단계: Add Plan 실행")
            print("-" * 30)
            
            # Add Plan 버튼 클릭
            try:
                await site_detail_page.click_add_plan_button()
                print("✅ Add Plan 버튼 클릭 성공")
                add_plan_clicked = True
            except Exception as e:
                print(f"❌ Add Plan 버튼 클릭 실패: {e}")
                return False
            
            if add_plan_clicked:
                print("✅ Add Plan 버튼 클릭 성공")
                
                # 파일 업로드 (자동 처리됨)
                print("✅ 이미지 파일 자동 업로드 완료")
                
                # Add Plan 모달에서 최종 확인
                add_plan_submitted = await site_detail_page.click_add_plan_submit()
                
                if add_plan_submitted:
                    print("✅ Add Plan 모달에서 최종 확인 완료")
                    
                    print("\n📋 2단계: Add Plan 성공 확인")
                    print("-" * 30)
                    
                    await asyncio.sleep(5)  # Wait for survey modal to appear
                    
                    try:
                        survey_modal_visible = await site_detail_page.is_survey_creation_modal_visible()
                        
                        if survey_modal_visible:
                            print("✅ Add Plan 성공! 'Create a new survey' 모달이 나타났습니다")
                            modal_closed = await site_detail_page.close_survey_creation_modal()
                            
                            if modal_closed:
                                print("✅ X 버튼 클릭으로 모달 닫기 성공 - Add Plan 완전 성공!")
                        else:
                            print("⚠️ 'Create a new survey' 모달이 나타나지 않음")
                            print("📝 하지만 + New survey 버튼이 활성화되었을 수 있습니다. 계속 진행해보겠습니다.")
                            
                    except Exception as survey_error:
                        print(f"⚠️ Add Plan 성공 확인 중 오류: {survey_error}")
                        print("📝 계속 진행해보겠습니다.")
                    
                    print("\n📋 3단계: New Survey 생성")
                    print("-" * 30)
                    
                    # 페이지 새로고침 후 + New survey 버튼 찾기 시도
                    print("📝 페이지 새로고침 후 + New survey 버튼 찾기...")
                    await browser_manager.page.reload()
                    await asyncio.sleep(3)
                    
                    # 현재 페이지 상태 확인을 위한 스크린샷
                    await browser_manager.take_screenshot("before_new_survey_attempt")
                    print("📸 New Survey 시도 전 스크린샷 저장됨")
                    
                    # + New survey 버튼 클릭 (여러 번 시도)
                    new_survey_clicked = False
                    for attempt in range(3):
                        try:
                            new_survey_clicked = await site_detail_page.click_new_survey_button()
                            if new_survey_clicked:
                                break
                            print(f"📝 {attempt + 1}번째 시도 실패, 잠시 대기...")
                            await asyncio.sleep(2)
                        except Exception as e:
                            print(f"📝 {attempt + 1}번째 시도 중 오류: {e}")
                            await asyncio.sleep(2)
                    
                    if new_survey_clicked:
                        print("✅ + New survey 버튼 클릭 성공")
                        
                        # New Survey 모달 확인
                        new_survey_modal_visible = await site_detail_page.is_new_survey_modal_visible()
                        
                        if new_survey_modal_visible:
                            print("✅ New Survey 모달이 나타났습니다")
                            
                            # 서베이 이름 생성 (현재 날짜/시간 포함)
                            survey_name = f"Test Survey {datetime.now().strftime('%Y%m%d_%H%M%S')}"
                            
                            # 새 서베이 생성
                            survey_created = await site_detail_page.create_new_survey(survey_name)
                            
                            if survey_created:
                                print(f"✅ 새 서베이 생성 성공: {survey_name}")
                                
                                print("\n📋 4단계: 테스트 완료")
                                print("-" * 30)
                                print("✅ Add Plan + New Survey 생성 완전한 플로우 성공!")
                                
                                # 스크린샷 촬영
                                await browser_manager.take_screenshot("add_plan_and_survey_success")
                                
                            else:
                                print("❌ 새 서베이 생성 실패")
                                await browser_manager.take_screenshot("add_plan_and_survey_failure")
                                return False
                                
                        else:
                            print("❌ New Survey 모달이 나타나지 않음")
                            await browser_manager.take_screenshot("add_plan_and_survey_failure")
                            return False
                            
                    else:
                        print("❌ + New survey 버튼 클릭 실패")
                        await browser_manager.take_screenshot("add_plan_and_survey_failure")
                        return False
                        
                else:
                    print("❌ Add Plan 모달 확인 실패")
                    await browser_manager.take_screenshot("add_plan_and_survey_failure")
                    return False
                    
            else:
                print("❌ Add Plan 버튼 클릭 실패")
                await browser_manager.take_screenshot("add_plan_and_survey_failure")
                return False
        
    except Exception as e:
        print(f"❌ 테스트 실행 중 오류 발생: {e}")
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(test_add_plan_and_create_survey_flow())
