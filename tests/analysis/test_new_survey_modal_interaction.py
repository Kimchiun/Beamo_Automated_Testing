#!/usr/bin/env python3
"""
New Survey 버튼 클릭 및 모달 상호작용 테스트
"""

import pytest
import asyncio
from datetime import datetime
from utils.browser_manager import BrowserManager
from utils.config_loader import get_config
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.site_detail_page import SiteDetailPage


class TestNewSurveyModalInteraction:
    """New Survey 모달 상호작용 테스트 클래스"""

    @pytest.mark.asyncio
    async def test_new_survey_modal_interaction(self):
        """New Survey 버튼 클릭 및 모달 상호작용"""
        config = get_config("dev")
        
        async with BrowserManager(config) as browser_manager:
            # 테스트 이름과 상태 설정
            browser_manager.set_current_test("new_survey_modal_interaction")
            browser_manager.set_test_status("success")
            
            print("🔍 New Survey 모달 상호작용 테스트 시작...")
            
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
            
            # 4단계: 플랜 생성 완료까지 대기
            print("\n📋 4단계: 플랜 생성 완료까지 대기")
            print("⏳ 플랜 생성 완료 확인 중...")
            
            # 플랜 생성 완료까지 대기 (요소가 실제로 로드되면 동작)
            plan_completion_success = await site_detail_page.wait_for_plan_creation_completion(max_wait_time=120)
            print(f"🔍 플랜 생성 완료 확인 결과: {plan_completion_success}")
            
            if not plan_completion_success:
                print("⚠️ 플랜 생성 완료 확인 실패, 수동 대기로 진행...")
                await asyncio.sleep(30)  # 수동 대기
            else:
                print("✅ 플랜 생성 완료 확인됨!")
            
            print("🔄 5단계로 진행 중...")
            
            # 5단계: New Survey 버튼 찾기 및 클릭
            print("\n📋 5단계: New Survey 버튼 찾기 및 클릭")
            new_survey_clicked = await self.find_and_click_new_survey_button(browser_manager.page)
            print(f"🔍 New Survey 버튼 클릭 결과: {new_survey_clicked}")
            
            if not new_survey_clicked:
                print("❌ New Survey 버튼 클릭 실패")
                return
            
            print("🔄 6단계로 진행 중...")
            
            # 6단계: New Survey 모달 분석
            print("\n📋 6단계: New Survey 모달 분석")
            modal_analyzed = await self.analyze_new_survey_modal(browser_manager.page)
            print(f"🔍 모달 분석 결과: {modal_analyzed}")
            
            if not modal_analyzed:
                print("❌ New Survey 모달 분석 실패")
                return
            
            print("🔄 7단계로 진행 중...")
            
            # 7단계: Add 버튼 클릭
            print("\n📋 7단계: Add button 클릭")
            add_button_clicked = await self.click_add_button_in_modal(browser_manager.page)
            print(f"🔍 Add 버튼 클릭 결과: {add_button_clicked}")
            
            if not add_button_clicked:
                print("❌ Add 버튼 클릭 실패")
                return
            
            print("✅ 모든 단계 완료!")
            
            print("\n🎉 New Survey 모달 상호작용 테스트 완료!")

    async def find_and_click_new_survey_button(self, page):
        """New Survey 버튼을 찾아서 클릭"""
        print("🔍 New Survey 버튼 찾기 시작...")
        
        try:
            # 다양한 셀렉터로 New Survey 버튼 찾기
            new_survey_selectors = [
                "button:has-text('New survey')",
                "button:has-text('+ New survey')",
                "[class*='new-survey']",
                "button.el-button--primary:has-text('New survey')",
                "button.create-survey-button",
                "button:has-text('New Survey')",
                "button:has-text('+ New Survey')"
            ]
            
            new_survey_button = None
            used_selector = ""
            
            for selector in new_survey_selectors:
                try:
                    button = await page.query_selector(selector)
                    if button and await button.is_visible():
                        new_survey_button = button
                        used_selector = selector
                        print(f"✅ New Survey 버튼 발견: {selector}")
                        break
                except Exception as e:
                    print(f"⚠️ 셀렉터 {selector} 실패: {e}")
                    continue
            
            if not new_survey_button:
                # 페이지에서 모든 버튼을 검색하여 "New survey" 텍스트가 포함된 버튼 찾기
                print("🔄 모든 버튼에서 'New survey' 텍스트 검색...")
                all_buttons = await page.query_selector_all("button")
                
                for button in all_buttons:
                    try:
                        button_text = await button.text_content()
                        if button_text and "new survey" in button_text.lower():
                            new_survey_button = button
                            used_selector = f"텍스트 기반 검색: {button_text}"
                            print(f"✅ 텍스트 기반으로 New Survey 버튼 발견: {button_text}")
                            break
                    except Exception:
                        continue
            
            if new_survey_button:
                print(f"🎯 New Survey 버튼 클릭 시도: {used_selector}")
                
                # 버튼 클릭
                await new_survey_button.click()
                print("✅ New Survey 버튼 클릭 성공!")
                
                # 모달이 나타날 때까지 대기
                print("⏳ New Survey 모달이 나타날 때까지 대기...")
                await asyncio.sleep(3)
                
                return True
            else:
                print("❌ New Survey 버튼을 찾을 수 없음")
                return False
                
        except Exception as e:
            print(f"❌ New Survey 버튼 찾기/클릭 중 오류: {e}")
            return False

    async def analyze_new_survey_modal(self, page):
        """New Survey 모달의 모든 요소 분석"""
        print("🔍 New Survey 모달 분석 시작...")
        
        try:
            # New Survey 모달 찾기
            modal_selectors = [
                ".el-dialog.create-survey-dialog",
                ".el-dialog:has-text('Survey Title')",
                ".el-dialog:has-text('Create Survey')",
                "[class*='create-survey']",
                "[class*='survey-dialog']"
            ]
            
            modal = None
            for selector in modal_selectors:
                try:
                    modal = await page.query_selector(selector)
                    if modal and await modal.is_visible():
                        print(f"✅ New Survey 모달 발견: {selector}")
                        break
                except Exception:
                    continue
            
            if not modal:
                # 모든 모달에서 "Survey Title" 또는 "Create Survey" 텍스트 검색
                print("🔄 모든 모달에서 'Survey Title' 또는 'Create Survey' 텍스트 검색...")
                all_modals = await page.query_selector_all(".el-dialog, [class*='modal'], [class*='dialog']")
                
                for mod in all_modals:
                    try:
                        modal_text = await mod.text_content()
                        if modal_text and ("survey title" in modal_text.lower() or "create survey" in modal_text.lower()):
                            modal = mod
                            print(f"✅ 텍스트 기반으로 New Survey 모달 발견")
                            break
                    except Exception:
                        continue
            
            if modal:
                print("📊 New Survey 모달 상세 분석:")
                
                # 1. 모달 제목
                try:
                    title = await modal.query_selector(".el-dialog__title, h3, h4, .title")
                    if title:
                        title_text = await title.text_content()
                        print(f"  📝 모달 제목: {title_text}")
                except Exception:
                    print("  📝 모달 제목: 읽기 실패")
                
                # 2. 모달 내용
                try:
                    content = await modal.query_selector(".el-dialog__body, .modal-body, .content")
                    if content:
                        content_text = await content.text_content()
                        if content_text and len(content_text.strip()) < 300:
                            print(f"  📄 모달 내용: {content_text.strip()}")
                except Exception:
                    print("  📄 모달 내용: 읽기 실패")
                
                # 3. 모든 입력 필드 찾기
                input_fields = await modal.query_selector_all("input, textarea, select")
                print(f"  📝 입력 필드 수: {len(input_fields)}")
                
                for i, input_field in enumerate(input_fields):
                    try:
                        input_type = await input_field.get_attribute("type")
                        placeholder = await input_field.get_attribute("placeholder")
                        input_id = await input_field.get_attribute("id")
                        input_name = await input_field.get_attribute("name")
                        print(f"    {i+1}. type: {input_type}, placeholder: {placeholder}, id: {input_id}, name: {input_name}")
                    except Exception:
                        print(f"    {i+1}. [속성 읽기 실패]")
                
                # 4. 모든 버튼 찾기
                buttons = await modal.query_selector_all("button")
                print(f"  🔘 버튼 수: {len(buttons)}")
                
                for i, button in enumerate(buttons):
                    try:
                        button_text = await button.text_content()
                        button_class = await button.get_attribute("class")
                        button_type = await button.get_attribute("type")
                        is_disabled = await button.get_attribute("disabled")
                        print(f"    {i+1}. {button_text} (class: {button_class}, type: {button_type}, disabled: {is_disabled})")
                    except Exception:
                        print(f"    {i+1}. [속성 읽기 실패]")
                
                # 5. 모달 크기 및 위치
                try:
                    modal_box = await modal.bounding_box()
                    if modal_box:
                        print(f"  📐 모달 크기: {modal_box['width']:.0f} x {modal_box['height']:.0f}")
                        print(f"  📍 모달 위치: ({modal_box['x']:.0f}, {modal_box['y']:.0f})")
                except Exception:
                    print("  📐 모달 크기/위치: 읽기 실패")
                
                return True
            else:
                print("❌ New Survey 모달을 찾을 수 없음")
                return False
                
        except Exception as e:
            print(f"❌ New Survey 모달 분석 중 오류: {e}")
            return False

    async def click_add_button_in_modal(self, page):
        """모달에서 Add 버튼 클릭"""
        print("🔍 Add 버튼 찾기 및 클릭...")
        
        try:
            # Add 버튼 찾기 (다양한 셀렉터 시도)
            add_button_selectors = [
                "button:has-text('Add')",
                "button:has-text('Create')",
                "button:has-text('Submit')",
                "button:has-text('Save')",
                "button.el-button--primary:has-text('Add')",
                "button.el-button--primary:has-text('Create')",
                "button.el-button--primary:has-text('Submit')",
                "button.el-button--primary:has-text('Save')",
                "[class*='add-button']",
                "[class*='create-button']",
                "[class*='submit-button']"
            ]
            
            add_button = None
            used_selector = ""
            
            for selector in add_button_selectors:
                try:
                    button = await page.query_selector(selector)
                    if button and await button.is_visible():
                        button_text = await button.text_content()
                        if button_text and any(keyword in button_text.lower() for keyword in ['add', 'create', 'submit', 'save']):
                            add_button = button
                            used_selector = selector
                            print(f"✅ Add 버튼 발견: {selector} (텍스트: {button_text})")
                            break
                except Exception as e:
                    print(f"⚠️ 셀렉터 {selector} 실패: {e}")
                    continue
            
            if not add_button:
                # 모든 버튼에서 "Add", "Create", "Submit", "Save" 텍스트 검색
                print("🔄 모든 버튼에서 'Add', 'Create', 'Submit', 'Save' 텍스트 검색...")
                all_buttons = await page.query_selector_all("button")
                
                for button in all_buttons:
                    try:
                        button_text = await button.text_content()
                        if button_text and any(keyword in button_text.lower() for keyword in ['add', 'create', 'submit', 'save']):
                            add_button = button
                            used_selector = f"텍스트 기반 검색: {button_text}"
                            print(f"✅ 텍스트 기반으로 Add 버튼 발견: {button_text}")
                            break
                    except Exception:
                        continue
            
            if add_button:
                print(f"🎯 Add 버튼 클릭 시도: {used_selector}")
                
                # 버튼이 클릭 가능한 상태인지 확인
                is_disabled = await add_button.get_attribute("disabled")
                if is_disabled:
                    print("⚠️ Add 버튼이 비활성화되어 있음")
                    return False
                
                # 버튼 클릭
                await add_button.click()
                print("✅ Add 버튼 클릭 성공!")
                
                # 모달이 닫히거나 페이지가 변경될 때까지 대기
                print("⏳ Add 버튼 클릭 후 변화 대기...")
                await asyncio.sleep(5)
                
                return True
            else:
                print("❌ Add 버튼을 찾을 수 없음")
                return False
                
        except Exception as e:
            print(f"❌ Add 버튼 클릭 중 오류: {e}")
            return False


if __name__ == "__main__":
    asyncio.run(TestNewSurveyModalInteraction().test_new_survey_modal_interaction())
