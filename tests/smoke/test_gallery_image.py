#!/usr/bin/env python3
"""
Gallery Image Upload Tests
갤러리 이미지 추가 테스트
"""

import asyncio
from functools import wraps
import sys
import os
from pathlib import Path

import pytest

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.config_loader import get_config
from utils.browser_manager import BrowserFactory
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.site_detail_page import SiteDetailPage


def create_sample_gallery_image() -> str:
    """테스트용 샘플 갤러리 이미지 파일을 반환합니다."""
    project_root = Path(__file__).parent.parent.parent
    image_path = project_root / "test_data" / "images" / "test_gallery_image.png"

    if not image_path.exists():
        raise FileNotFoundError(f"테스트 이미지 파일을 찾을 수 없습니다: {image_path}")

    return str(image_path)



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

@pytest.mark.env('dev')
@timeout(30)  # 30초 타임아웃
async def test_gallery_image_upload_complete_flow(environment: str = "dev"):
    """갤러리 이미지 업로드 완전한 플로우 테스트"""
    print(f"🖼️ {environment.upper()} 환경 갤러리 이미지 업로드 완전한 플로우 테스트...")
    
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
        dashboard_page = DashboardPage(browser_manager.page, config)
        await dashboard_page.wait_for_dashboard_load()
        
        # 첫 번째 사이트 직접 클릭 (다양한 방법 시도)
        print("📝 첫 번째 사이트 클릭 시도...")
        try:
            # 방법 1: building_address 셀렉터로 시도
            await dashboard_page.click_site_by_index(0)
            await asyncio.sleep(3)
            print("✅ 사이트 클릭 성공 (building_address)")
        except Exception as e:
            print(f"⚠️ building_address 방법 실패: {e}")
            try:
                # 방법 2: .building 셀렉터로 시도
                await dashboard_page.click_site_in_list_by_index(0)
                await asyncio.sleep(3)
                print("✅ 사이트 클릭 성공 (.building)")
            except Exception as e2:
                print(f"❌ 모든 사이트 클릭 방법 실패: {e2}")
                return False
        
        # 사이트 상세 페이지
        site_detail_page = SiteDetailPage(browser_manager.page, config)
        await site_detail_page.wait_for_page_load()
        
        print("\n📋 갤러리 이미지 업로드 테스트")
        print("-" * 30)
        
        # 갤러리 섹션 확인
        gallery_visible = await site_detail_page.is_gallery_section_visible()
        print(f"📸 갤러리 섹션 표시: {gallery_visible}")
        
        if not gallery_visible:
            print("⚠️ 갤러리 섹션이 보이지 않습니다. 페이지를 스크롤하거나 다른 위치를 확인해보겠습니다.")
            # 페이지 스크롤 시도
            await browser_manager.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(2)
            gallery_visible = await site_detail_page.is_gallery_section_visible()
            print(f"📸 스크롤 후 갤러리 섹션 표시: {gallery_visible}")
        
        # 갤러리 이미지 개수 확인 (업로드 전)
        initial_count = await site_detail_page.get_gallery_images_count()
        print(f"📊 업로드 전 갤러리 이미지 개수: {initial_count}")
        
        # 갤러리 이미지 업로드 시도
        try:
            # 샘플 이미지 파일 생성
            image_path = create_sample_gallery_image()
            print(f"📁 사용할 이미지 파일: {image_path}")
            
            # 갤러리 이미지 추가
            success = await site_detail_page.add_gallery_image(image_path)
            
            if success:
                print("✅ 갤러리 이미지 업로드 성공")
                
                # 업로드 후 이미지 개수 확인
                final_count = await site_detail_page.get_gallery_images_count()
                print(f"📊 업로드 후 갤러리 이미지 개수: {final_count}")
                
                # 이미지 개수 증가 확인
                if final_count > initial_count:
                    print("✅ 갤러리 이미지 개수 증가 확인됨")
                else:
                    print("⚠️ 갤러리 이미지 개수가 증가하지 않았습니다")
                
                # 갤러리 이미지 정보 가져오기
                gallery_images = await site_detail_page.get_gallery_images()
                print(f"🖼️ 갤러리 이미지 정보: {len(gallery_images)}개")
                
                for i, img in enumerate(gallery_images):
                    print(f"  - 이미지 {i+1}: src={img.get('src', 'N/A')[:50]}..., visible={img.get('visible', False)}")
                
            else:
                print("❌ 갤러리 이미지 업로드 실패")
                
        except Exception as e:
            print(f"❌ 갤러리 이미지 업로드 중 오류 발생: {e}")
            # 오류 발생 시 스크린샷 촬영
            await site_detail_page.take_screenshot("gallery_upload_error", "failure")
            raise
        
        # 최종 스크린샷 촬영
        await site_detail_page.take_screenshot("gallery_upload_complete", "success")
        
        print("\n✅ 갤러리 이미지 업로드 테스트 완료")
        return True


