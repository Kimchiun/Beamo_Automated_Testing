#!/usr/bin/env python3
"""
Page Structure Analysis Test
현재 페이지의 전체 구조를 분석하여 설정 관련 요소들을 찾습니다.
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

async def analyze_page_structure(environment: str = "dev"):
    """페이지 구조 분석"""
    print(f"🔍 {environment.upper()} 환경 페이지 구조 분석 시작...")
    
    config = get_config(environment)
    
    async with BrowserFactory.create(config) as browser_manager:
        # 로그인
        login_page = LoginPage(browser_manager.page, config)
        await login_page.navigate_to_login()
        await login_page.wait_for_page_load()
        
        space_id = "d-ge-pr"
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
        print("🔍 페이지 구조 분석")
        print("=" * 60)
        
        # 1. 헤더 영역 분석
        print("\n📋 1. 헤더 영역 분석")
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
                        
                        # 헤더 내부 요소들 분석
                        header_elements = await header.query_selector_all("*")
                        print(f"📝 헤더 내부 요소 개수: {len(header_elements)}")
                        
                        # 헤더 내부의 주요 요소들 찾기
                        for elem in header_elements[:20]:  # 처음 20개만
                            try:
                                tag_name = await elem.evaluate("el => el.tagName.toLowerCase()")
                                text = await elem.text_content()
                                classes = await elem.get_attribute("class")
                                
                                if text and text.strip() and len(text.strip()) < 50:  # 짧은 텍스트만
                                    print(f"  <{tag_name}> {text.strip()} (클래스: {classes})")
                            except:
                                continue
                        break
                except:
                    continue
            
            if not header_found:
                print("❌ 헤더를 찾을 수 없음")
                
        except Exception as e:
            print(f"❌ 헤더 분석 실패: {e}")
        
        # 2. 상단 네비게이션 영역 분석
        print("\n📋 2. 상단 네비게이션 영역 분석")
        print("-" * 30)
        
        try:
            # 상단에 있는 모든 버튼, 링크, 아이콘 찾기
            top_elements = await browser_manager.page.query_selector_all("header *, .header *, .main-header *, .el-header *")
            
            print(f"📝 상단 요소들 ({len(top_elements)}개):")
            visible_count = 0
            
            for elem in top_elements:
                try:
                    if await elem.is_visible():
                        tag_name = await elem.evaluate("el => el.tagName.toLowerCase()")
                        text = await elem.text_content()
                        classes = await elem.get_attribute("class")
                        href = await elem.get_attribute("href")
                        
                        if text and text.strip() and len(text.strip()) < 100:
                            visible_count += 1
                            if visible_count <= 15:  # 처음 15개만
                                print(f"  {visible_count}. <{tag_name}> {text.strip()}")
                                print(f"     클래스: {classes}")
                                if href:
                                    print(f"     링크: {href}")
                                print()
                            
                except:
                    continue
            
            print(f"📊 총 가시적 요소: {visible_count}개")
            
        except Exception as e:
            print(f"❌ 상단 네비게이션 분석 실패: {e}")
        
        # 3. 설정 관련 키워드 검색
        print("\n📋 3. 설정 관련 키워드 검색")
        print("-" * 30)
        
        try:
            # 설정 관련 텍스트를 포함한 요소들 찾기
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
                                        "classes": classes,
                                        "element": elem
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
            print(f"❌ 설정 관련 키워드 검색 실패: {e}")
        
        # 4. 아이콘 및 버튼 요소 분석
        print("\n📋 4. 아이콘 및 버튼 요소 분석")
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
        
        # 5. 페이지 스크린샷 저장
        print("\n📋 5. 페이지 스크린샷 저장")
        print("-" * 30)
        
        try:
            screenshot_path = await browser_manager.page.screenshot(path="reports/dev/screenshots/page_structure_analysis.png")
            print(f"📸 페이지 구조 분석 스크린샷 저장: {screenshot_path}")
        except Exception as e:
            print(f"❌ 스크린샷 저장 실패: {e}")
        
        print("\n" + "=" * 60)
        print("✅ 페이지 구조 분석 완료")
        print("=" * 60)
        
        return True

async def main():
    """메인 실행 함수"""
    print("🚀 페이지 구조 분석 시작")
    print("=" * 60)
    
    try:
        success = await analyze_page_structure("dev")
        if success:
            print("✅ 페이지 구조 분석 성공!")
        else:
            print("❌ 페이지 구조 분석 실패")
    except Exception as e:
        print(f"❌ 분석 실패: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 페이지 구조 분석 완료")

if __name__ == "__main__":
    asyncio.run(main())
