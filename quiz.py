class Quiz:
    def __init__(self, question, choices, answer, hint=None, is_custom=False):
        self.question = question   # str
        self.choices = choices     # list[str] (4개)
        self.answer = answer       # int (1~4)
        self.hint = hint
        self.is_custom = is_custom  # 기본: False, 사용자 추가: True
        self.record = None  # 플레이 기록 (맞춘 시간, 시도 횟수 등)

    def display(self):
        # 문제와 선택지를 출력
        print(self.question)
        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")
        print(f"힌트: {self.hint}") if self.hint else None

    def check(self, user_answer):
        # 정답 여부 반환 → bool
        return user_answer == self.answer

    def to_dict(self):
        # JSON 저장용 dict로 변환 → dict
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
            "is_custom": self.is_custom
        }
    
    # static method란 클래스의 인스턴스와 직접적으로 관련이 없는 메서드로, 클래스 이름으로 호출할 수 있는 메서드입니다.
    # static method를 쓰는 이유 : Quiz 클래스의 인스턴스를 생성하는 별도의 메서드로, Quiz 객체를 생성할 때 필요한 데이터를 dict 형태로 받아서 Quiz 객체로 변환하는 역할을 합니다. 
    # 이 메서드는 Quiz 클래스의 인스턴스와 직접적으로 관련이 없으며, 단순히 데이터를 변환하는 기능을 수행하기 때문에 static method로 정의하는 것이 적절합니다.
    @staticmethod
    def from_dict(data):
        # dict → Quiz 인스턴스 (불러오기용)
        return Quiz(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
            hint=data["hint"] if "hint" in data else None,
            is_custom=data["is_custom"]
        )

    # static method: Quiz 인스턴스 생성자 (from_dict)
    @staticmethod
    def from_dict(data):
        # dict → Quiz 인스턴스로 변환 (파일 불러올 때 사용)
        return Quiz(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
            hint=data["hint"] if "hint" in data else None,
            is_custom=data["is_custom"]
        )