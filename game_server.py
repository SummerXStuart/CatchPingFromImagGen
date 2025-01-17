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

class InitInfo(BaseModel):
    uid: str

class Input(BaseModel):
    uid: str
    estimation: str

# df = pd.read_csv("app/resources/single_mode_dummy_set.csv", encoding="utf-8")
df = pd.read_csv("app/resources/single_mode_set.csv", encoding="utf-8")

@app.post("/catchping_backend/single_mode_quiz")
async def single_mode(msg: Input):

    # uid 기준 status 가져오기
    _status = read_user_data(msg.uid)
    
    score_criteria = {
        1: 3,
        2: 2,
        3: 1
    }

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
    
    # 정답일 때와 end=True일 때, 한 문제에 대해 모든 힌트와 기회를 소진했을 때는 target을 알려주기 
    if result:
        # 맞으면 trial 에 따른 score 추가
        score += score_criteria[trial]
        
        # 마지막 문제일 경우
        # end=True, score 출력
        if current_target_index == 2:
            _data = {
                "uid": msg.uid,
                "targets": _status["targets"],
                "current_target_index": current_target_index,
                "current_hint_img_index": _status["current_hint_img_index"],
                "trial": trial,
                "score": score
            }

            write_user_data(msg.uid, _data)
                    
            output = {
                # "hint_b64_imgs": [],
                "current_target_index": current_target_index,
                "current_hint_img_index": _data["current_hint_img_index"],
                "score": score,
                "result": result, # 문제를 맞혔는지
                "trial": trial, 
                "target": target_word,
                "end": True
            }
        else:
            # 맞았는데 마지막 문제가 아님.
            # 다음 문제와 다음 문제의 힌트 이미지 부여
            current_target_index += 1
            current_hint_img_index = 0

            # _b64_img = df[df["target"]==_status["targets"][current_target_index]].iloc[0, 3]
            
            # reset trial
            trial = 0

            _data = {
                "uid": msg.uid,
                "targets": _status["targets"],
                "current_target_index": current_target_index,
                "current_hint_img_index": current_hint_img_index,
                "trial": trial,
                "score": score
            }

            write_user_data(msg.uid, _data)
            
            # output 정의해주기
            output = {
                # "hint_b64_imgs": [_b64_img],
                "current_target_index": current_target_index,
                "current_hint_img_index": current_hint_img_index,
                "score": score,
                "result": result, # 문제를 맞혔는지
                "trial": trial, 
                "target": target_word,
                "end": False
            }
        
    else:
        current_hint_img_index = _status["current_hint_img_index"]
        # 틀리면 
        if trial < 3:
            # trial < 3 이면 기존 힌트 인덱스 찾아서 힌트 이미지 출력
            # 다음 힌트 달라고 하는건 별개 엔드포인트 부여
            _data = {
                "uid": msg.uid,
                "targets": _status["targets"],
                "current_target_index": current_target_index,
                "current_hint_img_index": current_hint_img_index,
                "trial": trial,
                "score": score
            }
            write_user_data(msg.uid, _data)

            # b64_hint_imgs = []
            # for idx in range(0, current_hint_img_index+1):
            #     tmp_img = df[df["target"]==_status["targets"][current_target_index]].iloc[idx, 3]
            #     b64_hint_imgs.append(tmp_img)

            output = {
                # "hint_b64_imgs": b64_hint_imgs,
                "current_target_index": current_target_index,
                "current_hint_img_index": current_hint_img_index,
                "score": score,
                "result": result, # 문제를 맞혔는지
                "trial": trial, 
                "target": None,
                "end": False
            }
        
        # 틀렸음
        # trial == 3 이면 
        # 마지막 문제 아닐 경우, 
        #   다음 힌트
        #   마지막 힌트면, 다음 문제 부여

        # 마지막 문제일 경우, 
        #   다음 힌트
        #   마지막 힌트면, 종료

        # 마지막 힌트인지 아닌지 먼저 체크
        elif trial == 3:
            if current_hint_img_index < 2:
                current_hint_img_index = _status["current_hint_img_index"] + 1
                trial = 0

                _data = {
                    "uid": msg.uid,
                    "targets": _status["targets"],
                    "current_target_index": current_target_index,
                    "current_hint_img_index": current_hint_img_index,
                    "trial": trial,
                    "score": score
                }
                write_user_data(msg.uid, _data)

                # b64_hint_imgs = []
                # for idx in range(0, current_hint_img_index+1):
                #     tmp_img = df[df["target"]==_status["targets"][current_target_index]].iloc[idx, 3]
                #     b64_hint_imgs.append(tmp_img)

                output = {
                    # "hint_b64_imgs": b64_hint_imgs,
                    "current_target_index": current_target_index,
                    "current_hint_img_index": current_hint_img_index,
                    "score": score,
                    "result": result, 
                    "trial": trial, 
                    "target": None,
                    "end": False
                }
            elif current_hint_img_index == 2:
                # 마지막 힌트였는데 세 번 다 틀림

                if current_target_index == 2:
                    # 마지막 문제일 경우
                    _data = {
                        "uid": msg.uid,
                        "targets": _status["targets"],
                        "current_target_index": current_target_index,
                        "current_hint_img_index": current_hint_img_index,
                        "trial": trial,
                        "score": score
                    }
                    write_user_data(msg.uid, _data)

                    output = {
                        # "hint_b64_imgs": [],
                        "current_target_index": current_target_index,
                        "current_hint_img_index": current_hint_img_index,
                        "score": score,
                        "result": result, # 문제를 맞혔는지
                        "trial": trial, 
                        "target": target_word,
                        "end": True
                    }
                elif current_target_index < 2:
                    # 다음 문제 주기

                    current_target_index = current_target_index + 1

                    current_hint_img_index = 0
                    trial = 0

                    _data = {
                        "uid": msg.uid,
                        "targets": _status["targets"],
                        "current_target_index": current_target_index,
                        "current_hint_img_index": current_hint_img_index,
                        "trial": trial,
                        "score": score
                    }
                    write_user_data(msg.uid, _data)

                    # b64_img = df[df["target"]==_status["targets"][current_target_index]].iloc[0, 3]

                    output = {
                        # "hint_b64_imgs": [b64_img],
                        "current_target_index": current_target_index,
                        "current_hint_img_index": current_hint_img_index,
                        "score": score,
                        "result": result, # 문제를 맞혔는지
                        "trial": trial, 
                        "target": target_word,
                        "end": False
                    }

    
    return output

