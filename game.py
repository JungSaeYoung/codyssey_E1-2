import os
import sys
from quiz import Quiz
import json

class QuizGame:
    def __init__(self):
        self.best_score = 0
        self.is_windows = os.name == "nt"  # 초기화 시 OS 한 번만 확인
        self.quizzes = self.default_quizzes()  # 기본 탑재된 퀴즈 로드
        self.warningMessage = self.load()  # 게임 실행 후 상태 불러오기

    # --- 진입점 ---
    def run(self):
        self.show_menu(warningMessage=self.warningMessage)

    # --- 메뉴 ---
    def show_menu(self, warningMessage=None):
        self.clear()
        main_menu = "=== 퀴즈 게임 ===\n1. 퀴즈 풀기\n2. 퀴즈 추가\n3. 퀴즈 목록\n4. 점수 확인\n5. 종료"
        print(main_menu)
        if warningMessage:
            print(warningMessage)
        main_input = self.input_number("메뉴 번호를 입력하세요 > ", 1, 5)

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

    # --- 기능 ---
    def play(self):
      self.clear()
      print("=== 퀴즈 풀기 ===\n")

      if not self.quizzes:
          print("등록된 퀴즈가 없습니다.")
          input("엔터를 누르면 메뉴로 돌아갑니다.")
          return self.show_menu()

      score = 0

      for i, quiz in enumerate(self.quizzes):
          print(f"[{i + 1} / {len(self.quizzes)}]")
          quiz.display()

          user_answer = self.input_number("정답 번호 > ", 1, 4)

          if quiz.check(user_answer):
              print("정답입니다!\n")
              score += 1
          else:
              print(f"오답입니다. 정답은 {quiz.answer}번입니다.\n")

      # 최종 결과
      print(f"최종 점수: {score} / {len(self.quizzes)}")

      if score > self.best_score:
          self.best_score = score
          print("최고 점수를 갱신했습니다!")

      self.save()
      input("\n엔터를 누르면 메뉴로 돌아갑니다.")
      self.show_menu()
    
    def add_quiz(self):
      self.clear()
      print("=== 퀴즈 추가 ===")

      question = input("문제를 입력하세요 > ").strip()

      choices = []
      for i in range(1, 5):
          choice = input(f"{i}번 선택지 > ").strip()
          choices.append(choice)

      answer = self.input_number("정답 번호 (1~4) > ", 1, 4)

      self.quizzes.append(Quiz(question, choices, answer, is_custom=True))
      self.save()  # 즉시 저장
      print("퀴즈가 추가되었습니다.")
      self.show_menu()

    def show_list(self):
      self.clear()
      print("=== 퀴즈 목록 ===\n")

      if not self.quizzes:
          print("등록된 퀴즈가 없습니다.")
          input("\n엔터를 누르면 메뉴로 돌아갑니다.")
          return self.show_menu()

      for i, quiz in enumerate(self.quizzes, start=1):
          label = "[사용자 추가]" if quiz.is_custom else "[기본]"
          print(f"[{i}] {label} {quiz.question}")
          print(f"[{i}] {quiz.question}")

          for j, choice in enumerate(quiz.choices, start=1):
              if j == quiz.answer:
                  print(f"  {j}. {choice}  ← 정답")
              else:
                  print(f"  {j}. {choice}")
          print()

      print(f"총 {len(self.quizzes)}개의 퀴즈가 있습니다.")
      input("\n엔터를 누르면 메뉴로 돌아갑니다.")
      self.show_menu()

    def show_score(self):
      self.clear()
      print("=== 점수 확인 ===\n")
      print(f"최고 점수: {self.best_score} / {len(self.quizzes)}")
      input("\n엔터를 누르면 메뉴로 돌아갑니다.")
      self.show_menu()

    # --- 파일 입출력 ---
    FILE_PATH = "state.json"

    def save(self):
        try:
            data = {
                "quizzes": [quiz.to_dict() for quiz in self.quizzes],
                "best_score": self.best_score
            }
            with open(self.FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                # ensure_ascii=False — 한글이 유니코드 이스케이프(\uc608\uc2dc) 대신 한글 그대로 저장됩니다.
        except OSError:
            print("파일 저장에 실패했습니다.")

    def load(self):
        try:
            with open(self.FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.quizzes = [Quiz.from_dict(q) for q in data["quizzes"]]
                self.best_score = data["best_score"]
        except FileNotFoundError:
            self.quizzes = self.default_quizzes()
        except (json.JSONDecodeError, KeyError):
            print("데이터 파일이 손상되었습니다. 기본 데이터로 초기화합니다.")
            self.quizzes = self.default_quizzes()
            return "!!warning!! 데이터 파일이 손상되어 초기화되었습니다. !!"

    # --- 유틸리티 ---
    # 숫자 입력 시 예외 처리를 위해 input 함수 래핑
    def input_number(self, prompt, min_val, max_val):
      while True:
          user_input = input(prompt).strip()
          if not user_input.isdigit():
              print("***숫자만 입력하세요.***")
              continue

          number = int(user_input)
          if number < min_val or number > max_val:
              print(f"***{min_val}에서 {max_val} 사이의 숫자를 입력하세요.***")
              continue

          return number

    # 화면 클리어 함수 (Windows와 Unix 계열 OS 모두 지원)
    def clear(self):
      if self.is_windows:
          os.system("cls")
      else:
          sys.stdout.write("\033[2J\033[H")
          sys.stdout.flush()

    # 기본 퀴즈 6개 제공
    def default_quizzes(self):
        return [
            Quiz(
                question="다음 중 파이썬의 자료형이 아닌 것은?",
                choices=["list", "tuple", "dict", "array"],
                answer=4
            ),
            Quiz(
                question="다음 중 파이썬에서 반복문을 만드는 키워드가 아닌 것은?",
                choices=["for", "while", "repeat", "do"],
                answer=3
            ),
            Quiz(
                question="다음 중 파이썬에서 함수를 정의하는 키워드는?",
                choices=["function", "def", "fun", "define"],
                answer=2
            ),
            Quiz(
                question="다음 중 파이썬에서 예외 처리를 위한 키워드가 아닌 것은?",
                choices=["try", "except", "catch", "finally"],
                answer=3
            ),
            Quiz(
                question="다음 중 파이썬에서 모듈을 가져오는 키워드는?",
                choices=["import", "include", "require", "using"],
                answer=1
            ),
            Quiz(
                question="다음 중 파이썬에서 클래스 정의에 사용하는 키워드는?",
                choices=["class", "object", "def", "struct"],
                answer=1
            )
        ]