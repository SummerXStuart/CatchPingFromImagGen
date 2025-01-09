from fastapi import FastAPI, HTTPException
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
    
    score_criteria = {
        1: 3,
        2: 2,
        3: 1
    }

    # _status 
    if _status:
        # 처음이 아님
        # 현재 문제가 뭔지 확인
        current_target_index = _status["current_target_index"]
        target_word = _status["targets"][current_target_index]
        # trial +=1
        trial = _status["trial"] + 1 
        
        # 정답 확인 해주기
        if not msg.estimation:
            raise HTTPException(status_code=400, 
                                detail="처음 요청이 아닐 경우 예상 정답(estimation) 같이 줘야 함."
                                )
        # 정답인지 아닌지
        result = msg.estimation == target_word
        
        score = _status["score"]
        
        if result:
            # 맞으면 trial 에 따른 score 추가
            score += score_criteria[trial]
            
            # 마지막 문제일 경우
            # end=True, score 출력
            if current_target_index == 2:
                _data = {
                    "uid": msg.uid,
                    "targets": _targets,
                    "current_target_index": current_target_index,
                    "current_hint_img_index": _status["current_hint_img_index"],
                    "trial": trial,
                    "score": score
                }

                write_user_data(msg.uid, _data)
                        
                output = {
                    "start": False,
                    "hint_b64_imgs": [],
                    "current_target_index": current_target_index,
                    "current_hint_img_index": _data["current_hint_img_index"],
                    "score": score,
                    "result": result, # 문제를 맞혔는지
                    "trial": trial, 
                    "end": True
                }
            else:
            
                
                # reset trial
                trial = 0
                
                # TODO output 정의해주기
            
            
        
        
        # 틀리면 
        # trial < 3 이면 기존 힌트 인덱스 찾아서 힌트 이미지 출력
        # 다음 힌트 달라고 하는건 별개 엔드포인트 부여
        
        
        # trial == 3 이면 다음 문제 부여
        # reset trial
        
        
        
        

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
            
            "start": True,
            "hint_b64_imgs": [_b64_img],
            "current_target_index": _data["current_target_index"], # 첫번째 의미
            "current_hint_img_index": _data["current_hint_img_index"], # 첫번째 의미
            "score": _data["score"],
            "result": False, # 문제를 맞혔는지
            "trial": _data["trial"], 
            "end": False
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
