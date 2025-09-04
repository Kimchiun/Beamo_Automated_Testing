#!/usr/bin/env python3
"""
Final Gear Settings Test - Click All Menu Items
발견된 톱니바퀴 버튼을 클릭하고 드롭다운 메뉴의 모든 항목을 순차적으로 클릭하여 동작을 분석하는 최종 테스트
"""

import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.config_loader import get_config
from utils.browser_manager import BrowserFactory
from pages.login_page import LoginPage

async def test_gear_settings_final_click_all_menu_items(environment: str = "dev"):
    print(f"🔍 {environment.upper()} 환경에서 톱니바퀴 설정 버튼 최종 테스트...")
    config = get_config(environment)
    
    async with BrowserFactory.create(config) as browser_manager:
        # 1. 로그인
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
        
        await asyncio.sleep(5)
        
        # 2. 톱니바퀴 버튼 찾기 (발견된 정확한 셀렉터 사용)
        print("\n🔍 톱니바퀴 버튼 찾기...")
        
        # 여러 셀렉터로 시도
        gear_button_selectors = [
            "i.el-icon-s-tools",
            "button:has(i.el-icon-s-tools)",
            ".header-btn00:has(i.el-icon-s-tools)",
            "[class*='header-btn']:has(i.el-icon-s-tools)"
        ]
        
        gear_button = None
        used_selector = ""
        
        for selector in gear_button_selectors:
            try:
                button = await browser_manager.page.query_selector(selector)
                if button and await button.is_visible():
                    gear_button = button
                    used_selector = selector
                    print(f"✅ 톱니바퀴 버튼 발견: {selector}")
                    break
            except Exception as e:
                continue
        
        if not gear_button:
            print("❌ 톱니바퀴 버튼을 찾을 수 없습니다")
            return False
        
        # 3. 클릭 전 스크린샷
        print("\n📸 클릭 전 스크린샷 저장...")
        await browser_manager.page.screenshot(path="reports/dev/screenshots/gear_settings_before_click.png")
        
        # 4. 톱니바퀴 버튼 클릭
        print(f"\n🔧 톱니바퀴 버튼 클릭: {used_selector}")
        
        try:
            # 스크롤하여 버튼이 보이도록 함
            await gear_button.scroll_into_view_if_needed()
            await asyncio.sleep(1)
            
            # 클릭 실행
            await gear_button.click()
            print("✅ 톱니바퀴 버튼 클릭 성공")
            
            # 드롭다운 메뉴가 나타날 때까지 대기
            await asyncio.sleep(3)
            
        except Exception as e:
            print(f"❌ 톱니바퀴 버튼 클릭 실패: {e}")
            return False
        
        # 5. 클릭 후 스크린샷
        print("\n📸 클릭 후 스크린샷 저장...")
        await browser_manager.page.screenshot(path="reports/dev/screenshots/gear_settings_after_click.png")
        
        # 6. 드롭다운 메뉴 요소 찾기
        print("\n🔍 드롭다운 메뉴 요소 찾기...")
        
        # 드롭다운 메뉴의 모든 메뉴 항목 찾기
        menu_items = await browser_manager.page.query_selector_all("li.el-menu-item")
        print(f"발견된 메뉴 항목: {len(menu_items)}개")
        
        if len(menu_items) == 0:
            print("❌ 드롭다운 메뉴 항목을 찾을 수 없습니다")
            return False
        
        # 7. 각 메뉴 항목의 정보 출력
        print("\n📋 드롭다운 메뉴 항목 정보:")
        for i, item in enumerate(menu_items):
            try:
                text = await item.text_content() or ""
                classes = await item.get_attribute("class") or ""
                print(f"  {i+1}. {text} (class: {classes})")
            except Exception as e:
                print(f"  {i+1}. 항목 정보 읽기 실패: {e}")
        
        # 8. 메뉴 항목들을 카테고리별로 분류
        print("\n📂 메뉴 항목 카테고리별 분류:")
        
        # Space Management 항목들
        space_management_items = []
        user_management_items = []
        data_management_items = []
        
        for item in menu_items:
            try:
                text = await item.text_content() or ""
                if text.strip():
                    if text in ["License Details", "Security", "All Spaces and Licenses", "Preferences", "Filter"]:
                        space_management_items.append(item)
                    elif text in ["Teams", "Users"]:
                        user_management_items.append(item)
                    elif text in ["Overview", "Shared Survey", "Recovery"]:
                        data_management_items.append(item)
            except:
                continue
        
        print(f"  🏢 Space Management: {len(space_management_items)}개")
        for item in space_management_items:
            text = await item.text_content() or ""
            print(f"    - {text}")
        
        print(f"  👥 User Management: {len(user_management_items)}개")
        for item in user_management_items:
            text = await item.text_content() or ""
            print(f"    - {text}")
        
        print(f"  📊 Data Management: {len(data_management_items)}개")
        for item in data_management_items:
            text = await item.text_content() or ""
            print(f"    - {text}")
        
        # 9. 각 메뉴 항목을 순차적으로 클릭하고 동작 분석
        print("\n🔍 각 메뉴 항목 클릭 및 동작 분석...")
        
        all_menu_items = space_management_items + user_management_items + data_management_items
        
        for i, item in enumerate(all_menu_items):
            try:
                text = await item.text_content() or ""
                print(f"\n--- {i+1}. {text} 클릭 테스트 ---")
                
                # 클릭 전 상태 기록
                before_url = browser_manager.page.url
                before_title = await browser_manager.page.title()
                
                # 클릭 전 스크린샷
                await browser_manager.page.screenshot(path=f"reports/dev/screenshots/menu_item_{i+1}_{text.replace(' ', '_')}_before.png")
                
                # 메뉴 항목 클릭
                print(f"  클릭 시도: {text}")
                await item.click()
                await asyncio.sleep(2)
                
                # 클릭 후 상태 확인
                after_url = browser_manager.page.url
                after_title = await browser_manager.page.title()
                
                # 클릭 후 스크린샷
                await browser_manager.page.screenshot(path=f"reports/dev/screenshots/menu_item_{i+1}_{text.replace(' ', '_')}_after.png")
                
                # 변화 분석
                url_changed = before_url != after_url
                title_changed = before_title != after_title
                
                print(f"  URL 변화: {'예' if url_changed else '아니오'}")
                if url_changed:
                    print(f"    이전: {before_url}")
                    print(f"    이후: {after_url}")
                
                print(f"  제목 변화: {'예' if title_changed else '아니오'}")
                if title_changed:
                    print(f"    이전: {before_title}")
                    print(f"    이후: {after_title}")
                
                # 새로운 모달/팝업/페이지 요소 확인
                new_elements = await browser_manager.page.query_selector_all("[class*='modal'], [class*='popup'], [class*='dialog'], [class*='page']")
                visible_new_elements = [elem for elem in new_elements if await elem.is_visible()]
                
                print(f"  새로운 요소: {len(visible_new_elements)}개")
                for j, elem in enumerate(visible_new_elements[:3]):  # 처음 3개만 표시
                    try:
                        tag_name = await elem.evaluate('el => el.tagName.toLowerCase()')
                        classes = await elem.get_attribute("class") or ""
                        print(f"    {j+1}. {tag_name} (class: {classes})")
                    except:
                        continue
                
                # 뒤로가기 (브라우저 히스토리)
                if url_changed:
                    print("  뒤로가기 실행...")
                    await browser_manager.page.go_back()
                    await asyncio.sleep(2)
                    
                    # 뒤로가기 후 톱니바퀴 버튼 다시 클릭하여 메뉴 복원
                    try:
                        gear_button = await browser_manager.page.query_selector(used_selector)
                        if gear_button and await gear_button.is_visible():
                            await gear_button.click()
                            await asyncio.sleep(2)
                            print("  ✅ 메뉴 복원 성공")
                        else:
                            print("  ❌ 메뉴 복원 실패")
                    except Exception as e:
                        print(f"  ❌ 메뉴 복원 중 오류: {e}")
                
                print(f"  ✅ {text} 테스트 완료")
                
            except Exception as e:
                print(f"  ❌ {text} 테스트 실패: {e}")
                continue
        
        # 10. 최종 스크린샷
        print("\n📸 최종 스크린샷 저장...")
        await browser_manager.page.screenshot(path="reports/dev/screenshots/gear_settings_final_test_complete.png")
        
        # 11. 결과 요약
        print("\n" + "=" * 80)
        print("📊 톱니바퀴 설정 버튼 최종 테스트 결과")
        print("=" * 80)
        print(f"🔧 사용된 셀렉터: {used_selector}")
        print(f"📸 클릭 전: reports/dev/screenshots/gear_settings_before_click.png")
        print(f"📸 클릭 후: reports/dev/screenshots/gear_settings_after_click.png")
        print(f"📸 최종: reports/dev/screenshots/gear_settings_final_test_complete.png")
        print(f"🏢 Space Management 항목: {len(space_management_items)}개")
        print(f"👥 User Management 항목: {len(user_management_items)}개")
        print(f"📊 Data Management 항목: {len(data_management_items)}개")
        print(f"🔍 총 테스트된 메뉴 항목: {len(all_menu_items)}개")
        
        print("\n🎉 모든 메뉴 항목 클릭 테스트 완료!")
        return True

async def main():
    """메인 실행 함수"""
    try:
        result = await test_gear_settings_final_click_all_menu_items("dev")
        if result:
            print("\n🎉 테스트 성공!")
        else:
            print("\n❌ 테스트 실패")
    except Exception as e:
        print(f"\n💥 테스트 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
