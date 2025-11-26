## 📝 Flask Memo API

Flask로 구현한 간단한 메모 CRUD REST API입니다.  
POST / GET / PUT / DELETE 각각 2개씩 (총 8개)의 엔드포인트와  
요청·응답 로깅 미들웨어, 표준화된 응답 포맷을 제공합니다.

---

## 📂 프로젝트 구조

project/
├─ app.py # Flask 앱, 라우팅, 미들웨어, 에러 핸들러
├─ memo_service.py # 메모 CRUD 비즈니스 로직 (인메모리 저장)
└─ requirements.txt # 의존성 목록


---

## 🚀 실행 방법

### 1. 가상환경 활성화 (PowerShell)

cd C:\Users...\Flask_api
& "..venv\Scripts\Activate.ps1"

프롬프트에 `(.venv)` 표시가 보이면 성공입니다.

### 2. 패키지 설치

pip install -r requirements.txt


### 3. 서버 실행

python app.py

실행 후 브라우저 또는 API 클라이언트에서 아래 주소를 사용합니다.

- 기본 주소: `http://127.0.0.1:5000`

---

## 🧩 주요 기능 개요

- 메모 생성 / 조회 / 수정 / 삭제 (인메모리 딕셔너리 사용)
- HTTP 메소드별 2개씩 API 구현  
  - POST 2개, GET 2개, PUT 2개, DELETE 2개
- 요청/응답 로깅 미들웨어  
  - 요청 전: 메서드, 경로, JSON 바디 출력  
  - 응답 후: 상태 코드, 경로 출력
- 표준화된 JSON 응답 형식 사용

응답 예시:

{
"status": "success",
"data": { ... }
}

undefined

{
"status": "error",
"message": "에러 설명"
}

