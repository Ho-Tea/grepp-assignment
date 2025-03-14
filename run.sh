#!/bin/bash
# run.sh: 전체 환경 설정 및 FastAPI 애플리케이션 실행 스크립트

# 가상환경 활성화 (가상환경 이름이 .venv인 경우)
source .venv/bin/activate

# 의존성 설치 (이미 설치되어 있다면 건너뛰어도 됩니다)
pip install -r requirements.txt

# Uvicorn을 사용하여 FastAPI 앱 실행 (코드 변경 시 자동 재시작)
uvicorn app.main:app --reload
