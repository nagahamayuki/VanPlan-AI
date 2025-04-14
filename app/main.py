from fastapi import FastAPI
from typing import List

app = FastAPI()

@app.get("/vanning/check")
def check_vanning(vins: List[str]):
    return {"message": "VINを受け取りました", "vins": vins}
