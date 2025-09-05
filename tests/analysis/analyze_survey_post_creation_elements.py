#!/usr/bin/env python3
"""
서베이 생성 이후 나타나는 모든 요소들을 체계적으로 분석하는 테스트
"""

import pytest
import asyncio
from datetime import datetime
from utils.browser_manager import BrowserManager
from utils.config_loader import get_config
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.site_detail_page import SiteDetailPage


class TestSurveyPostCreationAnalysis:
    """서베이 생성 이후 요소 분석 테스트 클래스"""

    @pytest.mark.asyncio
    async def test_analyze_survey_post_creation_elements(self):
        """서베이 생성 이후 모든 요소들을 분석"""
        config = get_config("dev")
        
        async with BrowserManager(config) as browser_manager:
            # 테스트 이름과 상태 설정
            browser_manager.set_current_test("survey_post_creation_analysis")
            browser_manager.set_test_status("success")
            
            print("🔍 서베이 생성 이후 요소 분석 시작...")
            
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
            
            # Add Plan 버튼 클릭
            add_plan_clicked = await site_detail_page.click_add_plan_button()
            if not add_plan_clicked:
                print("❌ Add Plan 버튼 클릭 실패")
                return
            
            print("✅ Add Plan 버튼 클릭됨")
            
            # 플랜 추가 프로세스 진행 상태 확인
            print("⏳ 플랜 추가 프로세스 진행 중...")
            await asyncio.sleep(5)  # 초기 대기
            
            # 4단계: Add Plan 완료 후 서베이 생성 모달 확인
            print("\n📋 4단계: Add Plan 완료 후 서베이 생성 모달 확인")
            
            # 플랜 추가 완료까지 충분한 대기 시간
            print("⏳ 플랜 추가 완료까지 대기 중... (최대 60초)")
            await asyncio.sleep(60)  # 플랜 추가 완료까지 충분한 대기
            
            # 현재 페이지의 모든 요소들을 체계적으로 분석
            print("\n🔍 플랜 추가 완료 후 화면 전체 요소 분석 시작...")
            await self.analyze_complete_page_after_add_plan(browser_manager.page)
            
            # 서베이 생성 모달 확인
            survey_modal_visible = await site_detail_page.is_survey_creation_modal_visible()
            if survey_modal_visible:
                print("✅ Add Plan 성공! 'Create a new survey' 모달이 나타났습니다")
                
                # 모달 내용 분석
                await self.analyze_survey_creation_modal(browser_manager.page)
                
                # 모달 닫기
                await site_detail_page.close_survey_creation_modal()
            else:
                print("⚠️ 'Create a new survey' 모달이 나타나지 않음")
            
            # 5단계: + New Survey 버튼 클릭 및 모달 분석
            print("\n📋 5단계: + New Survey 버튼 클릭 및 모달 분석")
            
            # 페이지 새로고침 후 + New survey 버튼 찾기
            await browser_manager.page.reload()
            await asyncio.sleep(3)
            
            # + New survey 버튼 클릭
            new_survey_clicked = await site_detail_page.click_new_survey_button()
            if new_survey_clicked:
                print("✅ + New survey 버튼 클릭 성공")
                
                # New Survey 모달 분석
                await self.analyze_new_survey_modal(browser_manager.page)
                
                # 모달 닫기
                await site_detail_page.close_new_survey_modal()
            else:
                print("❌ + New survey 버튼 클릭 실패")
            
            # 6단계: 서베이 생성 후 페이지 전체 요소 분석
            print("\n📋 6단계: 서베이 생성 후 페이지 전체 요소 분석")
            
            # 테스트 서베이 생성
            survey_name = f"Test Survey {datetime.now().strftime('%Y%m%d_%H%M%S')}"
            survey_created = await site_detail_page.create_new_survey(survey_name)
            
            if survey_created:
                print(f"✅ 새 서베이 생성 성공: {survey_name}")
                
                # 서베이 생성 후 페이지 분석
                await self.analyze_page_after_survey_creation(browser_manager.page)
            else:
                print("❌ 서베이 생성 실패")
            
            print("\n🎉 서베이 생성 이후 요소 분석 완료!")

    async def analyze_survey_creation_modal(self, page):
        """서베이 생성 모달의 모든 요소 분석"""
        print("\n🔍 서베이 생성 모달 분석:")
        
        try:
            # 모달 제목 확인
            title = await page.query_selector(".el-dialog__title")
            if title:
                title_text = await title.text_content()
                print(f"  📝 모달 제목: {title_text}")
            
            # QR 코드 확인
            qr_code = await page.query_selector(".qr-code, [class*='qr']")
            if qr_code:
                print("  📱 QR 코드: 발견됨")
            else:
                print("  📱 QR 코드: 발견되지 않음")
            
            # 다운로드 버튼 확인
            download_btn = await page.query_selector("button:has-text('Download on the App Store')")
            if download_btn:
                print("  📲 App Store 다운로드 버튼: 발견됨")
            else:
                print("  📲 App Store 다운로드 버튼: 발견되지 않음")
            
            # Learn more 버튼 확인
            learn_more_btn = await page.query_selector("button:has-text('Learn more')")
            if learn_more_btn:
                print("  📚 Learn more 버튼: 발견됨")
            else:
                print("  📚 Learn more 버튼: 발견되지 않음")
            
            # Got it 버튼 확인
            got_it_btn = await page.query_selector("button:has-text('Got it')")
            if got_it_btn:
                print("  ✅ Got it 버튼: 발견됨")
            else:
                print("  ✅ Got it 버튼: 발견되지 않음")
            
            # 모달 내 모든 버튼 찾기
            all_buttons = await page.query_selector_all(".el-dialog button")
            print(f"  🔘 모달 내 총 버튼 수: {len(all_buttons)}")
            
            for i, button in enumerate(all_buttons):
                try:
                    button_text = await button.text_content()
                    button_class = await button.get_attribute("class")
                    print(f"    {i+1}. {button_text} (class: {button_class})")
                except Exception as e:
                    print(f"    {i+1}. [텍스트 읽기 실패: {e}]")
            
        except Exception as e:
            print(f"  ❌ 모달 분석 중 오류: {e}")

    async def analyze_new_survey_modal(self, page):
        """New Survey 모달의 모든 요소 분석"""
        print("\n🔍 New Survey 모달 분석:")
        
        try:
            # 모달 제목 확인
            title = await page.query_selector(".el-dialog.create-survey-dialog .el-dialog__title")
            if title:
                title_text = await title.text_content()
                print(f"  📝 모달 제목: {title_text}")
            
            # 입력 필드 확인
            name_input = await page.query_selector("input[placeholder='Survey Title']")
            if name_input:
                placeholder = await name_input.get_attribute("placeholder")
                input_type = await name_input.get_attribute("type")
                print(f"  📝 서베이 이름 입력 필드: 발견됨 (placeholder: {placeholder}, type: {input_type})")
            else:
                print("  📝 서베이 이름 입력 필드: 발견되지 않음")
            
            # 모든 입력 필드 찾기
            all_inputs = await page.query_selector_all(".el-dialog.create-survey-dialog input")
            print(f"  📝 모달 내 총 입력 필드 수: {len(all_inputs)}")
            
            for i, input_field in enumerate(all_inputs):
                try:
                    input_type = await input_field.get_attribute("type")
                    placeholder = await input_field.get_attribute("placeholder")
                    print(f"    {i+1}. type: {input_type}, placeholder: {placeholder}")
                except Exception as e:
                    print(f"    {i+1}. [속성 읽기 실패: {e}]")
            
            # 모든 버튼 찾기
            all_buttons = await page.query_selector_all(".el-dialog.create-survey-dialog button")
            print(f"  🔘 모달 내 총 버튼 수: {len(all_buttons)}")
            
            for i, button in enumerate(all_buttons):
                try:
                    button_text = await button.text_content()
                    button_class = await button.get_attribute("class")
                    print(f"    {i+1}. {button_text} (class: {button_class})")
                except Exception as e:
                    print(f"    {i+1}. [텍스트 읽기 실패: {e}]")
            
        except Exception as e:
            print(f"  ❌ New Survey 모달 분석 중 오류: {e}")

    async def analyze_page_after_survey_creation(self, page):
        """서베이 생성 후 페이지의 모든 요소 분석"""
        print("\n🔍 서베이 생성 후 페이지 분석:")
        
        try:
            # 페이지 제목 확인
            page_title = await page.title()
            print(f"  📄 페이지 제목: {page_title}")
            
            # URL 확인
            current_url = page.url
            print(f"  🌐 현재 URL: {current_url}")
            
            # 헤더 영역 분석
            await self.analyze_header_section(page)
            
            # 사이드바 영역 분석
            await self.analyze_sidebar_section(page)
            
            # 메인 콘텐츠 영역 분석
            await self.analyze_main_content_section(page)
            
            # 푸터 영역 분석
            await self.analyze_footer_section(page)
            
            # 전체 페이지에서 특정 요소들 찾기
            await self.analyze_specific_elements(page)
            
        except Exception as e:
            print(f"  ❌ 페이지 분석 중 오류: {e}")

    async def analyze_header_section(self, page):
        """헤더 영역 분석"""
        print("\n  🏷️ 헤더 영역 분석:")
        
        try:
            # 헤더 요소들 찾기
            header_selectors = [
                "header", "[class*='header']", "[class*='Header']",
                ".top-bar", ".navbar", ".nav-bar"
            ]
            
            for selector in header_selectors:
                header = await page.query_selector(selector)
                if header:
                    print(f"    📍 헤더 발견: {selector}")
                    break
            else:
                print("    📍 헤더: 발견되지 않음")
            
            # 헤더 내 버튼들 찾기
            header_buttons = await page.query_selector_all("header button, [class*='header'] button")
            print(f"    🔘 헤더 내 버튼 수: {len(header_buttons)}")
            
            for i, button in enumerate(header_buttons[:5]):  # 최대 5개만 표시
                try:
                    button_text = await button.text_content()
                    print(f"      {i+1}. {button_text}")
                except Exception:
                    print(f"      {i+1}. [텍스트 읽기 실패]")
            
        except Exception as e:
            print(f"    ❌ 헤더 분석 중 오류: {e}")

    async def analyze_sidebar_section(self, page):
        """사이드바 영역 분석"""
        print("\n  📱 사이드바 영역 분석:")
        
        try:
            # 사이드바 요소들 찾기
            sidebar_selectors = [
                "aside", "[class*='sidebar']", "[class*='Sidebar']",
                ".side-nav", ".side-panel", ".left-panel"
            ]
            
            for selector in sidebar_selectors:
                sidebar = await page.query_selector(selector)
                if sidebar:
                    print(f"    📍 사이드바 발견: {selector}")
                    break
            else:
                print("    📍 사이드바: 발견되지 않음")
            
            # 사이드바 내 메뉴 항목들 찾기
            sidebar_menu_items = await page.query_selector_all("aside li, [class*='sidebar'] li, .side-nav li")
            print(f"    📋 사이드바 메뉴 항목 수: {len(sidebar_menu_items)}")
            
            for i, item in enumerate(sidebar_menu_items[:10]):  # 최대 10개만 표시
                try:
                    item_text = await item.text_content()
                    print(f"      {i+1}. {item_text}")
                except Exception:
                    print(f"      {i+1}. [텍스트 읽기 실패]")
            
        except Exception as e:
            print(f"    ❌ 사이드바 분석 중 오류: {e}")

    async def analyze_main_content_section(self, page):
        """메인 콘텐츠 영역 분석"""
        print("\n  📄 메인 콘텐츠 영역 분석:")
        
        try:
            # 메인 콘텐츠 요소들 찾기
            main_selectors = [
                "main", "[class*='main']", "[class*='Main']",
                ".content", ".main-content", ".page-content"
            ]
            
            for selector in main_selectors:
                main_content = await page.query_selector(selector)
                if main_content:
                    print(f"    📍 메인 콘텐츠 발견: {selector}")
                    break
            else:
                print("    📍 메인 콘텐츠: 발견되지 않음")
            
            # 메인 콘텐츠 내 버튼들 찾기
            main_buttons = await page.query_selector_all("main button, [class*='main'] button, .content button")
            print(f"    🔘 메인 콘텐츠 내 버튼 수: {len(main_buttons)}")
            
            for i, button in enumerate(main_buttons[:10]):  # 최대 10개만 표시
                try:
                    button_text = await button.text_content()
                    button_class = await button.get_attribute("class")
                    print(f"      {i+1}. {button_text} (class: {button_class})")
                except Exception:
                    print(f"      {i+1}. [속성 읽기 실패]")
            
            # 테이블이나 리스트 요소들 찾기
            tables = await page.query_selector_all("table, [class*='table']")
            lists = await page.query_selector_all("ul, ol, [class*='list']")
            
            print(f"    📊 테이블 수: {len(tables)}")
            print(f"    📋 리스트 수: {len(lists)}")
            
        except Exception as e:
            print(f"    ❌ 메인 콘텐츠 분석 중 오류: {e}")

    async def analyze_footer_section(self, page):
        """푸터 영역 분석"""
        print("\n  🦶 푸터 영역 분석:")
        
        try:
            # 푸터 요소들 찾기
            footer_selectors = [
                "footer", "[class*='footer']", "[class*='Footer']",
                ".bottom-bar", ".page-footer"
            ]
            
            for selector in footer_selectors:
                footer = await page.query_selector(selector)
                if footer:
                    print(f"    📍 푸터 발견: {selector}")
                    break
            else:
                print("    📍 푸터: 발견되지 않음")
            
        except Exception as e:
            print(f"    ❌ 푸터 분석 중 오류: {e}")

    async def analyze_complete_page_after_add_plan(self, page):
        """플랜 추가 완료 후 페이지의 모든 요소들을 완전히 분석"""
        print("\n🔍 플랜 추가 완료 후 페이지 완전 분석:")
        
        try:
            # 페이지 제목과 URL 확인
            page_title = await page.title()
            current_url = page.url
            print(f"  📄 페이지 제목: {page_title}")
            print(f"  🌐 현재 URL: {current_url}")
            
            # 1. 헤더 영역 분석
            await self.analyze_header_section(page)
            
            # 2. 사이드바 영역 분석
            await self.analyze_sidebar_section(page)
            
            # 3. 메인 콘텐츠 영역 분석
            await self.analyze_main_content_section(page)
            
            # 4. 푸터 영역 분석
            await self.analyze_footer_section(page)
            
            # 5. 플랜 추가 후 새로 나타나는 특별한 요소들 분석
            await self.analyze_add_plan_specific_elements(page)
            
            # 6. 전체 페이지에서 모든 버튼과 링크 찾기
            await self.analyze_all_interactive_elements(page)
            
            # 7. 모달이나 팝업 요소들 찾기
            await self.analyze_modal_and_popup_elements(page)
            
        except Exception as e:
            print(f"  ❌ 페이지 완전 분석 중 오류: {e}")

    async def analyze_add_plan_specific_elements(self, page):
        """플랜 추가 후 새로 나타나는 특별한 요소들 분석"""
        print("\n  🆕 플랜 추가 후 특별한 요소 분석:")
        
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
            
        except Exception as e:
            print(f"    ❌ 특별한 요소 분석 중 오류: {e}")

    async def analyze_all_interactive_elements(self, page):
        """전체 페이지에서 모든 상호작용 가능한 요소들 찾기"""
        print("\n  🔘 모든 상호작용 요소 분석:")
        
        try:
            # 모든 버튼 찾기
            all_buttons = await page.query_selector_all("button, [role='button']")
            print(f"    🔘 총 버튼 수: {len(all_buttons)}")
            
            # 중요한 버튼들만 표시 (최대 15개)
            for i, button in enumerate(all_buttons[:15]):
                try:
                    button_text = await button.text_content()
                    button_class = await button.get_attribute("class")
                    is_visible = await button.is_visible()
                    if button_text and button_text.strip():  # 텍스트가 있는 버튼만
                        print(f"      {i+1}. {button_text} (class: {button_class}, visible: {is_visible})")
                except Exception:
                    print(f"      {i+1}. [속성 읽기 실패]")
            
            # 모든 링크 찾기
            all_links = await page.query_selector_all("a, [role='link']")
            print(f"    🔗 총 링크 수: {len(all_links)}")
            
            # 중요한 링크들만 표시 (최대 10개)
            for i, link in enumerate(all_links[:10]):
                try:
                    link_text = await link.text_content()
                    link_href = await link.get_attribute("href")
                    if link_text and link_text.strip():  # 텍스트가 있는 링크만
                        print(f"      {i+1}. {link_text} (href: {link_href})")
                except Exception:
                    print(f"      {i+1}. [속성 읽기 실패]")
            
            # 모든 입력 필드 찾기
            all_inputs = await page.query_selector_all("input, textarea, select")
            print(f"    📝 총 입력 필드 수: {len(all_inputs)}")
            
            # 입력 필드 상세 정보 (최대 10개)
            for i, input_field in enumerate(all_inputs[:10]):
                try:
                    input_type = await input_field.get_attribute("type")
                    placeholder = await input_field.get_attribute("placeholder")
                    input_id = await input_field.get_attribute("id")
                    print(f"      {i+1}. type: {input_type}, placeholder: {placeholder}, id: {input_id}")
                except Exception:
                    print(f"      {i+1}. [속성 읽기 실패]")
            
        except Exception as e:
            print(f"    ❌ 상호작용 요소 분석 중 오류: {e}")

    async def analyze_modal_and_popup_elements(self, page):
        """모달이나 팝업 요소들 찾기"""
        print("\n  🪟 모달/팝업 요소 분석:")
        
        try:
            # 모달 관련 요소들 찾기
            modal_elements = await page.query_selector_all("[class*='modal'], [class*='Modal'], [class*='dialog'], [class*='Dialog'], .el-dialog")
            print(f"    🪟 모달/다이얼로그 수: {len(modal_elements)}")
            
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
            
            # 토스트 메시지나 알림 찾기
            toast_elements = await page.query_selector_all("[class*='toast'], [class*='Toast'], [class*='notification'], [class*='snackbar']")
            print(f"    🔔 토스트/알림 수: {len(toast_elements)}")
            
        except Exception as e:
            print(f"    ❌ 모달/팝업 분석 중 오류: {e}")

    async def analyze_specific_elements(self, page):
        """특정 요소들 분석"""
        print("\n  🔍 특정 요소 분석:")
        
        try:
            # 서베이 관련 요소들 찾기
            survey_elements = await page.query_selector_all("[class*='survey'], [class*='Survey']")
            print(f"    📊 서베이 관련 요소 수: {len(survey_elements)}")
            
            # 계획 관련 요소들 찾기
            plan_elements = await page.query_selector_all("[class*='plan'], [class*='Plan']")
            print(f"    📋 계획 관련 요소 수: {len(plan_elements)}")
            
            # 사이트 관련 요소들 찾기
            site_elements = await page.query_selector_all("[class*='site'], [class*='Site']")
            print(f"    🏗️ 사이트 관련 요소 수: {len(site_elements)}")
            
            # 사용자 관련 요소들 찾기
            user_elements = await page.query_selector_all("[class*='user'], [class*='User']")
            print(f"    👤 사용자 관련 요소 수: {len(user_elements)}")
            
            # 설정 관련 요소들 찾기
            settings_elements = await page.query_selector_all("[class*='setting'], [class*='Setting'], [class*='config']")
            print(f"    ⚙️ 설정 관련 요소 수: {len(settings_elements)}")
            
            # 알림 관련 요소들 찾기
            notification_elements = await page.query_selector_all("[class*='notification'], [class*='alert'], [class*='message']")
            print(f"    🔔 알림 관련 요소 수: {len(notification_elements)}")
            
        except Exception as e:
            print(f"    ❌ 특정 요소 분석 중 오류: {e}")


if __name__ == "__main__":
    asyncio.run(TestSurveyPostCreationAnalysis().test_analyze_survey_post_creation_elements())
