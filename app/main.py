from fastapi import FastAPI, Query
from typing import List
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

DB_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'port': int(os.getenv("DB_PORT", 5432)),
    'database': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD")
}

@app.get("/vanning/check")
def check_vanning(vins: List[str] = Query(...)):
    # 空白やNoneを取り除いたクリーンなVINタプルを生成
    vin_tuple = tuple(v.strip() for v in vins if v and v.strip())

    if not vin_tuple:
        return {"error": "VINが指定されていません。"}

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # デバッグ：実際のVINと数を返す
        debug_info = {
            "cleaned_vins": vin_tuple,
            "vin_count": len(vin_tuple)
        }

        sql = """
        SELECT "JOB No."
        FROM "TEST_202504"
        WHERE "車台番号" IN %s
        GROUP BY "JOB No."
        HAVING COUNT(DISTINCT "車台番号") = %s;
        """
        cur.execute(sql, (vin_tuple, len(vin_tuple)))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        job_nos = [row[0] for row in rows]

        debug_info["matched_jobs"] = job_nos
        return debug_info  # ← 今だけデバッグ情報をすべて返す

    except Exception as e:
        return {"error": str(e)}
