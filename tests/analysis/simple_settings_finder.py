#!/usr/bin/env python3
"""
Simple Settings Finder
설정 메뉴를 찾는 간단한 테스트
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

async def find_settings_menu(environment: str = "dev"):
    """설정 메뉴 찾기"""
    print(f"🔍 {environment.upper()} 환경에서 설정 메뉴 찾기...")
    
    config = get_config(environment)
    
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
            return False
        
        print("✅ 로그인 성공")
        
        # 대시보드로 이동
        await asyncio.sleep(3)
        
        print("\n" + "=" * 60)
        print("🔍 설정 메뉴 찾기")
        print("=" * 60)
        
        # 1. 페이지에서 설정 관련 텍스트 찾기
        print("\n📋 1. 설정 관련 텍스트 찾기")
        print("-" * 30)
        
        try:
            # 설정 관련 키워드들
            settings_keywords = [
                "설정", "Settings", "Config", "Configuration", "Preferences",
                "옵션", "Options", "관리", "Management", "Admin",
                "프로필", "Profile", "계정", "Account", "사용자", "User"
            ]
            
            found_elements = []
            for keyword in settings_keywords:
                try:
                    elements = await browser_manager.page.query_selector_all(f":has-text('{keyword}')")
                    for elem in elements:
                        try:
                            if await elem.is_visible():
                                text = await elem.text_content()
                                tag_name = await elem.evaluate("el => el.tagName.toLowerCase()")
                                classes = await elem.get_attribute("class")
                                
                                if text and text.strip():
                                    found_elements.append({
                                        "keyword": keyword,
                                        "text": text.strip(),
                                        "tag": tag_name,
                                        "classes": classes
                                    })
                        except:
                            continue
                except:
                    continue
            
            print(f"📝 설정 관련 요소들 ({len(found_elements)}개):")
            for i, elem_info in enumerate(found_elements[:10]):  # 처음 10개만
                print(f"  {i+1}. [{elem_info['keyword']}] <{elem_info['tag']}> {elem_info['text']}")
                print(f"     클래스: {elem_info['classes']}")
                print()
                
        except Exception as e:
            print(f"❌ 설정 관련 텍스트 찾기 실패: {e}")
        
        # 2. 헤더 영역에서 버튼/링크 찾기
        print("\n📋 2. 헤더 영역에서 버튼/링크 찾기")
        print("-" * 30)
        
        try:
            # 헤더 관련 셀렉터들
            header_selectors = [
                "header",
                ".header",
                ".main-header",
                ".el-header",
                ".global-navigation",
                ".top-navigation",
                ".navbar",
                ".nav-bar"
            ]
            
            header_found = False
            for selector in header_selectors:
                try:
                    header = await browser_manager.page.query_selector(selector)
                    if header and await header.is_visible():
                        print(f"✅ 헤더 발견: {selector}")
                        header_found = True
                        
                        # 헤더 내부의 모든 클릭 가능한 요소들 찾기
                        clickable_elements = await header.query_selector_all("button, a, [role='button'], [tabindex='0']")
                        print(f"📝 헤더 내 클릭 가능한 요소들 ({len(clickable_elements)}개):")
                        
                        for i, elem in enumerate(clickable_elements[:15]):  # 처음 15개만
                            try:
                                text = await elem.text_content()
                                tag_name = await elem.evaluate("el => el.tagName.toLowerCase()")
                                classes = await elem.get_attribute("class")
                                
                                if text and text.strip() and len(text.strip()) < 50:
                                    print(f"  {i+1}. <{tag_name}> {text.strip()}")
                                    print(f"     클래스: {classes}")
                                    print()
                            except:
                                continue
                        break
                except:
                    continue
            
            if not header_found:
                print("❌ 헤더를 찾을 수 없음")
                
        except Exception as e:
            print(f"❌ 헤더 영역 분석 실패: {e}")
        
        # 3. 페이지 전체에서 아이콘 찾기
        print("\n📋 3. 페이지 전체에서 아이콘 찾기")
        print("-" * 30)
        
        try:
            # 아이콘 관련 요소들 찾기
            icon_selectors = [
                "i", ".icon", ".fa", ".fas", ".far", ".material-icons",
                "[class*='icon']", "[class*='Icon']", "[class*='fa']"
            ]
            
            icons_found = []
            for selector in icon_selectors:
                try:
                    icons = await browser_manager.page.query_selector_all(selector)
                    for icon in icons:
                        try:
                            if await icon.is_visible():
                                classes = await icon.get_attribute("class")
                                parent_text = await icon.evaluate("el => el.parentElement ? el.parentElement.textContent : ''")
                                
                                if classes:
                                    icons_found.append({
                                        "selector": selector,
                                        "classes": classes,
                                        "parent_text": parent_text.strip() if parent_text else ""
                                    })
                        except:
                            continue
                except:
                    continue
            
            print(f"📝 아이콘 요소들 ({len(icons_found)}개):")
            for i, icon_info in enumerate(icons_found[:15]):  # 처음 15개만
                print(f"  {i+1}. {icon_info['selector']} (클래스: {icon_info['classes']})")
                if icon_info['parent_text']:
                    print(f"     부모 텍스트: {icon_info['parent_text']}")
                print()
                
        except Exception as e:
            print(f"❌ 아이콘 요소 분석 실패: {e}")
        
        # 4. 스크린샷 저장
        print("\n📋 4. 스크린샷 저장")
        print("-" * 30)
        
        try:
            screenshot_path = await browser_manager.page.screenshot(path="reports/dev/screenshots/settings_finder.png")
            print(f"📸 스크린샷 저장: {screenshot_path}")
        except Exception as e:
            print(f"❌ 스크린샷 저장 실패: {e}")
        
        print("\n" + "=" * 60)
        print("✅ 설정 메뉴 찾기 완료")
        print("=" * 60)
        
        return True

async def main():
    """메인 실행 함수"""
    print("🚀 설정 메뉴 찾기 시작")
    print("=" * 60)
    
    try:
        success = await find_settings_menu("dev")
        if success:
            print("✅ 설정 메뉴 찾기 성공!")
        else:
            print("❌ 설정 메뉴 찾기 실패")
    except Exception as e:
        print(f"❌ 찾기 실패: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 설정 메뉴 찾기 완료")

if __name__ == "__main__":
    asyncio.run(main())
