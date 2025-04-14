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
    if not vins:
        return {"error": "VINが指定されていません。"}
    
    vin_tuple = tuple(v.strip() for v in vins if v.strip())  # 空白削除 & 空要素除外

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
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
        return {
            "input_vins": vins,
            "matched_jobs": job_nos
        }

    except Exception as e:
        return {"error": str(e)}
