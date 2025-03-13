# grepp-assignment

```
app/
│
├── config/
│   └── database.py              # 데이터베이스 설정
│
├── controllers/
│   └── reservation_controller.py  # 예약 관련 API 엔드포인트
│
├── services/
│   └── reservation_service.py    # 예약 비즈니스 로직
│
├── repositories/
│   └── models.py                # DB 모델 정의 (SQLAlchemy 모델)
│
├── dtos/
│   └── schemas.py               # 데이터 전송 객체 (Pydantic 모델)
│
└── main.py                      # FastAPI 애플리케이션 진입점
```
