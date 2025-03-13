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
├── exceptions/
│   └── exceptions.py             # 예외 처리 정의
│
└── main.py                      # FastAPI 애플리케이션 진입점
```

### 예약 조회, 신청

- [x] 고객은 예약 가능 시간을 조회할 수 있다.
- [x] 고객은 예약을 신청할 수 있다.
- [ ] 고객은 본인이 등록한 예약만 조회할 수 있다.
- [ ] 어드민은 모든 고객의 예약을 조회할 수 있다.

### 예약 수정 및 확정

- [ ] 어드민은 모든 고객의 예약을 확정할 수 있다.
- [ ] 고객은 예약 확정 전에 예약을 수정할 수 있다.
- [ ] 어드민은 모든 고객의 예약을 수정할 수 있다.

### 예약 삭제

- [ ] 고객은 확정 전에 예약을 삭제할 수 있다.
- [ ] 어드민은 모든 고객의 예약을 삭제할 수 있다.