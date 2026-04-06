# 퀴즈 게임 프로젝트

## 목차

1. [환경 설정](#환경-설정)
2. [브랜치 전략](#브랜치-전략)
3. [단계별 구현 순서](#단계별-구현-순서)
4. [커밋 메시지 컨벤션](#커밋-메시지-컨벤션)
5. [제출 체크리스트](#제출-체크리스트)

---

## 환경 설정

### 1. uv 설치

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. 프로젝트 초기화

```bash
uv init .
```

### 3. Python 버전 고정

```bash
uv python pin 3.12
```

### 4. 가상환경 생성 및 활성화

```bash
uv venv

# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\activate
```

### 5. 프로그램 실행

```bash
uv run main.py
```

### 파일 구조

```
프로젝트 루트/
├── .venv/            # 가상환경 (git 제외)
├── .python-version   # Python 버전 고정
├── pyproject.toml    # 프로젝트 설정
├── main.py           # 메인 실행 파일
├── game.py           # QuizGame 클래스 (게임 로직)
├── quiz.py           # Quiz 클래스 (퀴즈 모델)
├── state.json        # 퀴즈/점수 저장 파일 (자동 생성)
├── .gitignore
└── README.md
```

### .gitignore 설정

```
.venv/
__pycache__/
*.pyc
.python-version
```

---

## 브랜치 전략

`main` 브랜치에는 완성된 기능만 병합합니다.
기능 개발은 항상 별도 브랜치를 만들어 작업한 뒤 `main`에 병합합니다.

```
main
├── feature/init          → 프로젝트 초기 설정
├── feature/menu          → 메뉴 기능
├── feature/quiz-class    → Quiz 클래스 + 기본 데이터
├── feature/quiz-play     → 퀴즈 풀기
├── feature/quiz-add      → 퀴즈 추가
├── feature/quiz-list     → 퀴즈 목록
├── feature/score         → 점수 확인
├── feature/quiz-game     → QuizGame 클래스 정리
├── feature/file-io       → state.json 저장/불러오기
└── feature/docs          → README.md 작성
```

### 브랜치 작업 기본 흐름

```bash
# 1. 새 브랜치 생성 및 이동
git checkout -b feature/브랜치명

# 2. 작업 후 커밋
git add .
git commit -m "feat: 기능 설명"

# 3. main으로 돌아와서 병합
git checkout main
git merge feature/브랜치명

# 4. 병합한 브랜치 삭제 (선택)
git branch -d feature/브랜치명
```

---

## 단계별 구현 순서

### STEP 1 — Git 저장소 설정

```bash
git checkout -b feature/init
```

**작업 내용**

- GitHub에 새 저장소 생성
- 로컬에 저장소 초기화 (`git init`)
- `.gitignore`, `README.md` 파일 생성

```bash
git add .
git commit -m "init: uv 초기화 및 README.MD 추가"
git checkout main
git merge feature/init
git push -u origin main
```

---

### STEP 2 — 메뉴 기능 구현

```bash
git checkout -b feature/menu
```

**요구사항**

- 실행 시 메뉴가 출력된다
- 번호를 입력하면 해당 기능으로 이동한다
- 종료 기능이 있다
- 잘못된 입력 시 안내 메시지를 출력하고 재입력을 받는다

**출력 예시**

```
=== 퀴즈 게임 ===
1. 퀴즈 풀기
2. 퀴즈 추가
3. 퀴즈 삭제
4. 퀴즈 목록
5. 플레이 기록 확인
6. 종료
메뉴 번호를 입력하세요 >
```

```bash
git add .
git commit -m "feat: 메인 메뉴 출력 및 입력 처리 구현"
git checkout main
git merge feature/menu
git push origin main
```

---

### STEP 3 — 공통 입력 / 예외 처리 기준

> 별도 브랜치 없이, 이후 모든 기능 구현 시 아래 기준을 일관되게 적용합니다.

**숫자 입력 처리**

| 케이스 | 처리 방법 |
|---|---|
| 앞뒤 공백 (예: `" 1 "`) | `.strip()` 후 처리 |
| 문자 입력 (예: `"abc"`) | 안내 메시지 출력 후 재입력 |
| 범위 밖 숫자 (예: 메뉴에서 `9`) | 안내 메시지 출력 후 재입력 |
| 빈 입력 (그냥 Enter) | 안내 메시지 출력 후 재입력 |

**프로그램 전체 예외 처리**

| 상황 | 처리 방법 |
|---|---|
| `Ctrl+C` (KeyboardInterrupt) | 안내 메시지 출력 후 저장하고 종료 |
| `EOF` (EOFError) | 동일하게 안전 종료 |
| `state.json` 없음 | 기본 퀴즈 데이터로 실행 |
| `state.json` 손상 | 안내 메시지 출력 후 기본 데이터로 초기화 |

---

### STEP 4 — Quiz 클래스 정의 + 기본 퀴즈 데이터 작성

```bash
git checkout -b feature/quiz-class
```

**Quiz 클래스 속성**

| 속성 | 설명 |
|---|---|
| `question` | 문제 텍스트 |
| `choices` | 선택지 4개 (리스트) |
| `answer` | 정답 번호 (1~4) |

**Quiz 클래스 메서드**

- `display()` — 문제와 선택지 출력
- `check(user_answer)` — 정답 여부 반환

```python
class Quiz:
    def __init__(self, question, choices, answer, hint=None, is_custom=False):
        self.question = question
        self.choices = choices    # ["선택1", "선택2", "선택3", "선택4"]
        self.answer = answer      # 1~4
        self.hint = hint
        self.is_custom = is_custom  # 기본: False, 사용자 추가: True

    def display(self):
        pass

    def check(self, user_answer):
        pass
```

**기본 퀴즈 데이터 요구사항**

- 본인이 직접 고른 주제의 퀴즈 5개 이상 작성
- 각 퀴즈는 문제 + 선택지 4개 + 정답 번호 포함
- `Quiz` 클래스의 인스턴스로 생성

```bash
git add .
git commit -m "feat: Quiz 클래스 정의 및 CLI 초기화 OS 별 분기 처리 추가"
git add .
git commit -m "feat: default quizzes 추가"
git checkout main
git merge feature/quiz-class
git push origin main
```

---

### STEP 5 — 퀴즈 풀기 기능 구현

```bash
git checkout -b feature/quiz-play
```

**요구사항**

- 풀 문제 수를 선택할 수 있다
- 퀴즈를 랜덤 순서로 출제한다
- 사용자가 1~4 중 번호로 정답을 입력한다
- 정답/오답 여부를 즉시 알려준다
- 문제별 소요 시간을 측정한다
- 모든 문제를 풀면 최종 점수, 정답률, 플레이타임, 평균 시간을 표시한다
- 최고 점수 갱신 시 알림을 출력한다
- 퀴즈가 없을 경우 안내 메시지를 출력한다

```bash
git add .
git commit -m "feat: 퀴즈 풀기 기능 구현"
git checkout main
git merge feature/quiz-play
git push origin main
```

play() 호출
│
├── 퀴즈 없음? → 안내 메시지 → 메뉴로 복귀
│
└── 퀴즈 있음
    │
    ├── 풀 문제 수 선택
    ├── score = 0, 퀴즈 랜덤 셔플
    │
    └── for quiz in shuffled_quizzes
        │
        ├── quiz.display()         # 문제 + 선택지 출력
        ├── input_number(1~4)      # 정답 입력 + 소요 시간 측정
        ├── quiz.check(answer)
        │   ├── 정답 → "정답입니다!" + score += 1
        │   └── 오답 → "오답입니다. 정답은 N번입니다."
        │
        └── 모든 문제 완료
            │
            ├── 최종 점수, 정답률, 플레이타임, 평균 시간 출력
            ├── best_score 갱신 여부 확인
            ├── history에 기록 추가
            └── save()

---

### STEP 6 — 퀴즈 추가 기능 구현

```bash
git checkout -b feature/quiz-add
```

**입력 순서**

1. 문제 입력
2. 선택지 4개 입력
3. 정답 번호 입력 (1~4)
4. 힌트 입력 (선택 사항, 엔터로 건너뛰기)

**요구사항**

- 잘못된 입력 시 STEP 3의 공통 처리 기준 적용
- 추가한 퀴즈를 즉시 `state.json`에 저장

```bash
git add .
git commit -m "feat: 퀴즈 추가 기능 구현"
git checkout main
git merge feature/quiz-add
git push origin main
```

---

### STEP 7 — 퀴즈 목록 기능 구현

```bash
git checkout -b feature/quiz-list
```

**요구사항**

- 번호와 문제를 목록으로 출력한다
- 퀴즈가 없을 경우 안내 메시지를 출력한다

```bash
git add .
git commit -m "feat: 퀴즈 목록 출력 기능 구현"
git checkout main
git merge feature/quiz-list
git push origin main
```

---

### STEP 8 — 파일 저장 / 불러오기 (state.json)

```bash
git checkout -b feature/file-io
```

**저장 위치:** 프로젝트 루트 `state.json` (UTF-8 인코딩)

**스키마**

```json
{
  "quizzes": [
    {
      "question": "문제 텍스트",
      "choices": ["선택1", "선택2", "선택3", "선택4"],
      "answer": 1,
      "hint": "힌트 텍스트 또는 null",
      "is_custom": false
    }
  ],
  "best_score": 5,
  "history": [
    {
      "date": "2026-04-07 04:50:26",
      "total": 5,
      "score": 2,
      "playtime": 1.7,
      "avg_time": 0.3,
      "accuracy": 40.0
    }
  ]
}
```

**처리 규칙**

- 파일 없음 → 기본 퀴즈 데이터로 시작
- 파일 손상 → 안내 메시지 후 기본 데이터로 초기화
- 모든 읽기/쓰기는 `try/except`로 처리

```bash
git add .
git commit -m "feat: state.json 파일 저장/불러오기 구현"
git checkout main
git merge feature/file-io
git push origin main
```
---

### STEP 9 — 점수 확인 기능 구현

```bash
git checkout -b feature/score
```

**요구사항**

- 퀴즈를 풀 때마다 기존 최고 점수와 비교한다
- 더 높으면 최고 점수를 갱신하고 `state.json`에 저장한다
- 메뉴에서 최고 점수를 확인할 수 있다
- 아직 퀴즈를 풀지 않은 경우 안내 메시지를 출력한다

```bash
git add .
git commit -m "feat: 최고 점수 저장 및 확인 기능 구현"
git checkout main
git merge feature/score
git push origin main
```

---

### STEP 10 — README.md 작성

```bash
git checkout -b feature/docs
```

**포함 항목**

1. 프로젝트 개요
2. 퀴즈 주제 및 선정 이유
3. 실행 방법
4. 기능 목록
5. 파일 구조
6. `state.json` 경로 / 역할 / 스키마 설명

```bash
git add .
git commit -m "docs: README.md 작성 완료"
git checkout main
git merge feature/docs
git push origin main
```

---

### STEP 11 — clone & pull 실습

```bash
# 1. 별도 폴더에 저장소 복제
git clone https://github.com/본인계정/저장소명.git 새폴더명

# 2. 복제된 폴더에서 변경 후 push
cd 새폴더명
git add .
git commit -m "docs: clone 실습 - README 한 줄 추가"
git push

# 3. 원래 폴더로 돌아와서 pull
cd ../기존폴더명
git pull origin main
```

---

### STEP 12 — 다른 환경에서 가상환경 설정

다른 PC나 환경에서 이 프로젝트를 클론한 뒤, 가상환경을 새로 생성해야 합니다.
`.venv/` 폴더는 `.gitignore`에 포함되어 있으므로 저장소에 포함되지 않습니다.

```bash
# 1. 저장소 클론
git clone https://github.com/본인계정/저장소명.git
cd 저장소명

# 2. uv가 설치되어 있지 않다면 먼저 설치
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 3. 가상환경 생성 (.python-version에 고정된 버전으로 자동 설정)
uv venv

# 4. 가상환경 활성화
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\activate

# 5. 의존성 설치 (pyproject.toml 기준)
uv sync

# 6. 프로그램 실행
uv run main.py
```

> **참고:** `uv sync`는 `pyproject.toml`에 명시된 의존성을 가상환경에 설치합니다.
> 현재 이 프로젝트는 외부 패키지 의존성이 없으므로, `uv venv` 후 바로 `uv run main.py`로 실행해도 됩니다.

---

## 커밋 메시지 컨벤션

### 기본 구조

```
type: 제목 (50자 이내)
```

### type 종류

| type | 언제 쓰나 |
|---|---|
| `feat` | 새 기능 추가 |
| `fix` | 버그 수정 |
| `docs` | README 등 문서 수정 |
| `refactor` | 기능 변화 없이 코드 구조 개선 |
| `style` | 들여쓰기, 공백 등 포맷만 변경 |
| `test` | 테스트 코드 추가/수정 |
| `chore` | 빌드 설정, .gitignore 등 기타 |
| `init` | 프로젝트 최초 설정 |

### 이 프로젝트 커밋 예시

```
init: 프로젝트 초기 설정 및 .gitignore 추가
feat: 메인 메뉴 출력 및 입력 처리 구현
feat: Quiz 클래스 정의
feat: 기본 퀴즈 데이터 5개 작성
feat: 퀴즈 풀기 기능 구현
feat: 퀴즈 추가 기능 구현
feat: 퀴즈 목록 출력 기능 구현
feat: 최고 점수 저장 및 확인 기능 구현
feat: state.json 파일 저장/불러오기 구현
refactor: QuizGame 클래스로 전체 구조 정리
fix: 잘못된 입력 예외 처리 누락 수정
docs: README.md 작성 완료
```

### 제목 작성 규칙

- type은 소문자로 작성한다 — `Feat` ❌ `feat` ✅
- 마침표를 붙이지 않는다 — `메뉴 구현.` ❌ `메뉴 구현` ✅
- 무엇을 했는지 명확하게 작성한다 — `수정함` ❌ `입력 예외 처리 누락 수정` ✅

---

## 코드 리뷰 (수정 완료)

### 예외 처리 — 수정 완료

1. **`add_quiz` - 빈 입력 검증** — 빈 문제 입력 시 재입력 요구, 빈 정답 선택지 방어 추가
2. **`from_dict` - `is_custom` 키 누락 대응** — `if "is_custom" in data`로 방어 처리
3. **`load` - 파일 손상 시 처리** — 손상된 `state.json` 삭제 후 초기화
4. **`from_dict` - 선택지/정답 유효성 검증** — 선택지 4개, 정답 번호 1~4 범위 검증 추가

### 리팩터링 — 수정 완료

1. **`from_dict` 중복 정의** — 중복 제거, 하나만 유지
2. **재귀 메뉴 → `while` 루프** — `run()`에서 루프로 전환, 각 메서드의 `show_menu()` 재귀 호출 제거
3. **`show_list` 중복 출력** — 중복 `print` 제거
4. **변수명 PEP 8** — `warningMessage` → `warning_message`
5. **미사용 필드** — `quiz.py`의 `self.record` 제거
6. **`display` 표현식 문** — `if` 문으로 변경