from game import QuizGame
import signal

def main():
    def handle_suspend(signum, frame):
        # Ctrl+Z로 프로그램이 일시 중지되는 것을 방지하기 위해 시그널 핸들러를 설정합니다.(macOS에서는 SIGTSTP가 Ctrl+Z에 해당합니다.)
        print("\nCtrl+Z는 사용할 수 없습니다.")

    signal.signal(signal.SIGTSTP, handle_suspend)

    game = QuizGame()
    
    try:
        game.run()
    except KeyboardInterrupt:
        print("\n\n프로그램을 종료합니다.(keyboard interrupt)")
        game.save()
    except EOFError:
        print("\n입력 스트림이 종료되었습니다.(EOF error)")
        game.save()

if __name__ == "__main__":
    main()
