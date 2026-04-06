from game import QuizGame
import signal

def main():
    def handle_suspend(signum, frame):
        # Ctrl+Z로 프로그램이 일시 중지되는 것을 방지하기 위해 시그널 핸들러를 설정(macOS에서는 SIGTSTP가 Ctrl+Z에 해당)
        print("\nCtrl+Z는 사용할 수 없습니다.")

    if hasattr(signal, 'SIGTSTP'): # SIGTSTP가 지원되는 플랫폼에서만 핸들러를 설정
        signal.signal(signal.SIGTSTP, handle_suspend)

    game = QuizGame()
    
    try:
        game.run()
    except KeyboardInterrupt: # Ctrl+C로 프로그램이 종료될 때를 처리
        print("\n\n프로그램을 종료합니다.(keyboard interrupt)")
        game.save()
    except EOFError: # 입력 스트림이 종료될 때를 처리합니다. (예: Ctrl+D)
        print("\n입력 스트림이 종료되었습니다.(EOF error)")
        game.save()

if __name__ == "__main__": # 클래스로 객체를 만들 때 자동으로 호출되는 초기화 메서드
    main()

# __--__는 파이썬에서 특별한 의미를 가지는 메서드나 속성을 나타내는 네이밍 컨벤션임(매직 매서드magic method 또는 dunder method라고도 불림)
# 예를 들어, __init__은 클래스의 인스턴스가 생성될 때 자동으로 호출되는 초기화 메서드임 
# 이러한 메서드들은 파이썬의 데이터 모델에서 특별한 역할을 함
# 일반적으로 직접 호출하기보다는 파이썬 인터프리터에 의해 자동으로 호출됨 
# 일반적으로 클래스의 동작을 정의하거나 객체의 상태를 관리하는 데 사용됨