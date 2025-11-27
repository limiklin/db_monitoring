import json
import os
from datetime import datetime, date
from monitor.db import get_connection
from monitor.dooray_sender import send_dooray

# 기록 파일 경로
HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alert_history.json")


# --------------------------------------------------------------------
# 기록 파일 로드 및 저장
# --------------------------------------------------------------------
def load_history():
    if not os.path.exists(HISTORY_FILE):
        return {}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)


# --------------------------------------------------------------------
# 에러 고유 key 생성
# --------------------------------------------------------------------
def build_error_key(row):
    start_date = row["START_TIME"].strftime("%Y%m%d")
    # 더 정교한 방식 유지
    return f"{row['EVENT_ID']}_{start_date}_{row['SEQ']}"

# --------------------------------------------------------------------
# 오늘 이미 보낸 알림인지 확인
# --------------------------------------------------------------------
def should_send_alert(row, history):
    key = build_error_key(row)
    today = date.today().strftime("%Y-%m-%d")

    # 기록 없이 처음이면 오늘로 기록 → 보내야 함
    if key not in history:
        history[key] = {"last_alert_date": today}
        return True

    record = history[key]

    # 오늘 이미 보냈으면 X
    if record["last_alert_date"] == today:
        return False

    # 오늘은 안 보냈으면 보내고 날짜 업데이트
    record["last_alert_date"] = today
    return True


# --------------------------------------------------------------------
# SQL 로드
# --------------------------------------------------------------------
def load_query():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    query_path = os.path.join(base_dir, "query.sql")
    with open(query_path, "r", encoding="utf-8") as f:
        return f.read()


# --------------------------------------------------------------------
# 커서를 dict 로 변환
# --------------------------------------------------------------------
def dict_cursor(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor]


# --------------------------------------------------------------------
# 메시지 포맷
# --------------------------------------------------------------------
def format_row(row):
    return (
        f"[DB ERROR]\n"
        f"SEQ: {row['SEQ']}\n"
        f"EVENT_ID: {row['EVENT_ID']}\n"
        f"EVENT_NAME: {row['EVENT_NAME']}\n"
        f"DB_NAME: {row['DB_NAME']}\n"
        f"START_TIME: {row['START_TIME']}\n"
        f"END_TIME: {row['END_TIME']}\n"
        f"DIFF_HOUR: {row['DIFF_HOUR']}\n"
        f"--------------------------------------\n"
    )


# --------------------------------------------------------------------
# 메인 로직
# --------------------------------------------------------------------
def check_events_and_send_dooray():
    history = load_history()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(load_query())
    rows = dict_cursor(cursor)

    send_rows = []

    for row in rows:
        if should_send_alert(row, history):
            send_rows.append(row)

    # 기록 저장
    save_history(history)

    # 전송
    if send_rows:
        message = "".join([format_row(r) for r in send_rows])
        send_dooray(message)
        print(f"{len(send_rows)}건 알림 전송 완료")
    else:
        print("오늘은 이미 알림 전송 완료 또는 전송할 에러 없음")

    cursor.close()
    conn.close()
