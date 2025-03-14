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
- [x] 고객은 본인이 등록한 예약만 조회할 수 있다.
- [x] 어드민은 모든 고객의 예약을 조회할 수 있다.

### 예약 수정 및 확정

- [x] 어드민은 모든 고객의 예약을 확정할 수 있다.
- [x] 고객은 예약 확정 전에 예약을 수정할 수 있다.
- [x] 어드민은 모든 고객의 예약을 수정할 수 있다.

### 예약 삭제

- [x] 고객은 확정 전에 예약을 삭제할 수 있다.
- [x] 어드민은 모든 고객의 예약을 삭제할 수 있다.

## 테스트 데이터 요약

### 1. 예약 시간 (ReservationTime)

| 예약 시간       | 예약 인원 |
|----------------|----------|
| **예약 시간 1** | 45,000명  |
| **예약 시간 2** | 100명     |
| **예약 시간 3** | 3,000명   |
| **예약 시간 4** | 50,000명  |
| **예약 시간 5** | 0명       |

### 2. 회원 (Member)

| 이름           | 역할        |
|----------------|------------|
| **Admin User** | **ADMIN**  |
| **Customer 1** | **CUSTOMER**|
| **Customer 2** | **CUSTOMER**|
| **Customer 3** | **CUSTOMER**|
| **Customer 4** | **CUSTOMER**|

### 3. 예약 (Reservation)

#### Customer 1
- **예약 시간 1**: 40,000명 예약, 상태: **CONFIRMED** (확정)
- **예약 시간 2**: 100명 예약, 상태: **CONFIRMED** (확정)

#### Customer 2
- **예약 시간 4**: 50,000명 예약, 상태: **CONFIRMED** (확정)

#### Customer 3
- **예약 시간 3**: 3,000명 예약, 상태: **CONFIRMED** (확정)
- **예약 시간 1**: 5,000명 예약, 상태: **CONFIRMED** (확정)
- **예약 시간 3**: 25,000명 예약, 상태: **PENDING** (대기)

#### Customer 4
- **예약 없음**: 아무 예약도 하지 않음

---

이 데이터는 서버가 시작될 때 자동으로 삽입됩니다.
