from fastapi import FastAPI  # FastAPI import
import pandas as pd
import uvicorn

app = FastAPI()

df = pd.read_csv("app/resources/single_mode_set.csv", encoding="utf-8")

@app.post("/catchping_backend/single_mode_quiz")
def single_mode():
	output = {
		"target_word": df.iloc[0,0],
		"hints_b64_imgs": [
			df.iloc[0,3],
			df.iloc[1,3],
			df.iloc[2,3]
        ]
    }
	# print(f"output: {output}")
	return output

if __name__=="__main__":
	
    uvicorn.run(
        app="dummy:app",
        host="0.0.0.0",
        port=5001,
        reload=False,
        workers=1
    )
