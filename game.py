import os
import sys

class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = 0
        self.is_windows = os.name == "nt"  # 초기화 시 OS 한 번만 확인

    def clear(self):
        if self.is_windows:
            os.system("cls")
        else:
            sys.stdout.write("\033[2J\033[H")
            sys.stdout.flush()

    # --- 진입점 ---
    def run(self):
        self.show_menu()

    # --- 메뉴 ---
    def show_menu(self):
        self.clear()
        main_menu = "=== 퀴즈 게임 ===\n1. 퀴즈 풀기\n2. 퀴즈 추가\n3. 퀴즈 목록\n4. 점수 확인\n5. 종료"
        print(main_menu)
        main_input = input("선택 > ").strip()

        if not main_input.isdigit():
            print("***숫자만 입력하세요.***")
            return self.show_menu()

        if main_input not in ["1", "2", "3", "4", "5"]:
            print("***잘못된 범위의 숫자입니다. 다시 입력해주세요.***")
            return self.show_menu()

        return self.handle_menu(int(main_input))

    def handle_menu(self, choice):
        if choice == 1:
            self.play()
        elif choice == 2:
            self.add_quiz()
        elif choice == 3:
            self.show_list()
        elif choice == 4:
            self.show_score()
        elif choice == 5:
            print("게임을 종료합니다.")
            exit()

    # # --- 기능 ---
    # def play(self):
    #     # 퀴즈 풀기 전체 흐름

    # def add_quiz(self):
    #     # 새 퀴즈 입력받아 추가

    # def show_list(self):
    #     # 퀴즈 목록 출력

    # def show_score(self):
    #     # 최고 점수 출력

    # # --- 파일 입출력 ---
    # def save(self):
    #     # state.json에 저장

    # def load(self):
    #     # state.json에서 불러오기

    # # --- 입력 처리 ---
    # def input_number(self, prompt, min_val, max_val):
    #     # 숫자 입력 + 예외처리 반복 루프 → int
    #     # 공백/빈값/문자/범위밖 모두 여기서 처리