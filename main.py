from os import getenv
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

"""

# single play mode

3문제 맞추기
문제당 3개의 연상 단어 생성

연상 단어의 이미지를 어떻게 출력할지
1. 연상 단어 검색 -> top1 출력
2. 연상 단어를 위한 이미지 프롬프트 생성 -> 이미지 생성

정답 확인 LLM

첫번째 연상단어에서 맞추면 3점, 두번째 연상단어에서 맞추면 2점, 세번째 연상단어에서 맞추면 1점

3문제 합산 점수 부여

# multiple play mode





"""


def get_hint_images_for_single_mode(word):
    """싱글 플레이 모드에서 word의 힌트 이미지를 반환하는 함수"""
    pass


if __name__=="__main__":
    from app.modes.single_play import make_single_play_set, make_the_hints

    make_single_play_set(0, 120, True)
    # make_the_hints("도서관")
    """
    - hint: Rows of tall shelves filled with colorful spines
    - hint: a quiet place where a student immerses in a book
    - hint: a librarian organizing stacks of dusty tomes.
    """