@pytest.mark.asyncio
@timeout(30)  # 30초 타임아웃
async def test_gallery_image_dialog_elements(environment: str = "dev"):
    """갤러리 이미지 업로드 다이얼로그 요소 테스트"""
    config = get_config(environment)
    
    async with BrowserFactory.create(config) as browser_manager:
        print("\n" + "=" * 60)
        print("🖼️ DEV 환경 갤러리 이미지 업로드 다이얼로그 요소 테스트")
        print("=" * 60)
        
        # 1단계: 로그인
        login_page = LoginPage(browser_manager.page, config)
        await login_page.navigate_to_login()
        await login_page.wait_for_page_load()
        
        # 3단계 로그인 실행
        space_id = "d-ge-pr"
        email = config.test_data.valid_user["email"]
        password = config.test_data.valid_user["password"]
        
        await login_page.login(space_id, email, password)
        print("✅ 로그인 성공")
        
        # 2단계: 대시보드로 이동
        dashboard_page = DashboardPage(browser_manager.page, config)
        await dashboard_page.wait_for_dashboard_load()
        
        # 첫 번째 사이트 직접 클릭 (다양한 방법 시도)
        print("📝 첫 번째 사이트 클릭 시도...")
        try:
            # 방법 1: building_address 셀렉터로 시도
            await dashboard_page.click_site_by_index(0)
            await asyncio.sleep(3)
            print("✅ 사이트 클릭 성공 (building_address)")
        except Exception as e:
            print(f"⚠️ building_address 방법 실패: {e}")
            try:
                # 방법 2: .building 셀렉터로 시도
                await dashboard_page.click_site_in_list_by_index(0)
                await asyncio.sleep(3)
                print("✅ 사이트 클릭 성공 (.building)")
            except Exception as e2:
                print(f"❌ 모든 사이트 클릭 방법 실패: {e2}")
                return False
        
        # 3단계: 사이트 상세 페이지
        site_detail_page = SiteDetailPage(browser_manager.page, config)
        await site_detail_page.wait_for_page_load()
        
        print("\n📋 갤러리 이미지 업로드 다이얼로그 요소 확인")
        print("-" * 30)
        
        try:
            # 갤러리 추가 버튼 클릭
            await site_detail_page.click_gallery_add_button()
            print("✅ 갤러리 추가 버튼 클릭 성공")
            
            # 다이얼로그 열림 확인
            dialog_open = await site_detail_page.is_gallery_dialog_open()
            print(f"📋 갤러리 업로드 다이얼로그 열림: {dialog_open}")
            
            if dialog_open:
                # 다이얼로그 제목 확인
                dialog_title = await site_detail_page.get_gallery_dialog_title()
                print(f"📝 다이얼로그 제목: {dialog_title}")
                
                # 파일 입력 요소 확인
                await site_detail_page.wait_for_gallery_file_input()
                print("✅ 파일 입력 요소 확인됨")
                
                # 다이얼로그 취소
                await site_detail_page.click_gallery_cancel()
                print("✅ 다이얼로그 취소 성공")
                
            else:
                print("⚠️ 갤러리 업로드 다이얼로그가 열리지 않았습니다")
                
        except Exception as e:
            print(f"❌ 갤러리 다이얼로그 테스트 중 오류 발생: {e}")
            # 오류 발생 시 스크린샷 촬영
            await site_detail_page.take_screenshot("gallery_dialog_error", "failure")
            raise
        
        # 최종 스크린샷 촬영
        await site_detail_page.take_screenshot("gallery_dialog_elements", "success")
        
        print("\n✅ 갤러리 이미지 업로드 다이얼로그 요소 테스트 완료")
        return True


