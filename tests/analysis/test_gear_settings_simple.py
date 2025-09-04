#!/usr/bin/env python3
"""
Simple Gear Settings Test
톱니바퀴 버튼을 찾기 위한 간단한 테스트
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

async def test_gear_settings_simple(environment: str = "dev"):
    """간단한 톱니바퀴 설정 버튼 테스트"""
    print(f"🔍 {environment.upper()} 환경에서 간단한 톱니바퀴 설정 버튼 테스트...")
    
    config = get_config(environment)
    
    async with BrowserFactory.create(config) as browser_manager:
        # 로그인
        login_page = LoginPage(browser_manager.page, config)
        await login_page.navigate_to_login()
        await login_page.wait_for_page_load()
        
        space_id = "d-ge-eric"
        email = config.test_data.valid_user["email"]
        password = config.test_data.valid_user["password"]
        
        await login_page.login(space_id, email, password)
        
        if not await login_page.is_logged_in():
            print("❌ 로그인 실패")
            return False
        
        print("✅ 로그인 성공")
        
        # 대시보드로 이동
        await asyncio.sleep(3)
        
        print("\n" + "=" * 80)
        print("🔍 페이지 전체 요소 분석")
        print("=" * 80)
        
        # 1. 모든 버튼 요소 찾기
        print("\n📋 1. 모든 버튼 요소 찾기")
        print("-" * 50)
        
        buttons = await browser_manager.page.query_selector_all("button")
        print(f"발견된 버튼 수: {len(buttons)}")
        
        for i, button in enumerate(buttons):
            try:
                if await button.is_visible():
                    classes = await button.get_attribute("class")
                    text = await button.text_content()
                    title = await button.get_attribute("title")
                    aria_label = await button.get_attribute("aria-label")
                    
                    print(f"\n{i+1}. 버튼")
                    print(f"   - 클래스: {classes}")
                    print(f"   - 텍스트: {text}")
                    print(f"   - title: {title}")
                    print(f"   - aria-label: {aria_label}")
                    
                    # 톱니바퀴 관련 키워드 확인
                    if any(keyword in (classes or "") for keyword in ['gear', 'cog', 'settings', 'config']):
                        print(f"   ⭐ 톱니바퀴 관련 버튼 발견!")
                    
            except Exception as e:
                print(f"   ⚠️ 버튼 {i+1} 분석 오류: {e}")
        
        # 2. 모든 링크 요소 찾기
        print("\n📋 2. 모든 링크 요소 찾기")
        print("-" * 50)
        
        links = await browser_manager.page.query_selector_all("a")
        print(f"발견된 링크 수: {len(links)}")
        
        for i, link in enumerate(links):
            try:
                if await link.is_visible():
                    classes = await link.get_attribute("class")
                    text = await link.text_content()
                    href = await link.get_attribute("href")
                    title = await link.get_attribute("title")
                    
                    print(f"\n{i+1}. 링크")
                    print(f"   - 클래스: {classes}")
                    print(f"   - 텍스트: {text}")
                    print(f"   - href: {href}")
                    print(f"   - title: {title}")
                    
                    # 톱니바퀴 관련 키워드 확인
                    if any(keyword in (classes or "") for keyword in ['gear', 'cog', 'settings', 'config']):
                        print(f"   ⭐ 톱니바퀴 관련 링크 발견!")
                    
            except Exception as e:
                print(f"   ⚠️ 링크 {i+1} 분석 오류: {e}")
        
        # 3. 모든 SVG 아이콘 찾기
        print("\n📋 3. 모든 SVG 아이콘 찾기")
        print("-" * 50)
        
        svgs = await browser_manager.page.query_selector_all("svg")
        print(f"발견된 SVG 수: {len(svgs)}")
        
        for i, svg in enumerate(svgs):
            try:
                if await svg.is_visible():
                    classes = await svg.get_attribute("class")
                    parent_classes = await svg.parent_element.get_attribute("class") if svg.parent_element else None
                    
                    print(f"\n{i+1}. SVG")
                    print(f"   - 클래스: {classes}")
                    print(f"   - 부모 클래스: {parent_classes}")
                    
                    # 톱니바퀴 관련 키워드 확인
                    if any(keyword in (classes or "") for keyword in ['gear', 'cog', 'settings', 'config']):
                        print(f"   ⭐ 톱니바퀴 관련 SVG 발견!")
                    if any(keyword in (parent_classes or "") for keyword in ['gear', 'cog', 'settings', 'config']):
                        print(f"   ⭐ 톱니바퀴 관련 부모 요소 발견!")
                    
            except Exception as e:
                print(f"   ⚠️ SVG {i+1} 분석 오류: {e}")
        
        # 4. 페이지 전체에서 특정 텍스트 검색
        print("\n📋 4. 페이지 전체에서 특정 텍스트 검색")
        print("-" * 50)
        
        # 톱니바퀴 이모지 검색
        try:
            gear_elements = await browser_manager.page.query_selector_all(":has-text('⚙️')")
            print(f"⚙️ 이모지가 포함된 요소: {len(gear_elements)}개")
            
            for i, elem in enumerate(gear_elements):
                if await elem.is_visible():
                    tag_name = await elem.evaluate("el => el.tagName")
                    classes = await elem.get_attribute("class")
                    text = await elem.text_content()
                    print(f"   {i+1}. {tag_name} (클래스: {classes}, 텍스트: {text})")
        except Exception as e:
            print(f"   ⚠️ ⚙️ 이모지 검색 오류: {e}")
        
        # 5. 스크린샷 저장
        print("\n📋 5. 스크린샷 저장")
        print("-" * 50)
        
        screenshot = await browser_manager.page.screenshot(path="reports/dev/screenshots/gear_settings_simple_analysis.png")
        print(f"📸 스크린샷 저장: {screenshot}")
        
        return True

async def main():
    """메인 실행 함수"""
    print("🚀 간단한 톱니바퀴 설정 버튼 테스트 시작")
    print("=" * 80)
    
    try:
        success = await test_gear_settings_simple("dev")
        if success:
            print("✅ 간단한 톱니바퀴 설정 버튼 테스트 성공!")
        else:
            print("❌ 간단한 톱니바퀴 설정 버튼 테스트 실패")
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
    
    print("\n" + "=" * 80)
    print("✅ 간단한 톱니바퀴 설정 버튼 테스트 완료")

if __name__ == "__main__":
    asyncio.run(main())
