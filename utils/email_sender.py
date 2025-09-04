#!/usr/bin/env python3
"""
Email sender utility for test reports
"""

import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import List, Optional, Dict, Any
import json
import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)


class EmailSender:
    """이메일 전송을 담당하는 클래스"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        EmailSender 초기화
        
        Args:
            config: 이메일 설정 정보
        """
        self.smtp_server = config.get("smtp_server", "smtp.gmail.com")
        self.smtp_port = config.get("smtp_port", 587)
        self.sender_email = config.get("sender_email")
        self.sender_password = config.get("sender_password")
        self.recipient_email = config.get("recipient_email", "steve.kim@3i.ai")
        
        if not self.sender_email or not self.sender_password:
            raise ValueError("이메일 설정이 완료되지 않았습니다. config.yaml을 확인해주세요.")
    
    def create_test_report_email(self, test_results: Dict[str, Any], 
                                screenshots: List[str], 
                                videos: List[str]) -> MIMEMultipart:
        """
        테스트 결과 이메일 생성
        
        Args:
            test_results: 테스트 결과 데이터
            screenshots: 스크린샷 파일 경로 리스트
            videos: 동영상 파일 경로 리스트
            
        Returns:
            생성된 이메일 객체
        """
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.recipient_email
        msg['Subject'] = f"🧪 Beamo 자동화 테스트 결과 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # 이메일 본문 생성
        body = self._generate_email_body(test_results, screenshots, videos)
        msg.attach(MIMEText(body, 'html', 'utf-8'))
        
        # 첨부파일 추가
        self._attach_files(msg, screenshots, videos)
        
        return msg
    
    def _generate_email_body(self, test_results: Dict[str, Any], 
                            screenshots: List[str], 
                            videos: List[str]) -> str:
        """
        이메일 본문 HTML 생성
        
        Args:
            test_results: 테스트 결과 데이터
            screenshots: 스크린샷 파일 리스트
            videos: 동영상 파일 리스트
            
        Returns:
            HTML 형식의 이메일 본문
        """
        total_tests = test_results.get("total_tests", 0)
        passed_tests = test_results.get("passed_tests", 0)
        failed_tests = test_results.get("failed_tests", 0)
        skipped_tests = test_results.get("skipped_tests", 0)
        execution_time = test_results.get("execution_time", "0s")
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 8px; }}
                .summary {{ margin: 20px 0; }}
                .stats {{ display: flex; gap: 20px; margin: 20px 0; }}
                .stat-box {{ 
                    background-color: #ffffff; 
                    border: 1px solid #dee2e6; 
                    border-radius: 6px; 
                    padding: 15px; 
                    text-align: center; 
                    flex: 1;
                }}
                .passed {{ color: #28a745; font-weight: bold; }}
                .failed {{ color: #dc3545; font-weight: bold; }}
                .skipped {{ color: #ffc107; font-weight: bold; }}
                .attachments {{ margin: 20px 0; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #dee2e6; color: #6c757d; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🧪 Beamo 자동화 테스트 결과</h1>
                <p><strong>실행 시간:</strong> {datetime.now().strftime('%Y년 %m월 %d일 %H시 %M분')}</p>
                <p><strong>실행 환경:</strong> {test_results.get('environment', 'dev')}</p>
            </div>
            
            <div class="summary">
                <h2>📊 테스트 요약</h2>
                <div class="stats">
                    <div class="stat-box">
                        <h3>전체 테스트</h3>
                        <p style="font-size: 24px; font-weight: bold;">{total_tests}</p>
                    </div>
                    <div class="stat-box">
                        <h3 class="passed">성공</h3>
                        <p style="font-size: 24px; font-weight: bold; color: #28a745;">{passed_tests}</p>
                    </div>
                    <div class="stat-box">
                        <h3 class="failed">실패</h3>
                        <p style="font-size: 24px; font-weight: bold; color: #dc3545;">{failed_tests}</p>
                    </div>
                    <div class="stat-box">
                        <h3 class="skipped">건너뜀</h3>
                        <p style="font-size: 24px; font-weight: bold; color: #ffc107;">{skipped_tests}</p>
                    </div>
                </div>
                
                <div style="text-align: center; margin: 20px 0;">
                    <h3>성공률</h3>
                    <p style="font-size: 32px; font-weight: bold; color: #28a745;">{success_rate:.1f}%</p>
                </div>
                
                <p><strong>총 실행 시간:</strong> {execution_time}</p>
            </div>
            
            <div class="attachments">
                <h2>📎 첨부 파일</h2>
                <p><strong>스크린샷:</strong> {len(screenshots)}개</p>
                <p><strong>동영상:</strong> {len(videos)}개</p>
            </div>
            
            <div class="footer">
                <p>이 이메일은 Beamo 자동화 테스트 시스템에서 자동으로 생성되었습니다.</p>
                <p>문의사항이 있으시면 개발팀에 연락해주세요.</p>
            </div>
        </body>
        </html>
        """
        
        return html_body
    
    def _attach_files(self, msg: MIMEMultipart, screenshots: List[str], videos: List[str]):
        """
        이메일에 파일 첨부
        
        Args:
            msg: 이메일 객체
            screenshots: 스크린샷 파일 경로 리스트
            videos: 동영상 파일 경로 리스트
        """
        # 스크린샷 첨부
        for screenshot in screenshots:
            if Path(screenshot).exists():
                try:
                    with open(screenshot, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                    
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {Path(screenshot).name}'
                    )
                    msg.attach(part)
                    logger.info(f"스크린샷 첨부 완료: {screenshot}")
                except Exception as e:
                    logger.error(f"스크린샷 첨부 실패: {screenshot}, 오류: {e}")
        
        # 동영상 첨부 (파일 크기가 클 수 있으므로 선택적)
        for video in videos[:5]:  # 최대 5개만 첨부
            if Path(video).exists():
                try:
                    file_size = Path(video).stat().st_size
                    if file_size > 25 * 1024 * 1024:  # 25MB 이상이면 건너뛰기
                        logger.warning(f"동영상 파일이 너무 큽니다 (25MB 초과): {video}")
                        continue
                        
                    with open(video, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                    
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {Path(video).name}'
                    )
                    msg.attach(part)
                    logger.info(f"동영상 첨부 완료: {video}")
                except Exception as e:
                    logger.error(f"동영상 첨부 실패: {video}, 오류: {e}")
    
    def send_email(self, msg: MIMEMultipart) -> bool:
        """
        이메일 전송
        
        Args:
            msg: 전송할 이메일 객체
            
        Returns:
            전송 성공 여부
        """
        try:
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                
                text = msg.as_string()
                server.sendmail(self.sender_email, self.recipient_email, text)
                
                logger.info(f"이메일 전송 성공: {self.recipient_email}")
                return True
                
        except Exception as e:
            logger.error(f"이메일 전송 실패: {e}")
            return False
    
    def send_test_report(self, test_results: Dict[str, Any], 
                        screenshots: List[str], 
                        videos: List[str]) -> bool:
        """
        테스트 결과 이메일 전송 (통합 메서드)
        
        Args:
            test_results: 테스트 결과 데이터
            screenshots: 스크린샷 파일 경로 리스트
            videos: 동영상 파일 경로 리스트
            
        Returns:
            전송 성공 여부
        """
        try:
            msg = self.create_test_report_email(test_results, screenshots, videos)
            return self.send_email(msg)
        except Exception as e:
            logger.error(f"테스트 리포트 이메일 생성/전송 실패: {e}")
            return False