@app.post("/catchping_backend/next_hint")
async def single_mode_next_hint(msg: InitInfo):
    # uid 기준 status 가져오기
    _status = read_user_data(msg.uid)
    
    # 현재 문제가 뭔지 확인
    current_target_index = _status["current_target_index"]
    target_word = _status["targets"][current_target_index]
    score = _status["score"]

    # validation 필요
    # 3번째 힌트면 못 줌.
    if _status["current_hint_img_index"] == (len(_status["targets"]) - 1):
        raise HTTPException(400, detail="You have already received all hints.")
    
    current_hint_img_index = _status["current_hint_img_index"] + 1
    trial = 0

    _data = {
        "uid": msg.uid,
        "targets": _status["targets"],
        "current_target_index": current_target_index,
        "current_hint_img_index": current_hint_img_index,
        "trial": trial,
        "score": score
    }
    write_user_data(msg.uid, _data)

    # b64_hint_imgs = []
    # for idx in range(0, current_hint_img_index+1):
    #     tmp_img = df[df["target"]==target_word].iloc[idx, 3]
    #     b64_hint_imgs.append(tmp_img)

    output = {
        # "hint_b64_imgs": b64_hint_imgs,
        "current_target_index": current_target_index,
        "current_hint_img_index": current_hint_img_index,
        "score": score,
        "result": False, 
        "trial": trial, 
        "target": None,
        "end": False
    }

    return output


@app.post("/catchping_backend/giveup")
async def giveup(msg: InitInfo):
    # uid 기준 status 가져오기
    _status = read_user_data(msg.uid)
    
    # 현재 문제가 뭔지 확인
    current_target_index = _status["current_target_index"]
    target_word = _status["targets"][current_target_index]
    score = _status["score"]

    # 현재 문제를 모르겠다고 포기한다는 의미
    # 정답 알려주고
    
    # 다음 문제 있으면 진행
    if current_target_index < 2:
        # TODO target_word 제대로 나오는지 확인, 이전 정답이 나와야 함.
        current_target_index += 1
        current_hint_img_index = 0
        trial = 0
        
        _data = {
            "uid": msg.uid,
            "targets": _status["targets"],
            "current_target_index": current_target_index,
            "current_hint_img_index": current_hint_img_index,
            "trial": trial,
            "score": score
        }
        write_user_data(msg.uid, _data)
        
        # b64_img = df[df["target"]==_status["targets"][current_target_index]].iloc[current_hint_img_index, 3]
        
        output = {
            # "hint_b64_imgs": [b64_img],
            "current_target_index": current_target_index,
            "current_hint_img_index": current_hint_img_index,
            "score": score,
            "result": False, 
            "trial": trial, 
            "target": target_word,
            "end": False
        }
    
    else:
        # 마지막 문제면 스코어 보여주고 마무리
        
        output = {
            # "hint_b64_imgs": [],
            "current_target_index": current_target_index,
            "current_hint_img_index": _status["current_hint_img_index"],
            "score": score,
            "result": False, 
            "trial": trial, 
            "target": target_word,
            "end": True
        }

    return output

@app.post("/catchping_backend/init_single_mode")
async def init_single_mode(msg: InitInfo):
    """처음 요청"""
    # 문제 뽑기
    _targets = random.choices(df["target"].unique(), k=3)

    # 모든 문제의 b64 image
    _b64_imgs = []

    for i in range(len(_targets)):
        quiz_set = df[df["target"]==_targets[i]]
        tmp = []
        for j in range(len(quiz_set)):
            tmp.append(quiz_set.iloc[j, 3])
        _b64_imgs.append(tmp)

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
        "hint_b64_imgs": _b64_imgs,
        "current_target_index": _data["current_target_index"], # 타겟 단어 인덱스
        "current_hint_img_index": _data["current_hint_img_index"], # 힌트 이미지 인덱스
        "score": _data["score"],
        # "result": False, # 문제를 맞혔는지
        # "trial": _data["trial"], 
        # "end": False
    }

    return output


if __name__=="__main__":
	
    uvicorn.run(
        app="game_server:app",
        host="0.0.0.0",
        port=5001,
        reload=False,
        workers=1
    )
