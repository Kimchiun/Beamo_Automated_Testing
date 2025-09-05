#!/usr/bin/env python3
"""
간단한 디버깅 테스트 - 파일 업로드 후 화면 새로고침으로 New Survey 버튼 찾기
"""

import pytest
import asyncio
from utils.browser_manager import BrowserManager
from utils.config_loader import get_config
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


class TestSimpleDebug:
    """간단한 디버깅 테스트 클래스"""

    @pytest.mark.asyncio
    async def test_simple_debug(self):
        """간단한 디버깅 테스트"""
        config = get_config("dev")
        
        async with BrowserManager(config) as browser_manager:
            # 테스트 이름과 상태 설정
            browser_manager.set_current_test("simple_debug")
            browser_manager.set_test_status("success")
            
            print("🔍 간단한 디버깅 테스트 시작...")
            
            # 1단계: 로그인
            print("\n📋 1단계: 로그인")
            login_page = LoginPage(browser_manager.page, config)
            await login_page.navigate_to_login()
            
            # 로그인 정보로 로그인
            space_id = "d-ge-pr"  # Dev 환경 스페이스 ID
            await login_page.login(
                space_id=space_id,
                email=config.test_data.valid_user["email"],
                password=config.test_data.valid_user["password"]
            )
            
            # 2단계: 대시보드에서 첫 번째 사이트 선택
            print("\n📋 2단계: 사이트 선택")
            dashboard_page = DashboardPage(browser_manager.page, config)
            await dashboard_page.wait_for_dashboard_load()
            
            # 첫 번째 사이트 직접 클릭 (메서드 호출 우회)
            print("🔍 첫 번째 사이트 직접 클릭 시도...")
            
            # 다양한 셀렉터로 첫 번째 사이트 찾기
            site_selectors = [
                ".building",
                "[class*='building']",
                "[class*='site']",
                "div[class*='site-item']",
                "div[class*='building-item']"
            ]
            
            first_site = None
            for selector in site_selectors:
                try:
                    site = await browser_manager.page.query_selector(selector)
                    if site and await site.is_visible():
                        first_site = site
                        print(f"✅ 사이트 발견: {selector}")
                        break
                except Exception:
                    continue
            
            if first_site:
                await first_site.click()
                print("✅ 첫 번째 사이트 클릭됨")
                
                # 사이트 상세 페이지로 이동할 때까지 대기
                print("⏳ 사이트 상세 페이지로 이동 대기...")
                await asyncio.sleep(10)  # 초기 대기
                
                # URL이 사이트 상세 페이지인지 확인
                current_url = browser_manager.page.url
                if "list" in current_url and "side" in current_url:
                    print("✅ 사이트 상세 페이지로 이동 완료")
                else:
                    print("⚠️ 아직 사이트 상세 페이지가 아님, 추가 대기...")
                    await asyncio.sleep(10)
                    
                    # 다시 URL 확인
                    current_url = browser_manager.page.url
                    if "list" in current_url and "side" in current_url:
                        print("✅ 사이트 상세 페이지로 이동 완료 (추가 대기 후)")
                    else:
                        print("⚠️ 여전히 사이트 상세 페이지가 아님")
                        print(f"현재 URL: {current_url}")
                
            else:
                print("❌ 사이트를 찾을 수 없음")
                return
            
            # 3단계: 사이트 상세 페이지에서 파일 업로드
            print("\n📋 3단계: 파일 업로드")
            
            # 페이지 로딩 대기
            await browser_manager.page.wait_for_load_state("networkidle", timeout=30000)
            print("✅ 사이트 상세 페이지 로딩 완료")
            
            # +Add plan 버튼 클릭 (다양한 셀렉터 시도)
            add_plan_selectors = [
                "button.el-button--primary.el-button--mini:has-text('Add plan')",
                "button:has-text('Add plan')",
                "button:has-text('+ Add plan')",
                "button:has-text('Add Plan')",
                "[class*='add-plan']",
                "button.el-button--primary:has-text('Add')"
            ]
            
            add_plan_button = None
            for selector in add_plan_selectors:
                try:
                    button = await browser_manager.page.query_selector(selector)
                    if button and await button.is_visible():
                        add_plan_button = button
                        print(f"✅ +Add plan 버튼 발견: {selector}")
                        break
                except Exception:
                    continue
            
            if add_plan_button:
                await add_plan_button.click()
                print("✅ +Add plan 버튼 클릭됨")
            else:
                print("❌ +Add plan 버튼을 찾을 수 없음")
                print("🔍 현재 페이지의 모든 버튼 확인...")
                await self.analyze_all_buttons_on_page(browser_manager.page)
                return
            
            # 파일 입력 대기 (숨겨진 요소도 찾기)
            await browser_manager.page.wait_for_selector(".el-upload--picture input[type='file']", timeout=10000, state="attached")
            print("✅ 파일 입력 요소 준비됨")
            
            # 파일 업로드
            file_input = await browser_manager.page.query_selector(".el-upload--picture input[type='file']")
            if file_input:
                await file_input.set_input_files("test_data/images/test_gallery_image.png")
                print("✅ 파일 업로드 완료")
                
                # 파일 업로드 후 잠시 대기
                await asyncio.sleep(3)
                print("✅ 파일 업로드 완료 후 대기 완료")
                
                # Add Plan 제출 버튼 클릭
                print("🔄 Add Plan 제출 버튼 찾기...")
                add_plan_submit_selectors = [
                    "button:has-text('Add Plan')",
                    "button:has-text('Add plan')",
                    "button.el-button--primary:has-text('Add')",
                    "button[type='submit']",
                    "button.el-button--primary"
                ]
                
                add_plan_submit_button = None
                for selector in add_plan_submit_selectors:
                    try:
                        button = await browser_manager.page.query_selector(selector)
                        if button and await button.is_visible():
                            button_text = await button.text_content()
                            if button_text and "add" in button_text.lower():
                                add_plan_submit_button = button
                                print(f"✅ Add Plan 제출 버튼 발견: {selector} (텍스트: {button_text})")
                                break
                    except Exception:
                        continue
                
                if add_plan_submit_button:
                    print("🎯 Add Plan 제출 버튼 클릭 시도...")
                    
                    # JavaScript로 직접 클릭 (Playwright 클릭이 차단되는 경우)
                    try:
                        await add_plan_submit_button.click()
                        print("✅ Add Plan 제출 버튼 클릭 성공! (Playwright)")
                    except Exception as click_error:
                        print(f"⚠️ Playwright 클릭 실패: {click_error}")
                        print("🔄 JavaScript로 직접 클릭 시도...")
                        
                        # JavaScript로 클릭
                        click_result = await browser_manager.page.evaluate("""
                            (button) => {
                                try {
                                    button.click();
                                    return true;
                                } catch (e) {
                                    return false;
                                }
                            }
                        """, add_plan_submit_button)
                        
                        if click_result:
                            print("✅ Add Plan 제출 버튼 클릭 성공! (JavaScript)")
                        else:
                            print("❌ JavaScript 클릭도 실패")
                            return
                    
                    # 로딩 마스크가 사라질 때까지 대기
                    try:
                        await browser_manager.page.wait_for_selector(".el-loading-mask", state="hidden", timeout=30000)
                        print("✅ 로딩 마스크 사라짐")
                    except Exception as e:
                        print(f"⚠️ 로딩 마스크 대기 타임아웃: {e}")
                    
                    # 추가 대기
                    await asyncio.sleep(3)
                    print("✅ Add Plan 제출 완료!")
                    
                else:
                    print("❌ Add Plan 제출 버튼을 찾을 수 없음")
                    print("🔍 현재 페이지의 모든 버튼 확인...")
                    await self.analyze_all_buttons_on_page(browser_manager.page)
                    return
                
            else:
                print("❌ 파일 입력 요소를 찾을 수 없음")
                return
            
            # 4단계: 화면 새로고침 후 New Survey 버튼 찾기
            print("\n📋 4단계: 화면 새로고침 후 New Survey 버튼 찾기")
            print("🔄 화면 새로고침 중...")
            
            # 현재 페이지 새로고침
            await browser_manager.page.reload()
            print("✅ 화면 새로고침 완료")
            
            # 페이지 로딩 대기
            await browser_manager.page.wait_for_load_state("networkidle", timeout=30000)
            print("✅ 페이지 로딩 완료")
            
            # New Survey 버튼 찾기 (다양한 셀렉터 시도)
            print("🔍 New Survey 버튼 찾기 시작...")
            
            new_survey_selectors = [
                "button:has-text('New survey')",
                "button:has-text('+ New survey')",
                "button:has-text('New Survey')",
                "button:has-text('+ New Survey')",
                "[class*='new-survey']",
                "button.el-button--primary:has-text('New survey')",
                "button.create-survey-button"
            ]
            
            new_survey_button = None
            used_selector = ""
            
            for selector in new_survey_selectors:
                try:
                    button = await browser_manager.page.query_selector(selector)
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
                all_buttons = await browser_manager.page.query_selector_all("button")
                
                for button in all_buttons:
                    try:
                        button_text = await button.text_content()
                        if button_text and "new survey" in button_text.lower():
                            if await button.is_visible():
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
                
                # 5단계: New Survey 모달 분석
                print("\n📋 5단계: New Survey 모달 분석")
                await self.analyze_new_survey_modal(browser_manager.page)
                
                # 6단계: Add 버튼 클릭
                print("\n📋 6단계: Add 버튼 클릭")
                add_button_clicked = await self.click_add_button_in_modal(browser_manager.page)
                
                if add_button_clicked:
                    print("✅ Add 버튼 클릭 성공!")
                    print("⏳ Add 버튼 클릭 후 변화 대기...")
                    await asyncio.sleep(5)
                    
                    # 7단계: Add 버튼 클릭 후 결과 확인
                    print("\n📋 7단계: Add 버튼 클릭 후 결과 확인")
                    await self.analyze_page_after_add_click(browser_manager.page)
                else:
                    print("❌ Add 버튼 클릭 실패")
                
            else:
                print("❌ New Survey 버튼을 찾을 수 없음")
                print("🔍 현재 페이지의 모든 버튼 확인...")
                await self.analyze_all_buttons_on_page(browser_manager.page)
            
            print("\n🎉 간단한 디버깅 테스트 완료!")

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

    async def analyze_all_buttons_on_page(self, page):
        """페이지의 모든 버튼 분석"""
        print("🔍 페이지의 모든 버튼 분석:")
        
        try:
            all_buttons = await page.query_selector_all("button")
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
                    
        except Exception as e:
            print(f"  ❌ 버튼 분석 중 오류: {e}")

    async def click_add_button_in_modal(self, page):
        """모달에서 Add 버튼 클릭"""
        print("🔍 Add 버튼 찾기 및 클릭...")
        
        try:
            # Add 버튼 찾기 (정확한 셀렉터 사용)
            add_button = await page.query_selector("button.el-button--primary:has-text('Add')")
            
            if add_button:
                print("✅ Add 버튼 발견")
                
                # 버튼이 클릭 가능한 상태인지 확인
                is_disabled = await add_button.get_attribute("disabled")
                if is_disabled:
                    print("⚠️ Add 버튼이 비활성화되어 있음")
                    return False
                
                # JavaScript로 직접 클릭 (Playwright 클릭이 차단되는 경우)
                try:
                    await add_button.click()
                    print("✅ Add 버튼 클릭 성공! (Playwright)")
                    return True
                except Exception as click_error:
                    print(f"⚠️ Playwright 클릭 실패: {click_error}")
                    print("🔄 JavaScript로 직접 클릭 시도...")
                    
                    # JavaScript로 클릭
                    click_result = await page.evaluate("""
                        (button) => {
                            try {
                                button.click();
                                return true;
                            } catch (e) {
                                return false;
                            }
                        }
                    """, add_button)
                    
                    if click_result:
                        print("✅ Add 버튼 클릭 성공! (JavaScript)")
                        return True
                    else:
                        print("❌ JavaScript 클릭도 실패")
                        return False
                
            else:
                print("❌ Add 버튼을 찾을 수 없음")
                return False
                
        except Exception as e:
            print(f"❌ Add 버튼 클릭 중 오류: {e}")
            return False

    async def analyze_page_after_add_click(self, page):
        """Add 버튼 클릭 후 페이지 상태 분석"""
        print("🔍 Add 버튼 클릭 후 페이지 상태 분석...")
        
        try:
            # 1. 모달이 닫혔는지 확인
            modal = await page.query_selector(".el-dialog:has-text('New Survey')")
            if modal and await modal.is_visible():
                print("⚠️ 모달이 아직 열려있음")
            else:
                print("✅ 모달이 닫힘")
            
            # 2. 현재 페이지의 모든 버튼 확인
            all_buttons = await page.query_selector_all("button")
            print(f"  🔘 현재 페이지 버튼 수: {len(all_buttons)}")
            
            # 중요한 버튼들만 표시 (최대 15개)
            button_count = 0
            for i, button in enumerate(all_buttons):
                try:
                    button_text = await button.text_content()
                    button_class = await button.get_attribute("class")
                    is_visible = await button.is_visible()
                    if button_text and button_text.strip() and button_count < 15:  # 텍스트가 있는 버튼만
                        print(f"      {button_count+1}. {button_text} (class: {button_class}, visible: {is_visible})")
                        button_count += 1
                except Exception:
                    continue
            
            # 3. 성공 메시지나 알림 찾기
            success_messages = await page.query_selector_all("[class*='success'], [class*='Success'], [class*='message'], [class*='alert']")
            print(f"  ✅ 성공/알림 메시지 수: {len(success_messages)}")
            
            for i, message in enumerate(success_messages[:5]):  # 최대 5개만 표시
                try:
                    if await message.is_visible():
                        message_text = await message.text_content()
                        message_class = await message.get_attribute("class")
                        print(f"      {i+1}. {message_text} (class: {message_class})")
                except Exception:
                    print(f"      {i+1}. [텍스트 읽기 실패]")
            
            # 4. 페이지 제목과 URL 확인
            page_title = await page.title()
            current_url = page.url
            print(f"  📄 페이지 제목: {page_title}")
            print(f"  🌐 현재 URL: {current_url}")
            
        except Exception as e:
            print(f"❌ 페이지 상태 분석 중 오류: {e}")


if __name__ == "__main__":
    asyncio.run(TestSimpleDebug().test_simple_debug())
