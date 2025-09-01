#!/usr/bin/env python3
"""
모든 테스트 파일에 타임아웃 데코레이터를 자동으로 추가하는 스크립트
"""

import os
import re
from pathlib import Path

# 타임아웃 설정 (테스트 유형별) - 절반 수준으로 단축
TIMEOUT_SETTINGS = {
    'login': 30,        # 로그인 테스트: 30초
    'dashboard': 45,    # 대시보드 테스트: 45초
    'add_plan': 45,     # Add Plan 테스트: 45초
    'survey': 60,       # Survey 테스트: 1분
    'navigation': 22,   # 네비게이션 테스트: 22초
    'search': 30,       # 검색 테스트: 30초
    'site': 37,         # 사이트 관련 테스트: 37초
    'gallery': 30,      # 갤러리 테스트: 30초
    'default': 45       # 기본: 45초
}

def get_timeout_for_test(filename, function_name):
    """테스트 파일명과 함수명을 기반으로 적절한 타임아웃 결정"""
    filename_lower = filename.lower()
    function_lower = function_name.lower()
    
    if 'login' in filename_lower or 'login' in function_lower:
        return TIMEOUT_SETTINGS['login']
    elif 'dashboard' in filename_lower or 'dashboard' in function_lower:
        return TIMEOUT_SETTINGS['dashboard']
    elif 'add_plan' in filename_lower or 'add_plan' in function_lower:
        return TIMEOUT_SETTINGS['add_plan']
    elif 'survey' in filename_lower or 'survey' in function_lower:
        return TIMEOUT_SETTINGS['survey']
    elif 'navigation' in filename_lower or 'navigation' in function_lower:
        return TIMEOUT_SETTINGS['navigation']
    elif 'search' in filename_lower or 'search' in function_lower:
        return TIMEOUT_SETTINGS['search']
    elif 'site' in filename_lower or 'site' in function_lower:
        return TIMEOUT_SETTINGS['site']
    elif 'gallery' in filename_lower or 'gallery' in function_lower:
        return TIMEOUT_SETTINGS['gallery']
    else:
        return TIMEOUT_SETTINGS['default']

def add_timeout_decorator(file_path):
    """파일에 타임아웃 데코레이터 추가"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 이미 타임아웃 데코레이터가 있는지 확인
    if '@timeout(' in content:
        print(f"⚠️ {file_path} - 이미 타임아웃 데코레이터가 있습니다.")
        return False
    
    # timeout 함수가 이미 정의되어 있는지 확인
    if 'def timeout(seconds):' in content:
        print(f"⚠️ {file_path} - 이미 timeout 함수가 정의되어 있습니다.")
        timeout_function_exists = True
    else:
        timeout_function_exists = False
    
    modified = False
    
    # 1. import 섹션에 필요한 import 추가
    if not timeout_function_exists:
        if 'from functools import wraps' not in content:
            # functools import 추가
            import_pattern = r'(import asyncio.*?\n)'
            if re.search(import_pattern, content):
                content = re.sub(
                    import_pattern,
                    r'\1from functools import wraps\n',
                    content
                )
                modified = True
        
        # 2. timeout 함수 정의 추가
        timeout_function = '''
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

'''
        
        # 클래스나 함수 정의 직전에 timeout 함수 추가
        class_or_function_pattern = r'(@pytest\.mark\.|class |async def test_)'
        match = re.search(class_or_function_pattern, content)
        if match:
            insert_pos = match.start()
            content = content[:insert_pos] + timeout_function + content[insert_pos:]
            modified = True
    
    # 3. 테스트 함수에 @timeout 데코레이터 추가
    filename = os.path.basename(file_path)
    
    # async def test_로 시작하는 함수 찾기
    test_function_pattern = r'(@pytest\.mark\..*?\n)*(\s*)(async def test_\w+)'
    
    def add_timeout_to_function(match):
        decorators = match.group(1) if match.group(1) else ''
        indent = match.group(2)
        function_def = match.group(3)
        
        # 함수명에서 타임아웃 결정
        function_name = re.search(r'async def (test_\w+)', function_def).group(1)
        timeout_value = get_timeout_for_test(filename, function_name)
        
        timeout_decorator = f'{indent}@timeout({timeout_value})  # {timeout_value//60}분 {timeout_value%60}초 타임아웃\n'
        
        return decorators + timeout_decorator + indent + function_def
    
    new_content = re.sub(test_function_pattern, add_timeout_to_function, content)
    
    if new_content != content:
        modified = True
        content = new_content
    
    # 파일 저장
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {file_path} - 타임아웃 데코레이터 추가 완료")
        return True
    else:
        print(f"📝 {file_path} - 변경 사항 없음")
        return False

def main():
    """메인 실행 함수"""
    print("🔧 모든 테스트 파일에 타임아웃 데코레이터 추가 중...")
    
    # 테스트 디렉토리 찾기
    test_dirs = ['tests/smoke', 'tests/regression', 'tests/integration']
    
    modified_files = []
    
    for test_dir in test_dirs:
        if os.path.exists(test_dir):
            print(f"\n📁 {test_dir} 디렉토리 처리 중...")
            
            for file_path in Path(test_dir).glob('test_*.py'):
                if add_timeout_decorator(file_path):
                    modified_files.append(str(file_path))
    
    print(f"\n🎉 완료! {len(modified_files)}개 파일이 수정되었습니다.")
    
    if modified_files:
        print("\n📝 수정된 파일 목록:")
        for file_path in modified_files:
            print(f"  - {file_path}")
    
    print(f"\n⏰ 타임아웃 설정:")
    for test_type, timeout_val in TIMEOUT_SETTINGS.items():
        print(f"  - {test_type}: {timeout_val}초 ({timeout_val//60}분 {timeout_val%60}초)")

if __name__ == "__main__":
    main()
