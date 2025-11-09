import time
import logging
from fastapi import FastAPI, Request

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_middleware(app: FastAPI):
    """모든 미들웨어 설정"""
    
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """
        요청 로깅 미들웨어
        - 요청 메소드, URL, 클라이언트 정보 기록
        - 요청 처리 시간 측정
        - 응답 상태 코드 기록
        """
        start_time = time.time()
        
        # 요청 정보 로깅
        logger.info(f"{'='*60}")
        logger.info(f"🔵 [{request.method}] {request.url.path}")
        logger.info(f"   Query: {dict(request.query_params)}")
        logger.info(f"   Client: {request.client.host}:{request.client.port}")
        logger.info(f"   Headers: {dict(request.headers)}")
        
        try:
            # 요청 처리
            response = await call_next(request)
            
            # 응답 시간 계산
            process_time = time.time() - start_time
            
            # 응답 정보 로깅
            logger.info(f"✅ Status: {response.status_code}")
            logger.info(f"⏱️  Processing Time: {process_time:.3f}s")
            logger.info(f"{'='*60}\n")
            
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(f"❌ Error: {str(e)}")
            logger.error(f"⏱️  Processing Time: {process_time:.3f}s")
            logger.error(f"{'='*60}\n")
            raise
