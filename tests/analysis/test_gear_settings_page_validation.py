#!/usr/bin/env python3
"""
Gear Settings Page Validation Test
각 메뉴 항목에 진입했을 때 정상적으로 페이지가 로드되고 필요한 요소들이 표시되는지 확인하는 테스트
"""

import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.config_loader import get_config
from utils.browser_manager import BrowserFactory
from pages.login_page import LoginPage

async def test_gear_settings_page_validation(environment: str = "dev"):
    print(f"🔍 {environment.upper()} 환경에서 톱니바퀴 설정 페이지 검증 테스트...")
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
        
        # 2. 톱니바퀴 버튼 찾기 및 클릭
        print("\n🔍 톱니바퀴 버튼 찾기...")
        
        gear_button = await browser_manager.page.query_selector("i.el-icon-s-tools")
        if not gear_button or not await gear_button.is_visible():
            print("❌ 톱니바퀴 버튼을 찾을 수 없습니다")
            return False
        
        print("✅ 톱니바퀴 버튼 발견")
        
        # 3. 페이지별 검증 정의
        page_validations = {
            "License Details": {
                "url_pattern": "/management/license/licenseDetail/",
                "expected_elements": [
                    "h1, h2, h3",  # 제목 요소
                    "[class*='license']",  # 라이선스 관련 요소
                    "[class*='detail']",  # 상세 정보 요소
                    "table",  # 테이블 요소
                    "[class*='info']"  # 정보 표시 요소
                ],
                "expected_text": ["License", "Details", "Information"]
            },
            "Security": {
                "url_pattern": "/management/security",
                "expected_elements": [
                    "h1, h2, h3",  # 제목 요소
                    "[class*='security']",  # 보안 관련 요소
                    "[class*='setting']",  # 설정 요소
                    "form",  # 폼 요소
                    "[class*='config']"  # 설정 요소
                ],
                "expected_text": ["Security", "Settings", "Configuration"]
            },
            "All Spaces and Licenses": {
                "url_pattern": "/management/license/licenses",
                "expected_elements": [
                    "h1, h2, h3",  # 제목 요소
                    "[class*='license']",  # 라이선스 관련 요소
                    "table",  # 테이블 요소
                    "[class*='list']",  # 목록 요소
                    "[class*='pager']"  # 페이지네이션
                ],
                "expected_text": ["Licenses", "Spaces", "Management"]
            },
            "Preferences": {
                "url_pattern": "/management/preferences/workspace",
                "expected_elements": [
                    "h1, h2, h3",  # 제목 요소
                    "[class*='preference']",  # 환경설정 관련 요소
                    "form",  # 폼 요소
                    "[class*='setting']",  # 설정 요소
                    "[class*='option']"  # 옵션 요소
                ],
                "expected_text": ["Preferences", "Workspace", "Settings"]
            },
            "Filter": {
                "url_pattern": "/management/sites/filter",
                "expected_elements": [
                    "h1, h2, h3",  # 제목 요소
                    "form",  # 폼 요소
                    "[class*='filter']",  # 필터 관련 요소
                    "[class*='option']",  # 옵션 요소
                    "[class*='button']"  # 버튼 요소
                ],
                "expected_text": ["Filter", "Sites", "Geographic"]
            },
            "Teams": {
                "url_pattern": "/management/teams/",
                "expected_elements": [
                    "h1, h2, h3",  # 제목 요소
                    "[class*='team']",  # 팀 관련 요소
                    "table",  # 테이블 요소
                    "[class*='list']",  # 목록 요소
                    "[class*='pager']"  # 페이지네이션
                ],
                "expected_text": ["Teams", "Management", "List"]
            },
            "Users": {
                "url_pattern": "/management/users",
                "expected_elements": [
                    "h1, h2, h3",  # 제목 요소
                    "[class*='user']",  # 사용자 관련 요소
                    "table",  # 테이블 요소
                    "[class*='list']",  # 목록 요소
                    "[class*='pager']"  # 페이지네이션
                ],
                "expected_text": ["Users", "Management", "List"]
            },
            "Overview": {
                "url_pattern": "/management/data/overview",
                "expected_elements": [
                    "h1, h2, h3",  # 제목 요소
                    "[class*='overview']",  # 개요 관련 요소
                    "[class*='chart']",  # 차트 요소
                    "[class*='stat']",  # 통계 요소
                    "[class*='summary']"  # 요약 요소
                ],
                "expected_text": ["Overview", "Data", "Management"]
            },
            "Shared Survey": {
                "url_pattern": "/management/data/shared/surveys",
                "expected_elements": [
                    "h1, h2, h3",  # 제목 요소
                    "[class*='survey']",  # 설문 관련 요소
                    "table",  # 테이블 요소
                    "[class*='list']",  # 목록 요소
                    "[class*='pager']"  # 페이지네이션
                ],
                "expected_text": ["Shared", "Surveys", "Management"]
            },
            "Recovery": {
                "url_pattern": "/management/data/recovery/site",
                "expected_elements": [
                    "h1, h2, h3",  # 제목 요소
                    "[class*='recovery']",  # 복구 관련 요소
                    "table",  # 테이블 요소
                    "[class*='list']",  # 목록 요소
                    "[class*='pager']"  # 페이지네이션
                ],
                "expected_text": ["Recovery", "Sites", "Management"]
            }
        }
        
        # 4. 각 페이지 검증 실행
        print("\n🔍 각 페이지 검증 시작...")
        
        validation_results = {}
        
        for page_name, validation in page_validations.items():
            try:
                print(f"\n--- {page_name} 페이지 검증 ---")
                
                # 톱니바퀴 버튼 클릭하여 메뉴 열기
                gear_button = await browser_manager.page.query_selector("i.el-icon-s-tools")
                if gear_button and await gear_button.is_visible():
                    await gear_button.click()
                    await asyncio.sleep(2)
                
                # 해당 메뉴 항목 찾기 및 클릭
                menu_item = await browser_manager.page.query_selector(f"li.el-menu-item:has-text('{page_name}')")
                if not menu_item:
                    print(f"  ❌ {page_name} 메뉴 항목을 찾을 수 없습니다")
                    validation_results[page_name] = {"status": "FAILED", "reason": "메뉴 항목을 찾을 수 없음"}
                    continue
                
                # 클릭 전 스크린샷
                safe_filename = page_name.replace(' ', '_').replace('/', '_').replace('&', 'and')
                await browser_manager.page.screenshot(path=f"reports/dev/screenshots/page_validation_{safe_filename}_before.png")
                
                # 메뉴 항목 클릭
                print(f"  클릭 시도: {page_name}")
                await menu_item.click()
                await asyncio.sleep(5)  # 페이지 로딩 대기
                
                # 클릭 후 스크린샷
                await browser_manager.page.screenshot(path=f"reports/dev/screenshots/page_validation_{safe_filename}_after.png")
                
                # URL 검증
                current_url = browser_manager.page.url
                url_valid = validation["url_pattern"] in current_url
                print(f"  URL 검증: {'✅' if url_valid else '❌'}")
                print(f"    현재 URL: {current_url}")
                print(f"    예상 패턴: {validation['url_pattern']}")
                
                # 페이지 제목 검증
                page_title = await browser_manager.page.title()
                print(f"  페이지 제목: {page_title}")
                
                # 예상 요소 검증
                element_validation_results = {}
                for selector in validation["expected_elements"]:
                    try:
                        elements = await browser_manager.page.query_selector_all(selector)
                        visible_elements = [elem for elem in elements if await elem.is_visible()]
                        element_validation_results[selector] = len(visible_elements)
                        print(f"    {selector}: {len(visible_elements)}개 발견")
                    except Exception as e:
                        element_validation_results[selector] = 0
                        print(f"    {selector}: 검증 실패 - {e}")
                
                # 예상 텍스트 검증
                text_validation_results = {}
                page_content = await browser_manager.page.content()
                for expected_text in validation["expected_text"]:
                    text_found = expected_text.lower() in page_content.lower()
                    text_validation_results[expected_text] = text_found
                    print(f"    텍스트 '{expected_text}': {'✅' if text_found else '❌'}")
                
                # 페이지 로딩 상태 확인
                try:
                    # 페이지가 완전히 로드될 때까지 대기
                    await browser_manager.page.wait_for_load_state("networkidle", timeout=10000)
                    loading_complete = True
                except:
                    loading_complete = False
                
                print(f"  페이지 로딩 완료: {'✅' if loading_complete else '❌'}")
                
                # 검증 결과 종합
                total_elements_found = sum(element_validation_results.values())
                total_texts_found = sum(text_validation_results.values())
                
                if (url_valid and total_elements_found > 0 and total_texts_found > 0 and loading_complete):
                    validation_status = "PASSED"
                    print(f"  🎉 {page_name} 페이지 검증 성공!")
                else:
                    validation_status = "FAILED"
                    print(f"  ❌ {page_name} 페이지 검증 실패")
                
                validation_results[page_name] = {
                    "status": validation_status,
                    "url_valid": url_valid,
                    "elements_found": total_elements_found,
                    "texts_found": total_texts_found,
                    "loading_complete": loading_complete,
                    "element_details": element_validation_results,
                    "text_details": text_validation_results
                }
                
                # 뒤로가기로 원래 페이지로 복원
                await browser_manager.page.go_back()
                await asyncio.sleep(3)
                
            except Exception as e:
                print(f"  ❌ {page_name} 페이지 검증 중 오류: {e}")
                validation_results[page_name] = {"status": "ERROR", "reason": str(e)}
                continue
        
        # 5. 검증 결과 요약
        print("\n" + "=" * 80)
        print("📊 톱니바퀴 설정 페이지 검증 결과 요약")
        print("=" * 80)
        
        passed_count = 0
        failed_count = 0
        error_count = 0
        
        for page_name, result in validation_results.items():
            status_icon = "✅" if result["status"] == "PASSED" else "❌" if result["status"] == "FAILED" else "💥"
            print(f"{status_icon} {page_name}: {result['status']}")
            
            if result["status"] == "PASSED":
                passed_count += 1
            elif result["status"] == "FAILED":
                failed_count += 1
            else:
                error_count += 1
        
        print(f"\n📈 검증 결과 통계:")
        print(f"  ✅ 성공: {passed_count}개")
        print(f"  ❌ 실패: {failed_count}개")
        print(f"  💥 오류: {error_count}개")
        print(f"  📊 총 페이지: {len(validation_results)}개")
        
        # 6. 최종 스크린샷
        print("\n📸 최종 스크린샷 저장...")
        await browser_manager.page.screenshot(path="reports/dev/screenshots/page_validation_final.png")
        
        # 7. 상세 결과를 파일로 저장
        import json
        results_file = "reports/dev/page_validation_results.json"
        with open(results_file, "w", encoding="utf-8") as f:
            json.dump(validation_results, f, ensure_ascii=False, indent=2)
        
        print(f"📄 상세 결과 저장: {results_file}")
        
        success_rate = (passed_count / len(validation_results)) * 100 if validation_results else 0
        print(f"🎯 성공률: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("\n🎉 대부분의 페이지가 정상적으로 작동합니다!")
        elif success_rate >= 60:
            print("\n⚠️ 일부 페이지에 문제가 있을 수 있습니다.")
        else:
            print("\n❌ 많은 페이지에 문제가 있습니다.")
        
        return success_rate >= 60

async def main():
    """메인 실행 함수"""
    try:
        result = await test_gear_settings_page_validation("dev")
        if result:
            print("\n🎉 페이지 검증 테스트 성공!")
        else:
            print("\n❌ 페이지 검증 테스트 실패")
    except Exception as e:
        print(f"\n💥 테스트 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