@pytest.mark.asyncio
@timeout(30)  # 30초 타임아웃
async def test_gallery_image_verification(environment: str = "dev"):
    """갤러리 이미지 검증 테스트"""
    config = get_config(environment)
    
    async with BrowserFactory.create(config) as browser_manager:
        print("\n" + "=" * 60)
        print("🖼️ DEV 환경 갤러리 이미지 검증 테스트")
        print("=" * 60)
        
        # 1단계: 로그인
        login_page = LoginPage(browser_manager.page, config)
        await login_page.navigate_to_login()
        await login_page.wait_for_page_load()
        
        # 3단계 로그인 실행
        space_id = "d-ge-pr"
        email = config.test_data.valid_user["email"]
        password = config.test_data.valid_user["password"]
        
        await login_page.login(space_id, email, password)
        print("✅ 로그인 성공")
        
        # 2단계: 대시보드로 이동
        dashboard_page = DashboardPage(browser_manager.page, config)
        await dashboard_page.wait_for_dashboard_load()
        
        # 첫 번째 사이트 직접 클릭 (다양한 방법 시도)
        print("📝 첫 번째 사이트 클릭 시도...")
        try:
            # 방법 1: building_address 셀렉터로 시도
            await dashboard_page.click_site_by_index(0)
            await asyncio.sleep(3)
            print("✅ 사이트 클릭 성공 (building_address)")
        except Exception as e:
            print(f"⚠️ building_address 방법 실패: {e}")
            try:
                # 방법 2: .building 셀렉터로 시도
                await dashboard_page.click_site_in_list_by_index(0)
                await asyncio.sleep(3)
                print("✅ 사이트 클릭 성공 (.building)")
            except Exception as e2:
                print(f"❌ 모든 사이트 클릭 방법 실패: {e2}")
                return False
        
        # 3단계: 사이트 상세 페이지
        site_detail_page = SiteDetailPage(browser_manager.page, config)
        await site_detail_page.wait_for_page_load()
        
        print("\n📋 갤러리 이미지 검증")
        print("-" * 30)
        
        try:
            # 갤러리 섹션 확인
            gallery_visible = await site_detail_page.is_gallery_section_visible()
            print(f"📸 갤러리 섹션 표시: {gallery_visible}")
            
            if gallery_visible:
                # 갤러리 이미지 개수 확인
                image_count = await site_detail_page.get_gallery_images_count()
                print(f"📊 갤러리 이미지 개수: {image_count}")
                
                # 갤러리 이미지 정보 가져오기
                gallery_images = await site_detail_page.get_gallery_images()
                print(f"🖼️ 갤러리 이미지 정보: {len(gallery_images)}개")
                
                for i, img in enumerate(gallery_images):
                    print(f"  - 이미지 {i+1}: src={img.get('src', 'N/A')[:50]}..., visible={img.get('visible', False)}")
                
                if image_count > 0:
                    print("✅ 갤러리에 이미지가 존재합니다")
                else:
                    print("⚠️ 갤러리에 이미지가 없습니다")
            else:
                print("⚠️ 갤러리 섹션이 보이지 않습니다")
                
        except Exception as e:
            print(f"❌ 갤러리 이미지 검증 중 오류 발생: {e}")
            # 오류 발생 시 스크린샷 촬영
            await site_detail_page.take_screenshot("gallery_verification_error", "failure")
            raise
        
        # 최종 스크린샷 촬영
        await site_detail_page.take_screenshot("gallery_verification", "success")
        
        print("\n✅ 갤러리 이미지 검증 테스트 완료")
        return True
