import base64
import pandas as pd
import traceback
import numpy as np
import os

def save_base64_image(base64_str, file_path):
    # base64 문자열을 바이트로 디코딩
    img_data = base64.b64decode(base64_str)
    
    # 디코딩된 바이트 데이터를 파일로 저장
    with open(file_path, 'wb') as f:
        f.write(img_data)
    print(f"save {file_path}")


if __name__=="__main__":
    df = pd.read_csv("app/resources/single_mode_set.csv", encoding="utf-8")
    
    start = 0
    for i in range(start, len(df)):
        try:
            hint_word = df.iloc[i, 1]
            _target = df.iloc[i, 0]
            _path = f"app/resources/ex/{_target}_{hint_word}.png"
            if type(df.iloc[i,3]) == str:
                if not os.path.isfile(_path):
                    if len(hint_word) > 40:
                        _path = f"app/resources/ex/{_target}_{hint_word[:30]}.png"
                    else:
                        _path = f"app/resources/ex/{_target}_{hint_word}.png"
                    if not os.path.isfile(_path):
                        save_base64_image(df.iloc[i,3], _path)
        except:
            print(f"{_path} failed")
            print(traceback.format_exc())
            break