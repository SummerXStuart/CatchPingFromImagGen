from fastapi import FastAPI  # FastAPI import
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uvicorn
from pydantic import BaseModel
import random
from app.database.crud import (
    read_user_data,
    write_user_data
)
from typing import Optional

app = FastAPI()

origins = [
	"*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Input(BaseModel):
    uid: str
    estimation: Optional[str]

df = pd.read_csv("app/resources/single_mode_dummy_set.csv", encoding="utf-8")

@app.post("/catchping_backend/single_mode_quiz")
def single_mode(msg: Input):

    # uid 기준 status 가져오기
    _status = read_user_data(msg.uid)

    # _status 
    if _status:
        pass

    else:
        # 처음 요청
        # 문제 뽑기
        _targets = random.choices(df["target"].unique(), k=3)

        # 첫번째 문제의 b64 image
        _b64_img = df[df["target"]==_targets[0]].iloc[0, 3]

        _data = {
            "uid": msg.uid,
            "targets": _targets,
            "current_target_index": 0,
            "current_hint_img_index": 0,
            "trial": 0,
            "score": 0
        }

        write_user_data(msg.uid, _data)
                
        output = {
            
            "hint_b64_img": _b64_img
            
        }

    # output = {
    #     "target_word": df.iloc[0,0],
    #     "hints_b64_imgs": [
    #         df.iloc[0,3],
    #         df.iloc[1,3],
    #         df.iloc[2,3]
    #     ]
    # }
     
    
    # for p in output:
    #     print(p["target_word"])
    return output

if __name__=="__main__":
	
    uvicorn.run(
        app="dummy:app",
        host="0.0.0.0",
        port=5001,
        reload=False,
        workers=1
    )
