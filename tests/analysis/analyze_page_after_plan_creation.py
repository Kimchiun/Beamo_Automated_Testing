#!/usr/bin/env python3
"""
플랜 생성 완료 후 화면의 모든 요소들을 분석하는 테스트
"""

import pytest
import asyncio
from utils.browser_manager import BrowserManager
from utils.config_loader import get_config
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.site_detail_page import SiteDetailPage


class TestPageAfterPlanCreation:
    """플랜 생성 완료 후 페이지 분석 테스트 클래스"""

    @pytest.mark.asyncio
    async def test_analyze_page_after_plan_creation(self):
        """플랜 생성 완료 후 페이지의 모든 요소들을 분석"""
        config = get_config("dev")
        
        async with BrowserManager(config) as browser_manager:
            # 테스트 이름과 상태 설정
            browser_manager.set_current_test("page_after_plan_creation")
            browser_manager.set_test_status("success")
            
            print("🔍 플랜 생성 완료 후 페이지 요소 분석 시작...")
            
            # 1단계: 로그인
            print("\n📋 1단계: 로그인")
            login_page = LoginPage(browser_manager.page, config)
            await login_page.navigate_to_login()
            
            # 로그인 정보로 로그인
            space_id = "d-ge-eric"  # Dev 환경 스페이스 ID
            await login_page.login(
                space_id=space_id,
                email=config.test_data.valid_user["email"],
                password=config.test_data.valid_user["password"]
            )
            
            # 2단계: 대시보드에서 첫 번째 사이트 선택
            print("\n📋 2단계: 사이트 선택")
            dashboard_page = DashboardPage(browser_manager.page, config)
            await dashboard_page.wait_for_dashboard_load()
            
            # 첫 번째 사이트 클릭
            first_site_clicked = await dashboard_page.click_first_available_site()
            if first_site_clicked:
                print("✅ 첫 번째 사이트 클릭됨")
            else:
                print("❌ 사이트를 찾을 수 없음")
                return
            
            # 3단계: 사이트 상세 페이지에서 Add Plan 실행
            print("\n📋 3단계: Add Plan 실행")
            site_detail_page = SiteDetailPage(browser_manager.page, config)
            await site_detail_page.wait_for_page_load()
            
            # Add Plan 실행 (실제 플랜 생성)
            print("🔄 Add Plan 프로세스 시작...")
            add_plan_success = await site_detail_page.add_plan("test_data/images/test_gallery_image.png")
            if not add_plan_success:
                print("❌ Add Plan 실패")
                return
            
            print("✅ Add Plan 프로세스 시작됨")
            
            # Add Plan 제출 버튼 클릭
            print("🔄 Add Plan 제출 버튼 클릭...")
            submit_success = await site_detail_page.click_add_plan_submit()
            if not submit_success:
                print("❌ Add Plan 제출 실패")
                return
            
            print("✅ Add Plan 제출됨")
            
            # 4단계: 플랜 생성 완료까지 대기 및 화면 분석
            print("\n📋 4단계: 플랜 생성 완료까지 대기 및 화면 분석")
            
            # 플랜 생성 프로세스 진행 상태 확인
            print("⏳ 플랜 추가 프로세스 진행 중...")
            await asyncio.sleep(10)  # 초기 대기
            
            # 현재 페이지의 모든 요소들을 체계적으로 분석
            print("\n🔍 플랜 생성 진행 중 화면 요소 분석...")
            await self.analyze_page_elements(browser_manager.page, "플랜 생성 진행 중")
            
            # 추가 대기 후 다시 분석
            print("\n⏳ 추가 대기 후 재분석...")
            await asyncio.sleep(20)
            
            print("\n🔍 플랜 생성 완료 후 화면 요소 분석...")
            await self.analyze_page_elements(browser_manager.page, "플랜 생성 완료 후")
            
            # 최종 대기 후 최종 분석
            print("\n⏳ 최종 대기 후 최종 분석...")
            await asyncio.sleep(30)
            
            print("\n🔍 최종 화면 요소 분석...")
            await self.analyze_page_elements(browser_manager.page, "최종 상태")
            
            print("\n🎉 플랜 생성 완료 후 페이지 요소 분석 완료!")

    async def analyze_page_elements(self, page, stage_name):
        """페이지의 모든 요소들을 체계적으로 분석"""
        print(f"\n🔍 {stage_name} - 페이지 요소 분석:")
        
        try:
            # 페이지 제목과 URL 확인
            page_title = await page.title()
            current_url = page.url
            print(f"  📄 페이지 제목: {page_title}")
            print(f"  🌐 현재 URL: {current_url}")
            
            # 1. 모든 버튼 찾기
            all_buttons = await page.query_selector_all("button, [role='button']")
            print(f"  🔘 총 버튼 수: {len(all_buttons)}")
            
            # 중요한 버튼들만 표시 (최대 20개)
            button_count = 0
            for i, button in enumerate(all_buttons):
                try:
                    button_text = await button.text_content()
                    button_class = await button.get_attribute("class")
                    is_visible = await button.is_visible()
                    if button_text and button_text.strip() and button_count < 20:  # 텍스트가 있는 버튼만
                        print(f"      {button_count+1}. {button_text} (class: {button_class}, visible: {is_visible})")
                        button_count += 1
                except Exception:
                    continue
            
            # 2. 모든 링크 찾기
            all_links = await page.query_selector_all("a, [role='link']")
            print(f"  🔗 총 링크 수: {len(all_links)}")
            
            # 중요한 링크들만 표시 (최대 15개)
            link_count = 0
            for i, link in enumerate(all_links):
                try:
                    link_text = await link.text_content()
                    link_href = await link.get_attribute("href")
                    if link_text and link_text.strip() and link_count < 15:  # 텍스트가 있는 링크만
                        print(f"      {link_count+1}. {link_text} (href: {link_href})")
                        link_count += 1
                except Exception:
                    continue
            
            # 3. 모든 입력 필드 찾기
            all_inputs = await page.query_selector_all("input, textarea, select")
            print(f"  📝 총 입력 필드 수: {len(all_inputs)}")
            
            # 입력 필드 상세 정보 (최대 15개)
            for i, input_field in enumerate(all_inputs[:15]):
                try:
                    input_type = await input_field.get_attribute("type")
                    placeholder = await input_field.get_attribute("placeholder")
                    input_id = await input_field.get_attribute("id")
                    print(f"      {i+1}. type: {input_type}, placeholder: {placeholder}, id: {input_id}")
                except Exception:
                    print(f"      {i+1}. [속성 읽기 실패]")
            
            # 4. 모달이나 팝업 요소들 찾기
            modal_elements = await page.query_selector_all("[class*='modal'], [class*='Modal'], [class*='dialog'], [class*='Dialog'], .el-dialog")
            print(f"  🪟 모달/다이얼로그 수: {len(modal_elements)}")
            
            for i, modal in enumerate(modal_elements):
                try:
                    modal_class = await modal.get_attribute("class")
                    modal_text = await modal.text_content()
                    is_visible = await modal.is_visible()
                    print(f"      {i+1}. class: {modal_class}, visible: {is_visible}")
                    if modal_text and len(modal_text.strip()) < 100:  # 너무 긴 텍스트는 제외
                        print(f"         텍스트: {modal_text.strip()}")
                except Exception:
                    print(f"      {i+1}. [속성 읽기 실패]")
            
            # 5. 특별한 요소들 찾기
            await self.analyze_special_elements(page)
            
        except Exception as e:
            print(f"  ❌ 페이지 요소 분석 중 오류: {e}")

    async def analyze_special_elements(self, page):
        """특별한 요소들 분석"""
        print("\n  🆕 특별한 요소 분석:")
        
        try:
            # 서베이 생성 관련 요소들
            survey_creation_elements = await page.query_selector_all("[class*='survey-creation'], [class*='SurveyCreation'], [class*='create-survey']")
            print(f"    📊 서베이 생성 관련 요소 수: {len(survey_creation_elements)}")
            
            # New Survey 버튼 찾기
            new_survey_buttons = await page.query_selector_all("button:has-text('New survey'), button:has-text('+ New survey'), [class*='new-survey']")
            print(f"    ➕ New Survey 버튼 수: {len(new_survey_buttons)}")
            
            for i, button in enumerate(new_survey_buttons):
                try:
                    button_text = await button.text_content()
                    button_class = await button.get_attribute("class")
                    is_visible = await button.is_visible()
                    print(f"      {i+1}. {button_text} (class: {button_class}, visible: {is_visible})")
                except Exception as e:
                    print(f"      {i+1}. [속성 읽기 실패: {e}]")
            
            # 플랜 관련 새로운 요소들
            plan_elements = await page.query_selector_all("[class*='plan'], [class*='Plan'], [class*='add-plan']")
            print(f"    📋 플랜 관련 요소 수: {len(plan_elements)}")
            
            # 성공 메시지나 알림 찾기
            success_messages = await page.query_selector_all("[class*='success'], [class*='Success'], [class*='message'], [class*='alert']")
            print(f"    ✅ 성공/알림 메시지 수: {len(success_messages)}")
            
            for i, message in enumerate(success_messages[:5]):  # 최대 5개만 표시
                try:
                    message_text = await message.text_content()
                    message_class = await message.get_attribute("class")
                    print(f"      {i+1}. {message_text} (class: {message_class})")
                except Exception:
                    print(f"      {i+1}. [텍스트 읽기 실패]")
            
            # 토스트 메시지나 알림 찾기
            toast_elements = await page.query_selector_all("[class*='toast'], [class*='Toast'], [class*='notification'], [class*='snackbar']")
            print(f"    🔔 토스트/알림 수: {len(toast_elements)}")
            
            # 테이블이나 리스트 요소들 찾기
            tables = await page.query_selector_all("table, [class*='table']")
            lists = await page.query_selector_all("ul, ol, [class*='list']")
            print(f"    📊 테이블 수: {len(tables)}")
            print(f"    📋 리스트 수: {len(lists)}")
            
        except Exception as e:
            print(f"    ❌ 특별한 요소 분석 중 오류: {e}")


if __name__ == "__main__":
    asyncio.run(TestPageAfterPlanCreation().test_analyze_page_after_plan_creation())
