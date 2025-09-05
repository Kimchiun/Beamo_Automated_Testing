#!/usr/bin/env python3
"""
Global Navigation Buttons Test
글로벌 네비게이션의 각 버튼을 클릭하고 어떤 일이 생기는지 테스트합니다.
"""

import asyncio
import sys
from pathlib import Path
from functools import wraps

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.config_loader import get_config
from utils.browser_manager import BrowserFactory
from pages.login_page import LoginPage
from pages.components.global_navigation import GlobalNavigation

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

async def test_global_navigation_buttons(environment: str = "dev"):
    """글로벌 네비게이션 버튼 테스트"""
    print(f"🔍 {environment.upper()} 환경에서 글로벌 네비게이션 버튼 테스트...")
    
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
        
        # 글로벌 네비게이션 초기화
        global_nav = GlobalNavigation(browser_manager.page, config)
        
        print("\n" + "=" * 80)
        print("🔍 글로벌 네비게이션 버튼 테스트")
        print("=" * 80)
        
        # 1. 글로벌 네비게이션 로드 확인
        print("\n📋 1. 글로벌 네비게이션 로드 확인")
        print("-" * 50)
        
        try:
            await global_nav.wait_for_navigation_load()
            print("✅ 글로벌 네비게이션 로드 완료")
        except Exception as e:
            print(f"❌ 글로벌 네비게이션 로드 실패: {e}")
            return False
        
        # 2. 모든 클릭 가능한 요소 찾기
        print("\n📋 2. 글로벌 네비게이션의 모든 클릭 가능한 요소 찾기")
        print("-" * 50)
        
        clickable_selectors = [
            "button",
            "a",
            "[role='button']",
            "[onclick]",
            "[class*='btn']",
            "[class*='button']",
            "[class*='link']",
            "[class*='nav-item']",
            "[class*='menu-item']"
        ]
        
        all_clickable = []
        for selector in clickable_selectors:
            try:
                elements = await browser_manager.page.query_selector_all(selector)
                for elem in elements:
                    try:
                        if await elem.is_visible():
                            # 부모가 글로벌 네비게이션 영역인지 확인
                            parent_nav = await elem.evaluate("""
                                el => {
                                    let parent = el.parentElement;
                                    while (parent) {
                                        if (parent.tagName === 'NAV' || 
                                            parent.className.includes('nav') || 
                                            parent.className.includes('header') ||
                                            parent.className.includes('top')) {
                                            return true;
                                        }
                                        parent = parent.parentElement;
                                    }
                                    return false;
                                }
                            """)
                            
                            if parent_nav:
                                tag_name = await elem.evaluate("el => el.tagName.toLowerCase()")
                                classes = await elem.get_attribute("class")
                                elem_text = await elem.text_content()
                                href = await elem.get_attribute("href")
                                title = await elem.get_attribute("title")
                                aria_label = await elem.get_attribute("aria-label")
                                
                                all_clickable.append({
                                    "tag": tag_name,
                                    "classes": classes,
                                    "text": elem_text,
                                    "href": href,
                                    "title": title,
                                    "aria_label": aria_label,
                                    "selector": selector,
                                    "element": elem
                                })
                    except:
                        continue
            except:
                continue
        
        print(f"📊 글로벌 네비게이션에서 발견된 클릭 가능한 요소: {len(all_clickable)}개")
        
        if all_clickable:
            print("\n📋 발견된 요소들:")
            for i, elem in enumerate(all_clickable):
                print(f"\n{i+1}. <{elem['tag']}>")
                print(f"   - 텍스트: {elem['text']}")
                print(f"   - 클래스: {elem['classes']}")
                print(f"   - href: {elem['href']}")
                print(f"   - title: {elem['title']}")
                print(f"   - aria-label: {elem['aria_label']}")
                print(f"   - 셀렉터: {elem['selector']}")
        
        # 3. 각 버튼 클릭 테스트
        print("\n📋 3. 각 버튼 클릭 테스트")
        print("-" * 50)
        
        button_results = []
        
        for i, elem_info in enumerate(all_clickable):
            try:
                print(f"\n🔍 {i+1}번째 버튼 테스트: {elem_info['text']}")
                print(f"   - 태그: <{elem_info['tag']}>")
                print(f"   - 클래스: {elem_info['classes']}")
                
                # 클릭 전 상태 저장
                before_url = browser_manager.page.url
                before_title = await browser_manager.page.title()
                
                # 스크린샷 저장 (클릭 전)
                before_screenshot = f"reports/dev/screenshots/button_{i+1}_{elem_info['text'][:20]}_before.png"
                await browser_manager.page.screenshot(path=before_screenshot)
                
                # 버튼 클릭
                print("   - 버튼 클릭 시도...")
                await elem_info['element'].click()
                
                # 클릭 후 대기
                await asyncio.sleep(2)
                
                # 클릭 후 상태 확인
                after_url = browser_manager.page.url
                after_title = await browser_manager.page.title()
                
                # 스크린샷 저장 (클릭 후)
                after_screenshot = f"reports/dev/screenshots/button_{i+1}_{elem_info['text'][:20]}_after.png"
                await browser_manager.page.screenshot(path=after_screenshot)
                
                # 결과 분석
                url_changed = before_url != after_url
                title_changed = before_title != after_title
                
                # 모달이나 드롭다운이 열렸는지 확인
                modal_opened = False
                dropdown_opened = False
                
                try:
                    # 모달 확인
                    modals = await browser_manager.page.query_selector_all("[class*='modal'], [class*='dialog'], [class*='popup']")
                    for modal in modals:
                        if await modal.is_visible():
                            modal_opened = True
                            break
                    
                    # 드롭다운 확인
                    dropdowns = await browser_manager.page.query_selector_all("[class*='dropdown'], [class*='menu'], [class*='popover']")
                    for dropdown in dropdowns:
                        if await dropdown.is_visible():
                            dropdown_opened = True
                            break
                except:
                    pass
                
                # 결과 저장
                result = {
                    "button_text": elem_info['text'],
                    "button_tag": elem_info['tag'],
                    "button_classes": elem_info['classes'],
                    "url_changed": url_changed,
                    "title_changed": title_changed,
                    "modal_opened": modal_opened,
                    "dropdown_opened": dropdown_opened,
                    "before_url": before_url,
                    "after_url": after_url,
                    "before_title": before_title,
                    "after_title": after_title,
                    "before_screenshot": before_screenshot,
                    "after_screenshot": after_screenshot
                }
                
                button_results.append(result)
                
                # 결과 출력
                print(f"   ✅ 클릭 완료")
                if url_changed:
                    print(f"   - URL 변경: {before_url} → {after_url}")
                if title_changed:
                    print(f"   - 제목 변경: {before_title} → {after_title}")
                if modal_opened:
                    print(f"   - 모달/다이얼로그 열림")
                if dropdown_opened:
                    print(f"   - 드롭다운/메뉴 열림")
                if not url_changed and not title_changed and not modal_opened and not dropdown_opened:
                    print(f"   - 변화 없음 (토글 버튼일 가능성)")
                
                # 페이지 뒤로가기 (URL이 변경된 경우)
                if url_changed:
                    print("   - 페이지 뒤로가기...")
                    await browser_manager.page.go_back()
                    await asyncio.sleep(2)
                
                # 모달/드롭다운 닫기 (열린 경우)
                if modal_opened or dropdown_opened:
                    print("   - 모달/드롭다운 닫기...")
                    try:
                        # ESC 키로 닫기 시도
                        await browser_manager.page.keyboard.press("Escape")
                        await asyncio.sleep(1)
                    except:
                        pass
                
            except Exception as e:
                print(f"   ❌ 버튼 클릭 실패: {e}")
                button_results.append({
                    "button_text": elem_info['text'],
                    "button_tag": elem_info['tag'],
                    "button_classes": elem_info['classes'],
                    "error": str(e)
                })
        
        # 4. 결과 요약
        print("\n📋 4. 버튼 클릭 테스트 결과 요약")
        print("-" * 50)
        
        print(f"\n📊 총 테스트한 버튼: {len(button_results)}개")
        
        url_changed_count = sum(1 for r in button_results if r.get('url_changed', False))
        title_changed_count = sum(1 for r in button_results if r.get('title_changed', False))
        modal_opened_count = sum(1 for r in button_results if r.get('modal_opened', False))
        dropdown_opened_count = sum(1 for r in button_results if r.get('dropdown_opened', False))
        error_count = sum(1 for r in button_results if 'error' in r)
        
        print(f"✅ URL 변경: {url_changed_count}개")
        print(f"✅ 제목 변경: {title_changed_count}개")
        print(f"✅ 모달 열림: {modal_opened_count}개")
        print(f"✅ 드롭다운 열림: {dropdown_opened_count}개")
        print(f"❌ 오류 발생: {error_count}개")
        
        # 5. 상세 결과 출력
        print("\n📋 5. 상세 결과")
        print("-" * 50)
        
        for i, result in enumerate(button_results):
            print(f"\n{i+1}. {result['button_text']} (<{result['button_tag']}>)")
            if 'error' in result:
                print(f"   ❌ 오류: {result['error']}")
            else:
                if result['url_changed']:
                    print(f"   🔗 URL 변경: {result['before_url']} → {result['after_url']}")
                if result['title_changed']:
                    print(f"   📝 제목 변경: {result['before_title']} → {result['after_title']}")
                if result['modal_opened']:
                    print(f"   🪟 모달/다이얼로그 열림")
                if result['dropdown_opened']:
                    print(f"   📋 드롭다운/메뉴 열림")
                if not any([result['url_changed'], result['title_changed'], result['modal_opened'], result['dropdown_opened']]):
                    print(f"   🔄 변화 없음 (토글 또는 상태 변경)")
        
        # 6. 최종 스크린샷 저장
        print("\n📋 6. 최종 페이지 스크린샷 저장")
        print("-" * 50)
        
        try:
            final_screenshot_path = await browser_manager.page.screenshot(path="reports/dev/screenshots/global_navigation_buttons_test_final.png")
            print(f"📸 최종 스크린샷 저장: {final_screenshot_path}")
        except Exception as e:
            print(f"❌ 최종 스크린샷 저장 실패: {e}")
        
        print("\n" + "=" * 80)
        print("✅ 글로벌 네비게이션 버튼 테스트 완료")
        print("=" * 80)
        
        return True

async def main():
    """메인 실행 함수"""
    print("🚀 글로벌 네비게이션 버튼 테스트 시작")
    print("=" * 80)
    
    try:
        success = await test_global_navigation_buttons("dev")
        if success:
            print("✅ 글로벌 네비게이션 버튼 테스트 성공!")
        else:
            print("❌ 글로벌 네비게이션 버튼 테스트 실패")
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
    
    print("\n" + "=" * 80)
    print("✅ 글로벌 네비게이션 버튼 테스트 완료")

if __name__ == "__main__":
    asyncio.run(main())
