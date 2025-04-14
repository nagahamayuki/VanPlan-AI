from fastapi import FastAPI, Query
from typing import List

app = FastAPI()

@app.get("/vanning/check")
def check_vanning(vins: List[str] = Query(...)):
    return {"message": "VINを受け取りました", "vins": vins}
