# CatchPingFromImageGen
Catch mind from generated image hint


## Single Mode

1. Randomly select a target word.
2. target word에 대한 힌트 및 힌트 이미지가 있는지 확인
    1. 힌트 이미지가 있으면 힌트 이미지 출력
    2. 힌트 이미지 없으면 힌트 3가지 생성, 힌트 3가지에 대한 이미지 생성(+ 등록)
3. 첫번째 이미지에서 맞추면 3점, 두번째 이미지에서 맞추면 2점, 세번째 이미지에 맞추면 1점, 못 맞추면 0점
4. 3문제를 내고 점수 합산


