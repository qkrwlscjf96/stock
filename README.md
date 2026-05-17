# Stock Monitoring

Yahoo Finance 데이터를 수집해 주요 종목의 가격 흐름을 점검하고, 이상 징후가 감지되면 Slack으로 알림을 보내는 개인용 주식 모니터링 프로젝트입니다.

## 주요 기능

- Yahoo Finance API 기반으로 종목별 시세 데이터를 조회합니다.
- 20일, 60일 이동평균선을 이용해 추세 이상 여부를 점검합니다.
- 이상 징후가 감지되면 차트를 생성해 Slack 채널로 전송합니다.
- 이상 징후가 없으면 텍스트 메시지만 Slack으로 전송합니다.
- 실행 로그를 기준으로 하루 2회 이상 중복 실행을 방지합니다.

## 이상 징후 조건

- 데드크로스: MA20이 MA60 아래로 내려가는 경우
- 추세 이탈: 종가가 MA60 아래로 내려가는 경우
- 급락: 전일 대비 종가 하락률이 `-3%` 이하인 경우

## 프로젝트 구조

```text
stock/
├── src/
│   ├── main.py
│   └── utils/
│       ├── func_analysis.py
│       ├── func_api.py
│       └── func_common.py
├── result/
│   └── *.png
└── README.md
```

- `src`: 실행 코드와 유틸리티 모듈이 들어 있습니다.
- `result`: 이상 징후 발생 시 생성되는 차트 이미지가 저장됩니다.

## 실행 환경

- Python 3.x
- `slack-sdk`
- `yfinance`
- `python-dotenv`
- `matplotlib`

예시 설치:

```bash
pip install slack-sdk yfinance python-dotenv matplotlib
```

## 환경 변수

루트 또는 실행 가능한 위치에서 `.env` 파일을 읽을 수 있어야 합니다.

```env
SLACK_TOKEN=xoxb-...
CHANNEL_ID=C0123456789
```

- `SLACK_TOKEN`: Slack Bot User OAuth Token
- `CHANNEL_ID`: 알림을 보낼 Slack 채널 ID

## 실행 방법

프로젝트 루트에서 아래처럼 실행합니다.

```bash
python3 src/main.py
```

`main.py`는 아래 종목들을 대상으로 최근 1년 데이터를 조회합니다.

- `GOOGL`
- `MSFT`
- `AAPL`
- `QQQ`
- `^GSPC`

## 동작 방식

1. `src/main.py`가 실행됩니다.
2. `99.logs/job.log`를 확인해 당일 2회 이상 실행되었는지 검사합니다.
3. 종목별 시세 데이터를 조회합니다.
4. 이동평균 기반 이상 징후를 분석합니다.
5. 이상 징후가 있으면 차트를 `result` 폴더에 저장하고 Slack으로 이미지를 전송합니다.
6. 이상 징후가 없으면 Slack으로 텍스트만 전송합니다.

## 자동 실행

작업 스케줄러에 `src/main.py`를 등록하면 부팅 시 자동 실행하도록 구성할 수 있습니다.
