import json
from pathlib import Path
from filelock import FileLock

# def add(id, data):
    # with open("app/database/textDB.json", "r"):



# 파일 경로 설정
DB_FILE = Path("app/database/textDB.json")
LOCK_FILE = Path("app/database/textDB.lock")

# 유저 데이터 읽기
def read_user_data(user_id):
    lock = FileLock(LOCK_FILE)
    with lock:
        if DB_FILE.exists():
            with open(DB_FILE, "r") as f:
                data = json.load(f)
            return data.get(user_id, None)
        return None

# 유저 데이터 저장/업데이트
def write_user_data(user_id, user_data):
    lock = FileLock(LOCK_FILE)
    with lock:
        if DB_FILE.exists():
            with open(DB_FILE, "r") as f:
                data = json.load(f)
        else:
            data = {}

        # 유저 데이터 업데이트
        data[user_id] = user_data

        # JSON 파일에 저장
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)