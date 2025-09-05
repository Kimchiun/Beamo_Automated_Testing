#!/usr/bin/env python3
"""
Tag Test 사이트 진입 후 페이지 요소 분석
"""

import asyncio
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


class TestTagTestSiteAnalysis:
    """Tag Test 사이트 요소 분석 테스트 클래스"""

    @pytest.mark.asyncio
    async def test_analyze_tag_test_site_elements(self):
        """Tag Test 사이트 진입 후 모든 요소 분석"""
        print("🔍 Tag Test 사이트 요소 분석 시작...")
        
        config = get_config("dev")
        
        async with BrowserManager(config) as browser_manager:
            # 테스트 이름과 상태 설정
            browser_manager.set_current_test("tag_test_site_analysis")
            browser_manager.set_test_status("success")
            
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
            
            print("✅ 로그인 성공")
            
            # 2단계: Tag Test 검색 및 진입
            print("\n📋 2단계: Tag Test 검색 및 진입")
            dashboard_page = DashboardPage(browser_manager.page, config)
            await dashboard_page.wait_for_dashboard_load()
            
            # Tag Test 검색
            search_term = "Tag Test"
            print(f"🔍 검색어: '{search_term}'")
            
            await dashboard_page.search_sites(search_term)
            await asyncio.sleep(3)
            
            # 첫 번째 검색 결과 클릭
            await dashboard_page.click_search_result_by_index(0)
            print("✅ Tag Test 사이트 진입 성공")
            
            # 3단계: 페이지 로딩 대기
            print("\n📋 3단계: 페이지 로딩 대기")
            await asyncio.sleep(5)
            await browser_manager.page.wait_for_load_state("networkidle", timeout=30000)
            print("✅ 페이지 로딩 완료")
            
            # 4단계: 페이지 기본 정보 분석
            print("\n📋 4단계: 페이지 기본 정보 분석")
            await self.analyze_page_basic_info(browser_manager.page)
            
            # 5단계: 모든 버튼 분석
            print("\n📋 5단계: 모든 버튼 분석")
            await self.analyze_all_buttons(browser_manager.page)
            
            # 6단계: 모든 입력 필드 분석
            print("\n📋 6단계: 모든 입력 필드 분석")
            await self.analyze_all_input_fields(browser_manager.page)
            
            # 7단계: 모든 링크 분석
            print("\n📋 7단계: 모든 링크 분석")
            await self.analyze_all_links(browser_manager.page)
            
            # 8단계: 모든 이미지 분석
            print("\n📋 8단계: 모든 이미지 분석")
            await self.analyze_all_images(browser_manager.page)
            
            # 9단계: 특정 영역별 상세 분석
            print("\n📋 9단계: 특정 영역별 상세 분석")
            await self.analyze_specific_areas(browser_manager.page)
            
            # 10단계: 스크린샷 저장
            print("\n📋 10단계: 스크린샷 저장")
            try:
                screenshot_path = await browser_manager.page.screenshot(path="reports/dev/screenshots/tag_test_site_analysis.png")
                print(f"📸 스크린샷 저장: {screenshot_path}")
            except Exception as e:
                print(f"❌ 스크린샷 저장 실패: {e}")
            
            print("\n" + "=" * 60)
            print("✅ Tag Test 사이트 요소 분석 완료")
            print("=" * 60)

    async def analyze_page_basic_info(self, page):
        """페이지 기본 정보 분석"""
        print("📊 페이지 기본 정보:")
        
        try:
            # 페이지 제목
            title = await page.title()
            print(f"  📄 페이지 제목: {title}")
            
            # 현재 URL
            current_url = page.url
            print(f"  🌐 현재 URL: {current_url}")
            
            # 페이지 크기
            viewport_size = page.viewport_size
            if viewport_size:
                print(f"  📐 뷰포트 크기: {viewport_size['width']} x {viewport_size['height']}")
            
            # 페이지 로딩 상태
            print(f"  🔄 페이지 로딩 상태: 완료")
            
        except Exception as e:
            print(f"  ❌ 페이지 기본 정보 분석 실패: {e}")

    async def analyze_all_buttons(self, page):
        """모든 버튼 분석"""
        print("🔘 모든 버튼 분석:")
        
        try:
            all_buttons = await page.query_selector_all("button")
            print(f"  🔘 총 버튼 수: {len(all_buttons)}")
            
            # 중요한 버튼들만 표시 (최대 30개)
            button_count = 0
            for i, button in enumerate(all_buttons):
                try:
                    button_text = await button.text_content()
                    button_class = await button.get_attribute("class")
                    button_type = await button.get_attribute("type")
                    is_visible = await button.is_visible()
                    
                    if button_text and button_text.strip() and button_count < 30:
                        print(f"    {button_count+1}. {button_text} (class: {button_class}, type: {button_type}, visible: {is_visible})")
                        button_count += 1
                except Exception:
                    continue
                    
        except Exception as e:
            print(f"  ❌ 버튼 분석 중 오류: {e}")

    async def analyze_all_input_fields(self, page):
        """모든 입력 필드 분석"""
        print("📝 모든 입력 필드 분석:")
        
        try:
            all_inputs = await page.query_selector_all("input, textarea, select")
            print(f"  📝 총 입력 필드 수: {len(all_inputs)}")
            
            for i, input_field in enumerate(all_inputs):
                try:
                    input_type = await input_field.get_attribute("type")
                    placeholder = await input_field.get_attribute("placeholder")
                    input_id = await input_field.get_attribute("id")
                    input_name = await input_field.get_attribute("name")
                    is_visible = await input_field.is_visible()
                    
                    if is_visible:
                        print(f"    {i+1}. type: {input_type}, placeholder: {placeholder}, id: {input_id}, name: {input_name}")
                except Exception:
                    continue
                    
        except Exception as e:
            print(f"  ❌ 입력 필드 분석 중 오류: {e}")

    async def analyze_all_links(self, page):
        """모든 링크 분석"""
        print("🔗 모든 링크 분석:")
        
        try:
            all_links = await page.query_selector_all("a")
            print(f"  🔗 총 링크 수: {len(all_links)}")
            
            # 중요한 링크들만 표시 (최대 20개)
            link_count = 0
            for i, link in enumerate(all_links):
                try:
                    link_text = await link.text_content()
                    link_href = await link.get_attribute("href")
                    is_visible = await link.is_visible()
                    
                    if link_text and link_text.strip() and link_count < 20:
                        print(f"    {link_count+1}. {link_text} (href: {link_href}, visible: {is_visible})")
                        link_count += 1
                except Exception:
                    continue
                    
        except Exception as e:
            print(f"  ❌ 링크 분석 중 오류: {e}")

    async def analyze_all_images(self, page):
        """모든 이미지 분석"""
        print("🖼️ 모든 이미지 분석:")
        
        try:
            all_images = await page.query_selector_all("img")
            print(f"  🖼️ 총 이미지 수: {len(all_images)}")
            
            # 중요한 이미지들만 표시 (최대 15개)
            image_count = 0
            for i, img in enumerate(all_images):
                try:
                    img_src = await img.get_attribute("src")
                    img_alt = await img.get_attribute("alt")
                    img_class = await img.get_attribute("class")
                    is_visible = await img.is_visible()
                    
                    if img_src and image_count < 15:
                        print(f"    {image_count+1}. src: {img_src}, alt: {img_alt}, class: {img_class}, visible: {is_visible}")
                        image_count += 1
                except Exception:
                    continue
                    
        except Exception as e:
            print(f"  ❌ 이미지 분석 중 오류: {e}")

    async def analyze_specific_areas(self, page):
        """특정 영역별 상세 분석"""
        print("🎯 특정 영역별 상세 분석:")
        
        # 1. 헤더 영역
        print("\n  📋 1. 헤더 영역:")
        try:
            header_elements = await page.query_selector_all("header, .header, .navbar, .nav-bar, [class*='header'], [class*='navbar']")
            print(f"    헤더 요소 수: {len(header_elements)}")
            
            for i, header in enumerate(header_elements[:3]):  # 최대 3개만
                try:
                    header_text = await header.text_content()
                    if header_text and len(header_text.strip()) < 200:
                        print(f"      {i+1}. {header_text.strip()[:100]}...")
                except Exception:
                    continue
        except Exception as e:
            print(f"    ❌ 헤더 분석 실패: {e}")
        
        # 2. 사이드바 영역
        print("\n  📋 2. 사이드바 영역:")
        try:
            sidebar_elements = await page.query_selector_all(".sidebar, .side-panel, [class*='sidebar'], [class*='side']")
            print(f"    사이드바 요소 수: {len(sidebar_elements)}")
            
            for i, sidebar in enumerate(sidebar_elements[:3]):  # 최대 3개만
                try:
                    sidebar_text = await sidebar.text_content()
                    if sidebar_text and len(sidebar_text.strip()) < 200:
                        print(f"      {i+1}. {sidebar_text.strip()[:100]}...")
                except Exception:
                    continue
        except Exception as e:
            print(f"    ❌ 사이드바 분석 실패: {e}")
        
        # 3. 메인 콘텐츠 영역
        print("\n  📋 3. 메인 콘텐츠 영역:")
        try:
            main_elements = await page.query_selector_all("main, .main, .content, [class*='main'], [class*='content']")
            print(f"    메인 콘텐츠 요소 수: {len(main_elements)}")
            
            for i, main in enumerate(main_elements[:3]):  # 최대 3개만
                try:
                    main_text = await main.text_content()
                    if main_text and len(main_text.strip()) < 200:
                        print(f"      {i+1}. {main_text.strip()[:100]}...")
                except Exception:
                    continue
        except Exception as e:
            print(f"    ❌ 메인 콘텐츠 분석 실패: {e}")
        
        # 4. 푸터 영역
        print("\n  📋 4. 푸터 영역:")
        try:
            footer_elements = await page.query_selector_all("footer, .footer, [class*='footer']")
            print(f"    푸터 요소 수: {len(footer_elements)}")
            
            for i, footer in enumerate(footer_elements[:3]):  # 최대 3개만
                try:
                    footer_text = await footer.text_content()
                    if footer_text and len(footer_text.strip()) < 200:
                        print(f"      {i+1}. {footer_text.strip()[:100]}...")
                except Exception:
                    continue
        except Exception as e:
            print(f"    ❌ 푸터 분석 실패: {e}")


if __name__ == "__main__":
    asyncio.run(TestTagTestSiteAnalysis().test_analyze_tag_test_site_elements())
