import os
import sys
from quiz import Quiz
import json
import random
import datetime

class QuizGame:
    def __init__(self):
        self.best_score = 0
        self.is_windows = os.name == "nt"  # 초기화 시 OS 한 번만 확인
        self.quizzes = self.default_quizzes()  # 기본 탑재된 퀴즈 로드
        self.history = []  # 플레이 기록 (게임 결과 저장용)
        self.warning_message = self.load()  # 게임 실행 후 상태 불러오기

    # --- 진입점 ---
    def run(self):
        warning = self.warning_message  # 초기 경고 메시지 (파일 손상 등) 전달
        while True:
            choice = self.show_menu(warning)
            warning = None  # 메뉴는 한 번만 보여주고 초기화
            self.handle_menu(choice)

    # --- 메뉴 ---
    def show_menu(self, warningMessage=None):
        self.clear()
        main_menu = "=== 퀴즈 게임 ===\n1. 퀴즈 풀기\n2. 퀴즈 추가\n3. 퀴즈 삭제\n4. 퀴즈 목록\n5. 플레이 기록 확인\n6. 종료"
        print(main_menu)
        if warningMessage:
            print(warningMessage)
        main_input = self.input_number("메뉴 번호를 입력하세요 > ", 1, 6)
        
        return main_input

    def handle_menu(self, choice):
        if choice == 1:
            self.play()
        elif choice == 2:
            self.add_quiz()
        elif choice == 3:
            self.delete_quiz()
        elif choice == 4:
            self.show_list()
        elif choice == 5:
            self.show_score()
        elif choice == 6:
            print("게임을 종료합니다.")
            self.save()  # 종료 전 상태 저장
            exit()

    # --- 기능 ---
    def play(self):
        self.clear()
        print("=== 퀴즈 풀기 ===\n")

        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            input("엔터를 누르면 메뉴로 돌아갑니다.")
            return None

        # 문제 수 선택
        total = len(self.quizzes)
        print(f"총 {total}개의 퀴즈가 있습니다.")
        count = self.input_number(f"몇 문제를 풀겠습니까? (1~{total}) > ", 1, total)

        score = 0
        question_times = []                          # 문제별 소요 시간 기록
        shuffled_quizzes = random.sample(self.quizzes, count)  # 퀴즈 순서 랜덤 섞기

        game_start = datetime.datetime.now()         # 게임 시작 시간

        for i, quiz in enumerate(shuffled_quizzes):
            print(f"[{i + 1} / {len(shuffled_quizzes)}]")
            quiz.display()

            question_start = datetime.datetime.now() # 문제 시작 시간
            user_answer = self.input_number("정답 번호 > ", 1, 4)
            question_end = datetime.datetime.now()   # 문제 종료 시간

            elapsed = (question_end - question_start).total_seconds()
            question_times.append(elapsed)
            print(f"⏱ 소요 시간: {elapsed:.1f}초")

            if quiz.check(user_answer):
                print("정답입니다!\n")
                score += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.\n")

        game_end = datetime.datetime.now()           # 게임 종료 시간

        # 통계 계산
        playtime = (game_end - game_start).total_seconds()
        avg_time = playtime / count
        accuracy = (score / count) * 100

        # 최종 결과 출력
        print("─" * 40)
        print(f"최종 점수  : {score} / {count}")
        print(f"정답률     : {accuracy:.1f}%")
        print(f"총 플레이타임  : {playtime:.1f}초")
        print(f"문제 당 평균 시간: {avg_time:.1f}초")
        print("─" * 40)

        if score > self.best_score:
            self.best_score = score
            print("최고 점수를 갱신했습니다!")

        # 히스토리 기록
        record = {
            "date": game_start.strftime("%Y-%m-%d %H:%M:%S"),
            "total": count,
            "score": score,
            "playtime": round(playtime, 1),
            "avg_time": round(avg_time, 1),
            "accuracy": round(accuracy, 1)
        }
        self.history.append(record)
        self.save()
        input("\n엔터를 누르면 메뉴로 돌아갑니다.")

    def add_quiz(self):
        self.clear()
        print("=== 퀴즈 추가 ===")

        question = input("문제를 입력하세요 > ").strip()

        while not question:
            print("***문제를 입력해야 합니다.***")
            question = input("문제를 입력하세요 > ").strip()

        choices = []
        for i in range(1, 5):
            choice = input(f"{i}번 선택지 > ").strip()
            choices.append(choice)

        answer = self.input_number("정답 번호 (1~4) > ", 1, 4)

        while not choices[answer - 1]:
            print("***정답으로 선택된 번호의 선택지가 비어 있습니다.***")
            answer = self.input_number("정답 번호 (1~4) > ", 1, 4)

        hint = input("힌트를 입력하세요 (선택 사항, 엔터로 건너뛰기) > ").strip() or None

        self.quizzes.append(Quiz(question, choices, answer, hint=hint, is_custom=True))
        self.save()  # 즉시 저장
        print("퀴즈가 추가되었습니다.")

    def delete_quiz(self):
        self.clear()
        print("=== 퀴즈 삭제 ===\n")

        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            input("\n엔터를 누르면 메뉴로 돌아갑니다.")
            return None

        for i, quiz in enumerate(self.quizzes, start=1):
            label = "[사용자 추가]" if quiz.is_custom else "[기본]"
            print(f"[{i}] {label} {quiz.question}")

        print("취소하려면 0을 입력하세요.")
        index = self.input_number("삭제할 퀴즈 번호 > ", 0, len(self.quizzes)) - 1

        if index == -1:
            print("취소되었습니다.")
        elif not self.quizzes[index].is_custom:
            print("기본 퀴즈는 삭제할 수 없습니다.")
        else:
            del self.quizzes[index]
            self.save()  # 즉시 저장
            print("퀴즈가 삭제되었습니다.")

        input("\n엔터를 누르면 메뉴로 돌아갑니다.")

    def show_list(self):
        self.clear()
        print("=== 퀴즈 목록 ===\n")

        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            input("\n엔터를 누르면 메뉴로 돌아갑니다.")
            return None

        for i, quiz in enumerate(self.quizzes, start=1):
            label = "[사용자 추가]" if quiz.is_custom else "[기본]"
            print(f"[{i}] {label} {quiz.question}")

            for j, choice in enumerate(quiz.choices, start=1):
                if j == quiz.answer:
                    print(f"  {j}. {choice}  ← 정답")
                else:
                    print(f"  {j}. {choice}")
            print(f"  힌트: {quiz.hint}" if quiz.hint else "  힌트: 없음")

        print(f"총 {len(self.quizzes)}개의 퀴즈가 있습니다.")
        input("\n엔터를 누르면 메뉴로 돌아갑니다.")

    def show_score(self):
        self.clear()
        print("=== 점수 확인 ===\n")

        if not self.history:
            print("아직 게임 기록이 없습니다.")
            input("\n엔터를 누르면 메뉴로 돌아갑니다.")
            return None

        print(f"최고 점수: {self.best_score}점\n")
        print("─" * 90)
        print(f"{'#':<4} {'날짜':<22} {'점수':<8} {'정답률':<8} {'플레이타임':<12} {'평균시간'}")
        print("─" * 90)

        for i, r in enumerate(self.history, start=1):
            print(f"{i:<4} {r['date']:<22} {r['score']}/{r['total']:<5} {r['accuracy']:<7.1f}% {r['playtime']:<11.1f}초 {r['avg_time']:.1f}초")

        print("─" * 90)
        input("\n엔터를 누르면 메뉴로 돌아갑니다.")

    # --- 파일 입출력 ---
    FILE_PATH = "state.json"

    def save(self):
        try:
            data = {
                "quizzes": [quiz.to_dict() for quiz in self.quizzes],
                "best_score": self.best_score,
                "history": self.history
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
                self.history = data.get("history", [])
                return None  # 정상적으로 불러왔을 때는 경고 메시지 없음
        except FileNotFoundError:
            self.quizzes = self.default_quizzes()
        except (json.JSONDecodeError, KeyError):
            self.quizzes = self.default_quizzes()
            os.remove(self.FILE_PATH)  # 손상된 파일 삭제
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
                hint="파이썬에는 array 자료형이 없습니다.",
                answer=4
            ),
            Quiz(
                question="다음 중 파이썬에서 반복문을 만드는 키워드가 아닌 것은?",
                choices=["for", "while", "repeat", "do"],
                hint="파이썬에는 repeat와 do 키워드가 없습니다.",
                answer=3
            ),
            Quiz(
                question="다음 중 파이썬에서 함수를 정의하는 키워드는?",
                choices=["function", "def", "fun", "define"],
                hint="파이썬에서는 def 키워드를 사용하여 함수를 정의합니다.",
                answer=2
            ),
            Quiz(
                question="다음 중 파이썬에서 예외 처리를 위한 키워드가 아닌 것은?",
                choices=["try", "except", "catch", "finally"],
                hint="파이썬에는 catch 키워드가 없습니다.",
                answer=3
            ),
            Quiz(
                question="다음 중 파이썬에서 모듈을 가져오는 키워드는?",
                choices=["import", "include", "require", "using"],
                hint="파이썬에서는 import 키워드를 사용하여 모듈을 가져옵니다.",
                answer=1
            ),
            Quiz(
                question="다음 중 파이썬에서 클래스 정의에 사용하는 키워드는?",
                choices=["class", "object", "def", "struct"],
                hint="파이썬에서는 class 키워드를 사용하여 클래스를 정의합니다.",
                answer=1
            )
        ]