#!/usr/bin/env python3
"""
Run all tests in sequence
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from tests.smoke.test_dashboard import test_dashboard_functions
from tests.smoke.test_site_creation import test_create_site_final
from tests.smoke.test_site_detail import test_site_detail_pom_simple
from tests.smoke.test_global_navigation import test_global_navigation
from tests.smoke.test_search_and_site_selection import test_search_and_site_selection


async def run_all_tests():
    """Run all tests in sequence"""
    print("🚀 전체 테스트 실행 시작")
    print("=" * 80)
    print(f"📅 실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    test_results = []
    
    # 테스트 목록
    tests = [
        ("대시보드 테스트", test_dashboard_functions),
        ("사이트 생성 테스트", test_create_site_final),
        ("사이트 상세 페이지 테스트", test_site_detail_pom_simple),
        ("글로벌 네비게이션 테스트", test_global_navigation),
        ("검색 및 사이트 선택 테스트", test_search_and_site_selection),
    ]
    
    total_tests = len(tests)
    passed_tests = 0
    failed_tests = 0
    
    for i, (test_name, test_func) in enumerate(tests, 1):
        print(f"\n📋 테스트 {i}/{total_tests}: {test_name}")
        print("-" * 60)
        
        try:
            start_time = datetime.now()
            success = await test_func("dev")
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            if success:
                print(f"✅ {test_name} 성공 (소요시간: {duration:.2f}초)")
                passed_tests += 1
                test_results.append((test_name, "PASS", duration))
            else:
                print(f"❌ {test_name} 실패 (소요시간: {duration:.2f}초)")
                failed_tests += 1
                test_results.append((test_name, "FAIL", duration))
                
        except Exception as e:
            print(f"❌ {test_name} 오류 발생: {e}")
            failed_tests += 1
            test_results.append((test_name, "ERROR", 0))
    
    # 결과 요약
    print("\n" + "=" * 80)
    print("📊 테스트 결과 요약")
    print("=" * 80)
    
    for test_name, status, duration in test_results:
        status_icon = "✅" if status == "PASS" else "❌"
        print(f"{status_icon} {test_name}: {status} ({duration:.2f}초)")
    
    print(f"\n📈 전체 결과:")
    print(f"   총 테스트: {total_tests}개")
    print(f"   성공: {passed_tests}개")
    print(f"   실패: {failed_tests}개")
    print(f"   성공률: {(passed_tests/total_tests)*100:.1f}%")
    
    if failed_tests == 0:
        print("\n🎉 모든 테스트가 성공했습니다!")
    else:
        print(f"\n⚠️ {failed_tests}개의 테스트가 실패했습니다.")
    
    print("\n" + "=" * 80)
    print("✅ 전체 테스트 실행 완료")
    print("=" * 80)
    
    return failed_tests == 0


async def main():
    """메인 실행 함수"""
    try:
        success = await run_all_tests()
        if success:
            print("🎉 전체 테스트 성공!")
            sys.exit(0)
        else:
            print("❌ 일부 테스트 실패")
            sys.exit(1)
    except Exception as e:
        print(f"❌ 테스트 실행 중 오류 발생: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
