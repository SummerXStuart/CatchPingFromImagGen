# CatchPingFromImageGen
Catch mind from generated image hint


## Single Mode

### 사전 작업

미리 싱글모드용 문제 생성

### 게임

1. 랜덤하게 3개 target words 선택
2. 각 target word에 대한 힌트 이미지 제공
3. 첫번째 힌트 이미지에서 맞추면 3점, 두번째 이미지에서 맞추면 2점, 세번째 이미지에 맞추면 1점, 못 맞추면 0점
4. 3문제를 내고 점수 합산

### 게임 서버 실행

```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate

# 가상환경 최신화
pip install --upgrade pip

# 필요 라이브러리 설치
pip install -r requirements.txt

# 게임서버 실행
python game_server.py
```

### tutorial

simulation.ipynb


